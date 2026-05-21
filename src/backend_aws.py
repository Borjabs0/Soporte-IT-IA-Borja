"""
backend_aws.py
Conexión con AWS Bedrock mediante boto3.
Usa AWS Bedrock Knowledge Bases (RAG oficial) para recuperar contexto
del Manual de Procedimientos, luego llama al modelo para generar
la clasificación, hoja de ruta y correo automático.
"""

import json
import os
import boto3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

# ── Configuración ────────────────────────────────────────────────────────────

MODEL_ID          = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
REGION            = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID", "")

# ── Clientes AWS ─────────────────────────────────────────────────────────────

def get_bedrock_client():
    """Cliente para invocar el modelo (generación de texto)."""
    return boto3.client(
        "bedrock-runtime",
        region_name=REGION,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN")
    )

def get_bedrock_agent_client():
    """Cliente para consultar la Knowledge Base (RAG)."""
    return boto3.client(
        "bedrock-agent-runtime",
        region_name=REGION,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN")
    )

# ── RAG: consulta a la Knowledge Base de Bedrock ─────────────────────────────

def recuperar_contexto_kb(incidencia: str, num_resultados: int = 5) -> str:
    """
    Consulta la Knowledge Base de AWS Bedrock con el texto de la incidencia.
    Devuelve los fragmentos más relevantes del Manual de Procedimientos
    como un string listo para incluir en el prompt.

    Usa búsqueda semántica por embeddings (Amazon Titan Embeddings V2).
    """
    if not KNOWLEDGE_BASE_ID:
        raise ValueError(
            "KNOWLEDGE_BASE_ID no configurado. "
            "Configura la variable de entorno con el ID de la Knowledge Base de Bedrock."
        )

    client = get_bedrock_agent_client()

    response = client.retrieve(
        knowledgeBaseId=KNOWLEDGE_BASE_ID,
        retrievalQuery={"text": incidencia},
        retrievalConfiguration={
            "vectorSearchConfiguration": {
                "numberOfResults": num_resultados
            }
        }
    )

    fragmentos = []
    for resultado in response.get("retrievalResults", []):
        texto = resultado.get("content", {}).get("text", "")
        score = resultado.get("score", 0)
        if texto:
            fragmentos.append(f"[Relevancia: {score:.2f}]\n{texto}")

    if not fragmentos:
        return "No se encontraron fragmentos relevantes en el manual."

    return "\n\n---\n\n".join(fragmentos)

# ── Prompt ───────────────────────────────────────────────────────────────────

PROMPT_SISTEMA = """Eres un asistente experto en soporte técnico IT de un centro educativo.
Tu tarea es analizar incidencias técnicas y devolver SIEMPRE una respuesta en formato JSON válido,
sin texto adicional antes ni después del JSON.

El JSON debe seguir EXACTAMENTE esta estructura:
{
  "clasificacion": {
    "categoria": "<Hardware | Software | Redes>",
    "urgencia": "<Baja | Media | Alta | Crítica>"
  },
  "hoja_de_ruta": [
    "Paso 1: ...",
    "Paso 2: ...",
    "Paso 3: ..."
  ],
  "correo_respuesta": "Texto completo del correo para enviar al usuario."
}

Basa tu respuesta en el Manual de Procedimientos proporcionado.
Si la incidencia no está cubierta por el manual, usa tu criterio técnico
e indícalo explícitamente en la hoja de ruta."""


def construir_prompt(incidencia: str, contexto_manual: str) -> str:
    return f"""A continuación tienes fragmentos relevantes del Manual de Procedimientos IT del centro,
recuperados mediante búsqueda semántica sobre la Knowledge Base de AWS Bedrock:

=== MANUAL DE PROCEDIMIENTOS (fragmentos relevantes) ===
{contexto_manual}
=== FIN DEL MANUAL ===

La incidencia reportada es:
"{incidencia}"

Analiza la incidencia usando el manual y devuelve el JSON estructurado."""

# ── Llamada al modelo ─────────────────────────────────────────────────────────

def procesar_incidencia(incidencia: str) -> dict:
    """
    Función principal del backend.

    Flujo:
      1. Consulta la Knowledge Base de Bedrock (RAG con embeddings)
      2. Construye el prompt con el contexto recuperado
      3. Llama al modelo en Bedrock
      4. Parsea y devuelve el JSON de respuesta

    Retorna un dict con clasificacion, hoja_de_ruta y correo_respuesta.
    En caso de error, retorna un dict con clave 'error'.
    """
    texto_respuesta = ""
    try:
        # Paso 1: RAG — recuperar contexto del manual desde la Knowledge Base
        contexto = recuperar_contexto_kb(incidencia)

        # Paso 2: construir el prompt
        prompt_usuario = construir_prompt(incidencia, contexto)

        # Paso 3: llamar al modelo
        client = get_bedrock_client()

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1500,
            "system": PROMPT_SISTEMA,
            "messages": [
                {"role": "user", "content": prompt_usuario}
            ]
        }

        response = client.invoke_model(
            modelId=MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body)
        )

        # Paso 4: parsear la respuesta
        response_body = json.loads(response["body"].read())
        texto_respuesta = response_body["content"][0]["text"].strip()

        # Limpiar posibles bloques de código markdown
        if texto_respuesta.startswith("```"):
            texto_respuesta = texto_respuesta.split("```")[1]
            if texto_respuesta.startswith("json"):
                texto_respuesta = texto_respuesta[4:]

        return json.loads(texto_respuesta)

    except json.JSONDecodeError as e:
        return {
            "error": f"Error al parsear la respuesta JSON del modelo: {e}",
            "respuesta_raw": texto_respuesta
        }
    except Exception as e:
        return {"error": f"Error inesperado: {e}"}