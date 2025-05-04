from fastapi import APIRouter, HTTPException
from app.schemas.note import Note, CreateNote
from app.clients.firestore import get_firestore_client
from typing import Dict, List
from google.cloud import firestore

# Instancia una clase Router para manejar las rutas de las notas
router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("", status_code=200)
async def get_notes() -> Dict[str, List[Note]]:
    db = get_firestore_client()
    collection_ref = db.collection("notes").order_by("updated_at", direction=firestore.Query.DESCENDING)

    notes = []

    docs = collection_ref.stream()
    for doc in docs:
        note_data = doc.to_dict()
        # Convertir Firestore Timestamp a string en ISO format
        note_data["created_at"] = note_data["created_at"].isoformat()
        note_data["updated_at"] = note_data["updated_at"].isoformat()
        notes.append(note_data)

    return { "notes": notes }

@router.post("", status_code=201)
async def create_note(note_data: CreateNote) -> Dict[str, Note]:
    db = get_firestore_client()
    collection_ref = db.collection("notes")

    doc_ref = collection_ref.document()
    now = firestore.SERVER_TIMESTAMP

    new_note = {
        "id": doc_ref.id,
        "title": note_data.title,
        "content": note_data.content,
        "created_at": now,
        "updated_at": now
    }

    doc_ref.set(new_note)

    doc = doc_ref.get()
    note_stored = doc.to_dict()

    return {
        "note": {
            "id": note_stored["id"],
            "title": note_stored["title"],
            "content": note_stored["content"],
            "created_at": note_stored["created_at"].isoformat(),
            "updated_at": note_stored["updated_at"].isoformat(),
        }
    }
