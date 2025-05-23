from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.notes.endpoints import router as notes_router

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://notes-frontend-service-846045290007.us-central1.run.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(notes_router)

#Endpoint básico "Hello wold"
@app.get("/")
def hello_world():
    return {"message": "Hello World AGAIN!"}

