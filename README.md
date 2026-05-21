# 🖥️ Asistente Inteligente de Soporte Técnico IT
### Especialización IA + Big Data — AWS Bedrock

> Aplicación web que automatiza la clasificación, diagnóstico y respuesta de incidencias técnicas mediante IA Generativa y un sistema RAG sobre AWS Bedrock Knowledge Bases.

---

## 📋 Descripción del Proyecto

El sistema recibe el texto de una incidencia técnica y devuelve automáticamente:

1. **Clasificación** — categoría (Hardware, Software, Redes) y nivel de urgencia (Baja, Media, Alta, Crítica)
2. **Hoja de ruta** — pasos exactos para el técnico, extraídos del Manual de Procedimientos interno
3. **Correo automático** — respuesta formal ya redactada para enviar al usuario

La IA no inventa las soluciones: las extrae del manual oficial del centro gracias al sistema RAG, que indexa el documento en AWS Bedrock Knowledge Bases con embeddings y búsqueda semántica.

---

## 🏗️ Arquitectura del Sistema

```
Usuario / Técnico
      │
      ▼
 Interfaz Web (Streamlit — src/app.py)
      │
      ▼
 backend_aws.py  ──► AWS Bedrock Knowledge Base (RAG)
                          │
                     S3: manual_procedimientos.pdf
                     Embeddings: Amazon Titan Embeddings V2
      │
      ▼
 AWS Bedrock — Claude Haiku 4.5
      │
      ▼
 JSON estructurado
      │
      ├── Clasificación + Urgencia
      ├── Hoja de Ruta Técnica
      └── Correo Automático al Usuario
```

---

## 📁 Estructura del Repositorio

```
Soporte-IT-IA/
│
├── src/
│   ├── backend_aws.py       # Conexión con AWS Bedrock + Knowledge Base (RAG)
│   └── app.py               # Interfaz web con Streamlit
│
├── data/
│   └── manual_procedimientos.pdf   # Base de conocimiento (Manual IT)
│
├── docs/
│   ├── arquitectura.md      # Documentación técnica del flujo de datos
│   └── reflexion_critica.md # Reflexión sobre limitaciones de la IA
│
├── Dockerfile               # Contenedor Docker del proyecto
├── docker-compose.yml       # Configuración Docker Compose
├── requirements.txt         # Dependencias Python
├── .gitignore               # Archivos excluidos del repositorio
└── README.md                # Este archivo
```

---

## 🚀 Instalación y Ejecución

### Prerrequisitos

- Cuenta AWS con acceso a Bedrock habilitado en `eu-south-2`
- Knowledge Base configurada en Bedrock con el manual subido a S3
- Python 3.11+

### Ejecución Local

**1. Clonar el repositorio**
```bash
git clone https://github.com/perezrodriguezpedro/Soporte-IT-IA.git
cd Soporte-IT-IA
```

**2. Crear entorno virtual e instalar dependencias**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

pip install -r requirements.txt
```

**3. Configurar credenciales AWS**

Crear un archivo `.env` en la raíz del proyecto con:

```env
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_SESSION_TOKEN=tu_session_token
AWS_DEFAULT_REGION=eu-south-2
BEDROCK_MODEL_ID=arn:aws:bedrock:eu-south-2:CUENTA:inference-profile/eu.anthropic.claude-haiku-4-5-20251001-v1:0
KNOWLEDGE_BASE_ID=tu_knowledge_base_id
```

> ⚠️ Las credenciales SSO son temporales. Obtenerlas desde el portal: https://gva-cons.awsapps.com/start/

**4. Lanzar la aplicación**
```bash
streamlit run src/app.py
```

Acceder en: `http://localhost:8501`

---

### Ejecución con Docker

```bash
docker-compose up
```

Acceder en: `http://localhost:8501`

---

## ⚙️ Configuración AWS

### 1. Habilitar modelos en Bedrock

En la consola AWS → Amazon Bedrock → Catálogo de modelos (`eu-south-2`), habilitar:
- **Claude Haiku 4.5** (Anthropic) — modelo principal
- **Amazon Titan Embeddings V2** — para indexar la Knowledge Base

### 2. Crear el bucket S3 y subir el manual

En la consola AWS → S3 → Create bucket:
- Nombre: `soporte-it-ia-kb`
- Región: `eu-south-2`

Subir `data/manual_procedimientos.pdf` al bucket.

### 3. Crear la Knowledge Base en Bedrock

En la consola AWS → Bedrock → Knowledge Bases → Create:
- **Nombre:** `soporte-it-kb`
- **Fuente de datos:** S3 → bucket `soporte-it-ia-kb`
- **Modelo de embeddings:** Amazon Titan Embeddings V2
- Copiar el **Knowledge Base ID** generado y añadirlo al `.env`

---

## 🧠 Tecnologías Utilizadas

| Componente | Tecnología |
|---|---|
| IA Generativa | AWS Bedrock (Claude Haiku 4.5) |
| RAG / Base de conocimiento | AWS Bedrock Knowledge Bases |
| Embeddings | Amazon Titan Embeddings V2 |
| Almacenamiento del manual | Amazon S3 |
| Backend Python | boto3, python-dotenv |
| Interfaz Web | Streamlit |
| Contenedor | Docker |

---

## ⚠️ Limitaciones y Reflexión Crítica

Ver [`docs/reflexion_critica.md`](docs/reflexion_critica.md) para el análisis completo sobre alucinaciones, privacidad, sesgos y necesidad de supervisión humana.

---

## 👥 Autores

Proyecto desarrollado en el marco de la **Especialización IA + Big Data** con AWS Bedrock — IES La Mar.

| Miembro | Rol |
|---|---|
| Pedro | Manual de Procedimientos · Backend AWS · Docker · Arquitectura |
| Borja | Configuración AWS (S3 + Knowledge Base) · Interfaz Streamlit · Integración · Reflexión crítica |

---

## 📄 Licencia

Proyecto académico — uso educativo.