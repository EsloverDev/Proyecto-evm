from pydantic import BaseModel, ConfigDict, Field
from backend.esquemas.actividad import ActividadRespuesta


class ProyectoCrear(BaseModel):
    nombre: str = Field(max_length=150)
    descripcion: str | None = None


class ProyectoActualizar(BaseModel):
    nombre: str = Field(max_length=150)
    descripcion: str | None = None


class ProyectoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    descripcion: str | None
    actividades: list[ActividadRespuesta] = Field(default_factory=list)
