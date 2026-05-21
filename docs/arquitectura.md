# Documentación Técnica: Arquitectura del Sistema

## Flujo de datos completo

```
[Usuario] → introduce texto de incidencia
    │
    ▼
[Streamlit - app.py]
    │  Recibe el texto
    ▼
[backend_aws.py]
    │  Consulta la Knowledge Base de AWS Bedrock
    │  con el texto de la incidencia
    ▼
[AWS Bedrock Knowledge Base (RAG)]
    │  Búsqueda semántica por embeddings
    │  sobre el Manual de Procedimientos (S3)
    │  Devuelve fragmentos relevantes
    ▼
[backend_aws.py]
    │  Construye el prompt enriquecido con:
    │    - Texto de la incidencia
    │    - Fragmentos relevantes del manual
    │    - Instrucciones de formato JSON
    ▼
[AWS Bedrock — Claude Haiku 4.5]
    │  Procesa el prompt
    │  Devuelve JSON estructurado
    ▼
[backend_aws.py]
    │  Parsea el JSON de respuesta
    ▼
[Streamlit - app.py]
    │  Muestra al usuario:
    ├── Clasificación: categoría + urgencia
    ├── Hoja de ruta para el técnico
    └── Correo automático redactado
```

## Componentes

| Archivo | Responsabilidad |
|---|---|
| `src/app.py` | Interfaz Streamlit, entrada/salida de datos |
| `src/backend_aws.py` | Conexión boto3 con Bedrock, consulta a la Knowledge Base, construcción del prompt, parseo del JSON |
| `data/manual_procedimientos.pdf` | Base de conocimiento subida a S3 e indexada en la Knowledge Base |

## Infraestructura AWS

| Servicio | Uso |
|---|---|
| AWS Bedrock | Invocación del modelo de lenguaje |
| AWS Bedrock Knowledge Bases | RAG: búsqueda semántica sobre el manual |
| Amazon S3 | Almacenamiento del PDF del manual |
| Amazon Titan Embeddings V2 | Generación de embeddings para indexar el manual |

## Modelo utilizado

- **Proveedor:** AWS Bedrock
- **Modelo:** Claude Haiku 4.5 (`eu.anthropic.claude-haiku-4-5-20251001-v1:0`)
- **Región:** eu-south-2 (Europa — España)
- **Motivo:** Velocidad de respuesta, coste reducido, y capacidad suficiente para clasificación y generación de texto estructurado

## Formato de respuesta esperado (JSON)

```json
{
  "clasificacion": {
    "categoria": "Hardware",
    "urgencia": "Alta"
  },
  "hoja_de_ruta": [
    "Paso 1: ...",
    "Paso 2: ...",
    "Paso 3: ..."
  ],
  "correo_respuesta": "Estimado usuario, ..."
}
```