import os
from dotenv import load_dotenv

# SETUP-LOCAL: Para cargar las variables de entorno desde el archivo .env.local descomentar la siguiente linea
# load_dotenv(".env.local")

class Settings:
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID")
    FIRESTORE_DATABASE_ID: str = os.getenv("FIRESTORE_DATABASE_ID")

settings = Settings()
