# Usamos como base una imagen ligera de python 3.10
FROM python:3.10-slim

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y gcc && apt-get clean

# Crea (si no existe) y se mueve al directorio /app dentro del contenedor
WORKDIR /app

# Copia TODO el proyecto en el contenedor
COPY . .

# Apuntar a la ruta donde quedo el archivo .JSON (LA LINEA DE ABAJO SOLO SE UTILIZA EN LOCAL DEVELOPMENT CON DOCKER)
# ENV GOOGLE_APPLICATION_CREDENTIALS=/app/sensitive/service-account.json

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# La aplicacion expone (va a esuchar) el puerto 8080
EXPOSE 8080

# Comando para ejecutar la aplicacion uvicorn
CMD ["uvicorn", "app.main:app", "--workers", "1", "--timeout-keep-alive", "0", "--host", "0.0.0.0", "--port", "8080"]
