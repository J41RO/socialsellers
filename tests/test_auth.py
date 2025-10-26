"""
Tests para módulo de Autenticación
TDD - Tests para registro, login y obtención de usuario actual
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import Usuario

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

def test_registrar_usuario():
    """Test: Registrar un nuevo usuario"""
    usuario_data = {
        "nombre": "María González",
        "email": "maria@example.com",
        "password": "password123",
        "rol": "vendedor"
    }
    response = client.post("/auth/registrar", json=usuario_data)

    # Verificar respuesta exitosa
    assert response.status_code == 201
    json_response = response.json()

    # Verificar datos del usuario
    assert "id" in json_response
    assert json_response["id"] > 0
    assert json_response["nombre"] == "María González"
    assert json_response["email"] == "maria@example.com"
    assert json_response["rol"] == "vendedor"
    assert "password" not in json_response  # No debe retornar password

    # Verificar que el usuario existe en BD
    db = TestingSessionLocal()
    usuario_count = db.query(Usuario).filter(Usuario.email == "maria@example.com").count()
    assert usuario_count == 1
    db.close()

def test_login_correcto():
    """Test: Login con credenciales correctas"""
    # Primero registrar usuario
    usuario_data = {
        "nombre": "Carlos López",
        "email": "carlos@example.com",
        "password": "password456",
        "rol": "admin"
    }
    client.post("/auth/registrar", json=usuario_data)

    # Intentar login
    login_data = {
        "username": "carlos@example.com",  # OAuth2PasswordRequestForm usa "username"
        "password": "password456"
    }
    response = client.post("/auth/login", data=login_data)

    # Verificar respuesta exitosa
    assert response.status_code == 200
    json_response = response.json()

    # Verificar token
    assert "access_token" in json_response
    assert "token_type" in json_response
    assert json_response["token_type"] == "bearer"
    assert len(json_response["access_token"]) > 0

def test_login_incorrecto():
    """Test: Login con credenciales incorrectas"""
    # Primero registrar usuario
    usuario_data = {
        "nombre": "Ana Martínez",
        "email": "ana@example.com",
        "password": "password789",
        "rol": "vendedor"
    }
    client.post("/auth/registrar", json=usuario_data)

    # Intentar login con password incorrecta
    login_data = {
        "username": "ana@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", data=login_data)

    # Verificar que falla
    assert response.status_code == 401
    assert "Email o contraseña incorrectos" in response.json()["detail"]

def test_obtener_usuario_actual():
    """Test: Obtener usuario actual con token válido"""
    # Registrar usuario
    usuario_data = {
        "nombre": "Pedro Ramírez",
        "email": "pedro@example.com",
        "password": "password111",
        "rol": "vendedor"
    }
    client.post("/auth/registrar", json=usuario_data)

    # Login para obtener token
    login_data = {
        "username": "pedro@example.com",
        "password": "password111"
    }
    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]

    # Obtener usuario actual con token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)

    # Verificar respuesta exitosa
    assert response.status_code == 200
    json_response = response.json()

    # Verificar datos del usuario
    assert json_response["nombre"] == "Pedro Ramírez"
    assert json_response["email"] == "pedro@example.com"
    assert json_response["rol"] == "vendedor"
    assert "password" not in json_response
