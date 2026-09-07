from fastapi import FastAPI
from backend.rutas.proyectos import router as router_proyectos
from backend.rutas.actividades import router as router_actividades



aplicacion = FastAPI()
aplicacion.include_router(router_proyectos, prefix="/api")
aplicacion.include_router(router_actividades, prefix="/api")

@aplicacion.get("/")
def inicio():
    return {"mensaje": "API EVM funcionando"}
