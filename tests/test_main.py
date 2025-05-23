import os

# Setear variables de entorno al inicio del test
os.environ["APP_ENV"] = "test"
os.environ["GCP_PROJECT_ID"] = "test-project"
os.environ["FIRESTORE_DATABASE_ID"] = "test-db"
os.environ["GEMINI_GOOGLE_API_KEY"] = "test-gemini"

import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from mockfirestore import MockFirestore
from app.main import app
from app.clients.firestore import get_firestore_client

client = TestClient(app)

# Mockear firestore.SERVER_TIMESTAMP para evitar errores cripticos en los tests
@pytest.fixture(autouse=True)
def mock_server_timestamp(mocker):
    mocker.patch("google.cloud.firestore.SERVER_TIMESTAMP", new=datetime.now())

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == { "message": "Hello World AGAIN!" }


def test_get_notes():
    db = get_firestore_client()
    db.reset()
    db.collection("notes").document("noteId1").set({
        "id": "noteId1",
        "title": "Primera nota",
        "content": "Contenido de la primera nota",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    })
    db.collection("notes").document("noteId2").set({
        "id": "noteId2",
        "title": "Segunda nota",
        "content": "Contenido de la segunda nota",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    })

    response = client.get("/notes")
    assert response.status_code == 200
    notes = response.json()["notes"]
    assert len(notes) == 2

    for note in notes:
        if note["id"] == "noteId1":
            assert note["title"] == "Primera nota"
            assert note["content"] == "Contenido de la primera nota"
        else:
            assert note["title"] == "Segunda nota"
            assert note["content"] == "Contenido de la segunda nota"


def test_create_note():
    db = get_firestore_client()
    db.reset()

    payload = { "title": "Nueva nota", "content": "Nueva nota con contenido" }
    response = client.post("/notes", json=payload)

    #verificando respuesta
    assert response.status_code == 201
    note = response.json()["note"]
    assert note["title"] == "Nueva nota"
    assert note["content"] == "Nueva nota con contenido"
    assert "id" in note

    #verificar base de datos
    doc = db.collection("notes").document(note["id"]).get()
    assert doc.exists
    doc_saved = doc.to_dict()
    assert doc_saved["title"] == "Nueva nota"
    assert doc_saved["content"] == "Nueva nota con contenido"

def test_get_note_by_id():
    db = get_firestore_client()
    db.reset()
    db.collection("notes").document("abc123").set({
        "id": "abc123",
        "title": "Mi nota",
        "content": "Mi contenido",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    })
    response = client.get("/notes/abc123")
    assert response.status_code == 200
    assert response.json()["note"]["id"] == "abc123"
    assert response.json()["note"]["title"] == "Mi nota"
    assert response.json()["note"]["content"] == "Mi contenido"


def test_patch_note():
    db = get_firestore_client()
    db.reset()

    note_id = "patch123"
    db.collection("notes").document(note_id).set({
        "id": "patch123",
        "title": "titulo original",
        "content": "contenido original",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    })

    payload = { "title": "Titulo Actualizado" }
    response = client.patch(f"/notes/{note_id}", json=payload)
    assert response.status_code == 200

    updated_note = response.json()["note"]
    assert updated_note["id"] == note_id
    assert updated_note["title"] == "Titulo Actualizado"
    assert updated_note["content"] == "contenido original"

    # Verificar base de datos
    doc = db.collection("notes").document(note_id).get()
    assert doc.exists
    saved_note = doc.to_dict()
    assert saved_note["title"] == "Titulo Actualizado"
    assert saved_note["content"] == "contenido original"

def test_delete_note():
   db = get_firestore_client()
   db.reset()

   note_id = "xyz789"
   db.collection("notes").document(note_id).set({
       "id": note_id,
       "title": "Nota a Eliminar",
       "content": "Contenido de la nota a eliminar",
       "created_at": datetime.now(),
       "updated_at": datetime.now()
   })
   response = client.delete(f"/notes/{note_id}")
   assert response.status_code == 200
   assert response.json()["message"] == f"Note with ID {note_id} deleted"

   #Confirmamos en la base de datos
   doc = db.collection("notes").document(note_id).get()
   assert not doc.exists

