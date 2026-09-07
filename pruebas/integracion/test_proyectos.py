from fastapi import status


def test_crear_proyecto(cliente):
    datos_proyecto = {
        "nombre": "Proyecto de integración",
        "descripcion": "Proyecto creado mediante una prueba de integración"
    }

    respuesta = cliente.post(
        "/api/proyectos",
        json=datos_proyecto
    )

    assert respuesta.status_code == status.HTTP_201_CREATED

    proyecto_creado = respuesta.json()

    assert "id" in proyecto_creado
    assert proyecto_creado["nombre"] == datos_proyecto["nombre"]
    assert proyecto_creado["descripcion"] == datos_proyecto["descripcion"]


def test_listar_proyectos(cliente):
    respuesta = cliente.get("/api/proyectos")

    assert respuesta.status_code == status.HTTP_200_OK

    proyectos = respuesta.json()

    assert isinstance(proyectos, list)
    assert len(proyectos) >= 1

    proyecto = proyectos[0]

    assert "id" in proyecto
    assert "nombre" in proyecto
    assert "descripcion" in proyecto


def test_obtener_proyecto_existente(cliente):
    datos_proyecto = {
        "nombre": "Proyecto de integración",
        "descripcion": "Proyecto creado mediante una prueba de integración"
    }

    respuesta_creacion = cliente.post(
        "/api/proyectos",
        json=datos_proyecto
    )

    id_proyecto = respuesta_creacion.json()["id"]

    respuesta = cliente.get(f"/api/proyectos/{id_proyecto}")

    assert respuesta.status_code == status.HTTP_200_OK

    proyecto = respuesta.json()

    assert proyecto["id"] == id_proyecto
    assert proyecto["nombre"] == datos_proyecto["nombre"]
    assert proyecto["descripcion"] == datos_proyecto["descripcion"]
    assert "actividades" in proyecto
    assert isinstance(proyecto["actividades"], list)
    assert proyecto["actividades"] == []


def test_obtener_proyecto_inexistente(cliente):
    respuesta = cliente.get("/api/proyectos/999")

    assert respuesta.status_code == status.HTTP_404_NOT_FOUND
    assert respuesta.json()["detail"] == "Proyecto no encontrado"


def test_obtener_proyecto_con_actividades(cliente):
    datos_proyecto = {
        "nombre": "Proyecto de integración",
        "descripcion": "Proyecto creado mediante una prueba de integración"
    }

    respuesta_creacion = cliente.post(
        "/api/proyectos",
        json=datos_proyecto
    )

    id_proyecto = respuesta_creacion.json()["id"]

    datos_actividad = {
        "nombre": "Actividad de prueba",
        "bac": 1000.0,
        "porcentaje_planificado": 50.0,
        "porcentaje_completado": 25.0,
        "costo_real": 500.0
    }

    cliente.post(
        f"/api/proyectos/{id_proyecto}/actividades",
        json=datos_actividad
    )

    respuesta = cliente.get(f"/api/proyectos/{id_proyecto}")

    assert respuesta.status_code == status.HTTP_200_OK

    proyecto = respuesta.json()

    assert proyecto["id"] == id_proyecto
    assert proyecto["nombre"] == datos_proyecto["nombre"]
    assert proyecto["descripcion"] == datos_proyecto["descripcion"]
    assert "actividades" in proyecto
    assert isinstance(proyecto["actividades"], list)
    assert len(proyecto["actividades"]) == 1

    actividad = proyecto["actividades"][0]

    assert actividad["nombre"] == datos_actividad["nombre"]
    assert actividad["bac"] == datos_actividad["bac"]
    assert actividad["porcentaje_planificado"] == datos_actividad["porcentaje_planificado"]
    assert actividad["porcentaje_completado"] == datos_actividad["porcentaje_completado"]
    assert actividad["costo_real"] == datos_actividad["costo_real"]


def test_actualizar_proyecto_existente(cliente):
    datos_proyecto = {
        "nombre": "Proyecto de integración",
        "descripcion": "Proyecto creado mediante una prueba de integración"
    }

    respuesta_creacion = cliente.post(
        "/api/proyectos",
        json=datos_proyecto
    )

    id_proyecto = respuesta_creacion.json()["id"]

    datos_actualizacion = {
        "nombre": "Sistema EVM Actualizado",
        "descripcion": "Proyecto actualizado mediante una prueba de integración"
    }

    respuesta = cliente.put(
        f"/api/proyectos/{id_proyecto}",
        json=datos_actualizacion
    )

    assert respuesta.status_code == status.HTTP_200_OK

    proyecto_actualizado = respuesta.json()

    assert proyecto_actualizado["id"] == id_proyecto
    assert proyecto_actualizado["nombre"] == datos_actualizacion["nombre"]
    assert proyecto_actualizado["descripcion"] == datos_actualizacion["descripcion"]


def test_actualizar_proyecto_inexistente(cliente):
    datos_actualizacion = {
        "nombre": "Proyecto inexistente",
        "descripcion": "Esta actualización no debe realizarse"
    }

    respuesta = cliente.put(
        "/api/proyectos/999",
        json=datos_actualizacion
    )

    assert respuesta.status_code == status.HTTP_404_NOT_FOUND
    assert respuesta.json()["detail"] == "Proyecto no encontrado"


def test_eliminar_proyecto_existente(cliente):
    datos_proyecto = {
        "nombre": "Proyecto de integración",
        "descripcion": "Proyecto creado mediante una prueba de integración"
    }

    respuesta_creacion = cliente.post(
        "/api/proyectos",
        json=datos_proyecto
    )

    id_proyecto = respuesta_creacion.json()["id"]

    respuesta = cliente.delete(f"/api/proyectos/{id_proyecto}")

    assert respuesta.status_code == status.HTTP_204_NO_CONTENT
    assert respuesta.content == b""


def test_eliminar_proyecto_inexistente(cliente):
    respuesta = cliente.delete("/api/proyectos/999")

    assert respuesta.status_code == status.HTTP_404_NOT_FOUND
    assert respuesta.json()["detail"] == "Proyecto no encontrado"