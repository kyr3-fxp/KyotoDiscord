# Usar imagen base ligera oficial de Python 3.11
FROM python:3.11-slim

# Evitar la creación de archivos .pyc y forzar buffer de salida para logs inmediatos
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema mínimas requeridas si fuera necesario
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copiar primero requirements para aprovechar la caché de capas de Docker
COPY requirements.txt .

# Instalar dependencias de Python sin cache para reducir tamaño de imagen
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente del bot
COPY . .

# Comando de ejecución por defecto
CMD ["python", "main.py"]
