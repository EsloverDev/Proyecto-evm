from fastapi import FastAPI

aplicacion = FastAPI()

@aplicacion.get("/")
def inicio():
    return {"mensaje": "API EVM funcionando"}
