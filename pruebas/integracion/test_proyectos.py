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
    respuesta = cliente.get("/api/proyectos/1")

    assert respuesta.status_code == status.HTTP_200_OK

    proyecto = respuesta.json()

    assert proyecto["id"] == 1
    assert proyecto["nombre"] == "Sistema EVM"
    assert proyecto["descripcion"] == "Aplicacion para gestionar proyectos"


def test_obtener_proyecto_inexistente(cliente):
    respuesta = cliente.get("/api/proyectos/999")

    assert respuesta.status_code == status.HTTP_404_NOT_FOUND
    assert respuesta.json()["detail"] == "Proyecto no encontrado"


def test_actualizar_proyecto_existente(cliente):
    datos_actualizacion = {
        "nombre": "Sistema EVM Actualizado",
        "descripcion": "Proyecto actualizado mediante una prueba de integración"
    }

    respuesta = cliente.put(
        "/api/proyectos/1",
        json=datos_actualizacion
    )

    assert respuesta.status_code == status.HTTP_200_OK

    proyecto_actualizado = respuesta.json()

    assert proyecto_actualizado["id"] == 1
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
    respuesta = cliente.delete("/api/proyectos/1")

    assert respuesta.status_code == status.HTTP_204_NO_CONTENT
    assert respuesta.content == b""


def test_eliminar_proyecto_inexistente(cliente):
    respuesta = cliente.delete("/api/proyectos/999")

    assert respuesta.status_code == status.HTTP_404_NOT_FOUND
    assert respuesta.json()["detail"] == "Proyecto no encontrado"