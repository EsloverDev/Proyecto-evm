from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.modelos.actividad import Actividad
from backend.esquemas.actividad import ActividadCrear, ActividadActualizar
from backend.servicios.proyecto import obtener_proyecto


def crear_actividad(
    id_proyecto: int,
    datos_actividad: ActividadCrear,
    session: Session
) -> Actividad | None:
    proyecto = obtener_proyecto(id_proyecto, session)

    if proyecto is None:
        return None

    nueva_actividad = Actividad(
        proyecto_id=id_proyecto,
        nombre=datos_actividad.nombre,
        bac=datos_actividad.bac,
        porcentaje_planificado=datos_actividad.porcentaje_planificado,
        porcentaje_completado=datos_actividad.porcentaje_completado,
        costo_real=datos_actividad.costo_real
    )

    session.add(nueva_actividad)
    session.commit()
    session.refresh(nueva_actividad)

    return nueva_actividad


def listar_actividades(
        id_proyecto: int,
        session: Session
) -> list[Actividad] | None:
    proyecto = obtener_proyecto(id_proyecto, session)

    if proyecto is None:
        return None

    consulta = select(Actividad).where(Actividad.proyecto_id == id_proyecto)
    return list(session.scalars(consulta).all())


def actualizar_actividad(
    id_actividad: int,
    datos_actividad: ActividadActualizar,
    session: Session
) -> Actividad | None:
    consulta = select(Actividad).where(Actividad.id == id_actividad)
    actividad = session.scalar(consulta)

    if actividad is None:
        return None

    actividad.nombre = datos_actividad.nombre
    actividad.bac = datos_actividad.bac
    actividad.porcentaje_planificado = datos_actividad.porcentaje_planificado
    actividad.porcentaje_completado = datos_actividad.porcentaje_completado
    actividad.costo_real = datos_actividad.costo_real

    session.commit()
    session.refresh(actividad)

    return actividad


def eliminar_actividad(
    id_actividad: int,
    session: Session
) -> bool:
    consulta = select(Actividad).where(Actividad.id == id_actividad)
    actividad = session.scalar(consulta)

    if actividad is None:
        return False

    session.delete(actividad)
    session.commit()

    return True