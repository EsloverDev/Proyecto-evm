from pydantic import BaseModel, Field, ConfigDict


class ActividadCrear(BaseModel):
    nombre: str = Field(max_length=150)
    bac: float = Field(ge=0)
    porcentaje_planificado: float = Field(ge=0, le=100)
    porcentaje_completado: float = Field(ge=0, le=100)
    costo_real: float = Field(ge=0)


class ActividadActualizar(BaseModel):
    nombre: str = Field(max_length=150)
    bac: float = Field(ge=0)
    porcentaje_planificado: float = Field(ge=0, le=100)
    porcentaje_completado: float = Field(ge=0, le=100)
    costo_real: float = Field(ge=0)


class ActividadRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    proyecto_id: int
    nombre: str
    bac: float
    porcentaje_planificado: float
    porcentaje_completado: float
    costo_real: float