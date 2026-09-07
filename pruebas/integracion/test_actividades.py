from fastapi import status


def test_crear_actividad(cliente):
    datos_actividad = {
        "nombre": "Actividad de prueba",
        "bac": 1000.0,
        "porcentaje_planificado": 50.0,
        "porcentaje_completado": 25.0,
        "costo_real": 500.0
    }
    respuesta = cliente.post(
        "/api/proyectos/1/actividades",
        json=datos_actividad
    )

    assert respuesta.status_code == status.HTTP_201_CREATED

    actividad_creada = respuesta.json()

    assert "id" in actividad_creada
    assert actividad_creada["proyecto_id"] == 1
    assert actividad_creada["nombre"] == datos_actividad["nombre"]
    assert actividad_creada["bac"] == datos_actividad["bac"]
    assert actividad_creada["porcentaje_planificado"] == datos_actividad["porcentaje_planificado"]
    assert actividad_creada["porcentaje_completado"] == datos_actividad["porcentaje_completado"]
    assert actividad_creada["costo_real"] == datos_actividad["costo_real"]


def test_crear_actividad_proyecto_inexistente(cliente):
    datos_actividad = {
        "nombre": "Actividad de prueba",
        "bac": 1000.0,
        "porcentaje_planificado": 50.0,
        "porcentaje_completado": 25.0,
        "costo_real": 500.0
    }
    respuesta = cliente.post(
        "/api/proyectos/999/actividades",
        json=datos_actividad
    )

    assert respuesta.status_code == status.HTTP_404_NOT_FOUND
    assert respuesta.json()["detail"] == "Proyecto no encontrado"


def test_listar_actividades(cliente):
    datos_actividad = {
            "nombre": "Actividad de prueba",
            "bac": 1000.0,
            "porcentaje_planificado": 50.0,
            "porcentaje_completado": 25.0,
            "costo_real": 500.0
        }
    cliente.post(
        "/api/proyectos/1/actividades",
        json=datos_actividad
    )

    respuesta = cliente.get("/api/proyectos/1/actividades")

    assert respuesta.status_code == status.HTTP_200_OK

    actividades = respuesta.json()

    assert isinstance(actividades, list)
    assert any(
        actividad["nombre"] == datos_actividad["nombre"]
        for actividad in actividades
    )

    actividad = actividades[0]

    assert "id" in actividad
    assert "proyecto_id" in actividad
    assert "nombre" in actividad
    assert "bac" in actividad
    assert "porcentaje_planificado" in actividad
    assert "porcentaje_completado" in actividad
    assert "costo_real" in actividad


def test_listar_actividades_proyecto_inexistente(cliente):
    respuesta = cliente.get("/api/proyectos/999/actividades")

    assert respuesta.status_code == status.HTTP_404_NOT_FOUND
    assert respuesta.json()["detail"] == "Proyecto no encontrado"


def test_actualizar_actividad_existente(cliente):
    datos_actividad = {
                "nombre": "Actividad de prueba",
                "bac": 1000.0,
                "porcentaje_planificado": 50.0,
                "porcentaje_completado": 25.0,
                "costo_real": 500.0
            }
    respuesta_creacion = cliente.post(
        "/api/proyectos/1/actividades",
        json=datos_actividad
    )

    id_actividad = respuesta_creacion.json()["id"]

    datos_actualizacion = {
        "nombre": "Actividad actualizada",
        "bac": 1200.0,
        "porcentaje_planificado": 60.0,
        "porcentaje_completado": 30.0,
        "costo_real": 600.0
    }
    respuesta = cliente.put(
        f"/api/actividades/{id_actividad}",
        json=datos_actualizacion
    )

    assert respuesta.status_code == status.HTTP_200_OK

    actividad_actualizada = respuesta.json()

    assert actividad_actualizada["id"] == id_actividad
    assert actividad_actualizada["proyecto_id"] == 1
    assert actividad_actualizada["nombre"] == datos_actualizacion["nombre"]
    assert actividad_actualizada["bac"] == datos_actualizacion["bac"]
    assert actividad_actualizada["porcentaje_planificado"] == datos_actualizacion["porcentaje_planificado"]
    assert actividad_actualizada["porcentaje_completado"] == datos_actualizacion["porcentaje_completado"]
    assert actividad_actualizada["costo_real"] == datos_actualizacion["costo_real"]


def test_actualizar_actividad_inexistente(cliente):
    datos_actualizacion = {
        "nombre": "Actividad inexistente",
        "bac": 1500.0,
        "porcentaje_planificado": 70.0,
        "porcentaje_completado": 40.0,
        "costo_real": 700.0
    }
    respuesta = cliente.put(
        "/api/actividades/999",
        json=datos_actualizacion
    )

    assert respuesta.status_code == status.HTTP_404_NOT_FOUND
    assert respuesta.json()["detail"] == "Actividad no encontrada"

def test_eliminar_actividad_existente(cliente):
    datos_actividad = {
                "nombre": "Actividad de prueba",
                "bac": 1000.0,
                "porcentaje_planificado": 50.0,
                "porcentaje_completado": 25.0,
                "costo_real": 500.0
            }
    respuesta_creacion = cliente.post(
        "/api/proyectos/1/actividades",
        json=datos_actividad
    )

    id_actividad = respuesta_creacion.json()["id"]

    respuesta = cliente.delete(f"/api/actividades/{id_actividad}")

    assert respuesta.status_code == status.HTTP_204_NO_CONTENT
    assert respuesta.content == b""


def test_eliminar_actividad_inexistente(cliente):
    respuesta = cliente.delete("/api/actividades/999")

    assert respuesta.status_code == status.HTTP_404_NOT_FOUND
    assert respuesta.json()["detail"] == "Actividad no encontrada"