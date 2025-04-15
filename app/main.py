from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO: Cambiar a la URL de tu frontend, para mejorar la seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#Endpoint básico "Hello wold"
@app.get("/")
def hello_world():
    return {"message": "Hello World AGAIN!"}
