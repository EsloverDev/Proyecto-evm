from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.base_de_datos import get_db_session
from backend.esquemas.actividad import ActividadCrear, ActividadRespuesta, ActividadActualizar
from backend.servicios.actividad import crear_actividad, listar_actividades, actualizar_actividad, eliminar_actividad


router = APIRouter()

@router.post(
    "/proyectos/{id_proyecto}/actividades",
    response_model=ActividadRespuesta,
    status_code=status.HTTP_201_CREATED
)
def registrar_actividad(
    id_proyecto: int,
    datos_actividad: ActividadCrear,
    session: Session = Depends(get_db_session)
):
    actividad = crear_actividad(id_proyecto, datos_actividad, session)

    if actividad is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    return actividad


@router.get(
    "/proyectos/{id_proyecto}/actividades",
    response_model=list[ActividadRespuesta]
)
def obtener_actividades(
    id_proyecto: int,
    session: Session = Depends(get_db_session)
):
    actividades = listar_actividades(id_proyecto, session)

    if actividades is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    return actividades


@router.put(
    "/actividades/{id_actividad}",
    response_model=ActividadRespuesta
)
def editar_actividad(
    id_actividad: int,
    datos_actividad: ActividadActualizar,
    session: Session = Depends(get_db_session)
):
    actividad = actualizar_actividad(id_actividad, datos_actividad, session)

    if actividad is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada"
        )
    return actividad


@router.delete(
    "/actividades/{id_actividad}",
    status_code=status.HTTP_204_NO_CONTENT
)
def borrar_actividad(
    id_actividad: int,
    session: Session = Depends(get_db_session)
):
    actividad_eliminada = eliminar_actividad(id_actividad, session)

    if not actividad_eliminada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada"
        )