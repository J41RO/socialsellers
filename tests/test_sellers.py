"""
Tests para módulo de Vendedores
Metodología TDD - Tests primero, implementación después
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import Vendedor

# Base de datos de testing en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override de la dependencia de base de datos para tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """Crear y limpiar base de datos antes de cada test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_api_activa():
    """Test básico: verificar que la API responde"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "API Social Sellers activa"}

def test_registrar_vendedor():
    """Test: Registrar un nuevo vendedor con persistencia en BD (requiere autenticación)"""
    # 1. Primero registrar un usuario vendedor
    usuario_data = {
        "nombre": "Test User",
        "email": "testuser@example.com",
        "password": "testpass",
        "rol": "vendedor"
    }
    client.post("/auth/registrar", json=usuario_data)

    # 2. Login para obtener token
    login_data = {
        "username": "testuser@example.com",
        "password": "testpass"
    }
    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]

    # 3. Registrar vendedor con autenticación
    vendedor_data = {
        "nombre": "Juan Pérez",
        "red_social": "Instagram",
        "usuario": "@juanperez"
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/vendedores/registrar", json=vendedor_data, headers=headers)

    # Verificar respuesta exitosa
    assert response.status_code == 200

    # Verificar que el JSON incluye un ID válido
    json_response = response.json()
    assert "id" in json_response
    assert json_response["id"] > 0
    assert json_response["nombre"] == "Juan Pérez"
    assert json_response["red_social"] == "Instagram"
    assert json_response["usuario"] == "@juanperez"

    # Verificar que el registro existe en la base de datos
    db = TestingSessionLocal()
    vendedor_count = db.query(Vendedor).count()
    assert vendedor_count == 1
    db.close()
