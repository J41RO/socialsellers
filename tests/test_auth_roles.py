"""
Tests para autorización basada en roles
Verificación de permisos y control de acceso
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

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

def test_sin_token_acceso_denegado():
    """Test: Intentar acceder a endpoint protegido sin token"""
    vendedor_data = {
        "nombre": "Test Vendedor",
        "red_social": "Instagram",
        "usuario": "@testvendedor"
    }

    # Intentar registrar vendedor sin autenticación
    response = client.post("/vendedores/registrar", json=vendedor_data)

    # Debe retornar 401 Unauthorized
    assert response.status_code == 401
    assert "detail" in response.json()

def test_vendedor_puede_registrar_vendedores():
    """Test: Usuario con rol vendedor puede registrar vendedores"""
    # 1. Registrar usuario vendedor
    usuario_data = {
        "nombre": "Vendedor Test",
        "email": "vendedor@example.com",
        "password": "password123",
        "rol": "vendedor"
    }
    client.post("/auth/registrar", json=usuario_data)

    # 2. Login para obtener token
    login_data = {
        "username": "vendedor@example.com",
        "password": "password123"
    }
    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]

    # 3. Registrar vendedor con token
    vendedor_data = {
        "nombre": "Nuevo Vendedor",
        "red_social": "Facebook",
        "usuario": "@nuevovendedor"
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/vendedores/registrar", json=vendedor_data, headers=headers)

    # Debe ser exitoso
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["nombre"] == "Nuevo Vendedor"
    assert json_response["usuario"] == "@nuevovendedor"

def test_admin_puede_listar_usuarios():
    """Test: Usuario con rol admin puede listar usuarios"""
    # 1. Registrar usuario admin
    admin_data = {
        "nombre": "Admin Test",
        "email": "admin@example.com",
        "password": "adminpass",
        "rol": "admin"
    }
    client.post("/auth/registrar", json=admin_data)

    # 2. Login como admin
    login_data = {
        "username": "admin@example.com",
        "password": "adminpass"
    }
    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]

    # 3. Listar usuarios
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/admin/usuarios", headers=headers)

    # Debe ser exitoso
    assert response.status_code == 200
    usuarios = response.json()
    assert isinstance(usuarios, list)
    assert len(usuarios) >= 1  # Al menos el admin

def test_vendedor_no_puede_listar_usuarios():
    """Test: Usuario con rol vendedor NO puede listar usuarios (403 Forbidden)"""
    # 1. Registrar usuario vendedor
    vendedor_data = {
        "nombre": "Vendedor Test",
        "email": "vendedor2@example.com",
        "password": "vendedorpass",
        "rol": "vendedor"
    }
    client.post("/auth/registrar", json=vendedor_data)

    # 2. Login como vendedor
    login_data = {
        "username": "vendedor2@example.com",
        "password": "vendedorpass"
    }
    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]

    # 3. Intentar listar usuarios (debe fallar)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/admin/usuarios", headers=headers)

    # Debe retornar 403 Forbidden
    assert response.status_code == 403
    assert "Acceso denegado" in response.json()["detail"]
