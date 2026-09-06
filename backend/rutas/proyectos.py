from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.base_de_datos import get_db_session
from backend.esquemas.proyecto import ProyectoCrear, ProyectoRespuesta, ProyectoActualizar
from backend.servicios.proyecto import (
    actualizar_proyecto,
    crear_proyecto,
    eliminar_proyecto,
    listar_proyectos,
    obtener_proyecto,
)

router = APIRouter()


@router.post(
    "/proyectos",
    response_model=ProyectoRespuesta,
    status_code=status.HTTP_201_CREATED
)
def registrar_proyecto(
    datos_proyecto: ProyectoCrear,
    session: Session = Depends(get_db_session)
):
    return crear_proyecto(datos_proyecto, session)


@router.get(
    "/proyectos",
    response_model=list[ProyectoRespuesta]
)
def obtener_proyectos(
    session: Session = Depends(get_db_session)
):
    return listar_proyectos(session)


@router.get(
    "/proyectos/{id_proyecto}",
    response_model=ProyectoRespuesta
)
def obtener_proyecto_por_id(
    id_proyecto: int,
    session: Session = Depends(get_db_session)
):
    proyecto = obtener_proyecto(id_proyecto, session)

    if proyecto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    return proyecto


@router.put(
    "/proyectos/{id_proyecto}",
    response_model=ProyectoRespuesta
)
def editar_proyecto(
    id_proyecto: int,
    datos_proyecto: ProyectoActualizar,
    session: Session = Depends(get_db_session)
):
    proyecto = actualizar_proyecto(
        id_proyecto,
        datos_proyecto,
        session
    )

    if proyecto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    return proyecto


@router.delete(
    "/proyectos/{id_proyecto}",
    status_code=status.HTTP_204_NO_CONTENT
)
def borrar_proyecto(
    id_proyecto: int,
    session: Session = Depends(get_db_session)
):
    proyecto_eliminado = eliminar_proyecto(id_proyecto, session)

    if not proyecto_eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )