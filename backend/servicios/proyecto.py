from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.modelos.proyecto import Proyecto
from backend.modelos.actividad import Actividad
from backend.esquemas.proyecto import ProyectoCrear, ProyectoActualizar


def crear_proyecto(
    datos_proyecto: ProyectoCrear,
    session: Session
) -> Proyecto:
    nuevo_proyecto = Proyecto(
        nombre=datos_proyecto.nombre,
        descripcion=datos_proyecto.descripcion
    )

    session.add(nuevo_proyecto)
    session.commit()
    session.refresh(nuevo_proyecto)

    return nuevo_proyecto


def listar_proyectos(session: Session) -> list[Proyecto]:
    consulta = select(Proyecto)
    return list(session.scalars(consulta).all())


def obtener_proyecto(
    id_proyecto: int,
    session: Session
) -> Proyecto | None:
    consulta = select(Proyecto).where(Proyecto.id == id_proyecto)
    return session.scalar(consulta)


def obtener_detalle_proyecto(
    id_proyecto: int,
    session: Session
):
    proyecto = obtener_proyecto(id_proyecto, session)

    if proyecto is None:
        return None

    consulta = select(Actividad).where(Actividad.proyecto_id == id_proyecto)
    actividades = list(session.scalars(consulta).all())

    return {
        "id": proyecto.id,
        "nombre": proyecto.nombre,
        "descripcion": proyecto.descripcion,
        "actividades": actividades
    }


def actualizar_proyecto(
    id_proyecto: int,
    datos_proyecto: ProyectoActualizar,
    session: Session
) -> Proyecto | None:
    proyecto = obtener_proyecto(id_proyecto, session)

    if proyecto is None:
        return None

    proyecto.nombre = datos_proyecto.nombre
    proyecto.descripcion = datos_proyecto.descripcion

    session.commit()
    session.refresh(proyecto)

    return proyecto


def eliminar_proyecto(
    id_proyecto: int,
    session: Session
) -> bool:
    proyecto = obtener_proyecto(id_proyecto, session)

    if proyecto is None:
        return False

    session.delete(proyecto)
    session.commit()

    return True