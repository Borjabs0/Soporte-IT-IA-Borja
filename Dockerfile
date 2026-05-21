FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente y los datos
COPY src/ ./src/
COPY data/ ./data/

# Exponer el puerto de Streamlit
EXPOSE 8501

# Variables de entorno por defecto (se sobreescriben con --env-file)
ENV AWS_DEFAULT_REGION=us-east-1

# Comando de arranque
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
