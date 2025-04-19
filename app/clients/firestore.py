from google.cloud import firestore
from app.config import settings

project_id = settings.GCP_PROJECT_ID
database_id = settings.FIRESTORE_DATABASE_ID

if not project_id:
    raise ValueError("GCP_PROJECT_ID is not configured")

if not database_id:
    raise ValueError("FIRESTORE_DATABASE_ID is not configured")

client = firestore.Client(project=project_id, database=database_id)

def get_firestore_client():
    return client
