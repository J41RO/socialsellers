"""
Tests para módulo de Productos (Inventario)
Verificación de endpoints y autorización de productos
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

def test_crear_producto_admin():
    """Test: Usuario con rol admin puede crear productos"""
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

    # 3. Crear producto
    producto_data = {
        "nombre": "Producto Test",
        "descripcion": "Descripción del producto",
        "precio": 99.99,
        "stock": 10,
        "activo": True
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/productos/registrar", json=producto_data, headers=headers)

    # Debe retornar 201 Created
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["nombre"] == "Producto Test"
    assert json_response["precio"] == 99.99
    assert json_response["stock"] == 10
    assert json_response["activo"] == True
    assert "id" in json_response

def test_listar_productos_autenticado():
    """Test: Cualquier usuario autenticado puede listar productos"""
    # 1. Registrar usuario vendedor (no admin)
    vendedor_data = {
        "nombre": "Vendedor Test",
        "email": "vendedor@example.com",
        "password": "vendedorpass",
        "rol": "vendedor"
    }
    client.post("/auth/registrar", json=vendedor_data)

    # 2. Login como vendedor
    login_data = {
        "username": "vendedor@example.com",
        "password": "vendedorpass"
    }
    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]

    # 3. Listar productos
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/productos/listar", headers=headers)

    # Debe ser exitoso (200 OK)
    assert response.status_code == 200
    productos = response.json()
    assert isinstance(productos, list)

def test_actualizar_producto_admin():
    """Test: Usuario admin puede actualizar productos (stock, precio, estado)"""
    # 1. Registrar usuario admin
    admin_data = {
        "nombre": "Admin Test",
        "email": "admin2@example.com",
        "password": "adminpass",
        "rol": "admin"
    }
    client.post("/auth/registrar", json=admin_data)

    # 2. Login como admin
    login_data = {
        "username": "admin2@example.com",
        "password": "adminpass"
    }
    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Crear producto primero
    producto_data = {
        "nombre": "Producto Original",
        "descripcion": "Descripción original",
        "precio": 50.0,
        "stock": 5,
        "activo": True
    }
    create_response = client.post("/productos/registrar", json=producto_data, headers=headers)
    producto_id = create_response.json()["id"]

    # 4. Actualizar el producto
    update_data = {
        "stock": 20,
        "precio": 75.0,
        "activo": False
    }
    response = client.patch(f"/productos/{producto_id}", json=update_data, headers=headers)

    # Debe ser exitoso (200 OK)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["stock"] == 20
    assert json_response["precio"] == 75.0
    assert json_response["activo"] == False
    assert json_response["nombre"] == "Producto Original"  # No cambia

def test_vendedor_no_puede_crear():
    """Test: Usuario con rol vendedor NO puede crear productos (403 Forbidden)"""
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

    # 3. Intentar crear producto (debe fallar)
    producto_data = {
        "nombre": "Producto No Autorizado",
        "descripcion": "No debería crearse",
        "precio": 100.0,
        "stock": 5
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/productos/registrar", json=producto_data, headers=headers)

    # Debe retornar 403 Forbidden
    assert response.status_code == 403
    assert "Acceso denegado" in response.json()["detail"]

def test_sin_auth_no_puede_listar():
    """Test: Usuario sin autenticación NO puede listar productos (401 Unauthorized)"""
    # Intentar listar productos sin token
    response = client.get("/productos/listar")

    # Debe retornar 401 Unauthorized
    assert response.status_code == 401
    assert "detail" in response.json()
