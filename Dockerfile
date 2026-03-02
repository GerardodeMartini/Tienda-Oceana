# Usar imagen base oficial de Python (Bookworm es la versión estable actual de Debian)
FROM python:3.10-slim-bookworm

# Establecer directorio de trabajo
WORKDIR /app

# Establecer variables de entorno
# PYTHONDONTWRITEBYTECODE: Previene que Python escriba archivos pyc
# PYTHONUNBUFFERED: Asegura que la salida de Python se envíe directamente al terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema
# build-essential: para compilar ciertos paquetes de Python
# libpango-1.0-0, libcairo2, libgdk-pixbuf2.0-0: bibliotecas gráficas (útiles para Pillow/WeasyPrint si se usan)
# git: útil si alguna dependencia viene de git
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar requerimientos e instalarlos
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar el código del proyecto
COPY . /app/

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

# Exponer el puerto
EXPOSE 8000

# Comando para correr la aplicación usando Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120", "--workers", "3"]
