from fastapi import FastAPI
from backend.rutas.proyectos import router

aplicacion = FastAPI()
aplicacion.include_router(router, prefix="/api")

@aplicacion.get("/")
def inicio():
    return {"mensaje": "API EVM funcionando"}
