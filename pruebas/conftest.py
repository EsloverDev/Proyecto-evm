import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from backend.base_de_datos import DATABASE_URL, get_db_session
from backend.principal import aplicacion


@pytest.fixture
def cliente():
    engine_pruebas = create_engine(DATABASE_URL)
    connection = engine_pruebas.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    def obtener_sesion_prueba():
        return session

    aplicacion.dependency_overrides[get_db_session] = obtener_sesion_prueba

    with TestClient(aplicacion) as cliente_pruebas:
        yield cliente_pruebas

    aplicacion.dependency_overrides.clear()
    session.close()
    transaction.rollback()
    connection.close()
    engine_pruebas.dispose()