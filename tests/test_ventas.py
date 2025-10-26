"""
Tests para módulo de Ventas y Comisiones
Verificación de endpoints, validaciones y cálculos
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

def crear_usuario_y_login(email: str, password: str, rol: str = "vendedor"):
    """Helper para crear usuario y obtener token"""
    usuario_data = {
        "nombre": f"Usuario {rol}",
        "email": email,
        "password": password,
        "rol": rol
    }
    client.post("/auth/registrar", json=usuario_data)

    login_data = {
        "username": email,
        "password": password
    }
    login_response = client.post("/auth/login", data=login_data)
    return login_response.json()["access_token"]

def crear_producto(token_admin: str, nombre: str = "Producto Test", precio: float = 100.0, stock: int = 10):
    """Helper para crear producto"""
    producto_data = {
        "nombre": nombre,
        "descripcion": "Descripción del producto",
        "precio": precio,
        "stock": stock,
        "activo": True
    }
    headers = {"Authorization": f"Bearer {token_admin}"}
    response = client.post("/productos/registrar", json=producto_data, headers=headers)
    return response.json()

def test_registrar_venta_vendedor():
    """Test: Usuario vendedor puede registrar ventas"""
    # 1. Crear admin para crear producto
    token_admin = crear_usuario_y_login("admin@example.com", "adminpass", "admin")

    # 2. Crear producto con stock
    producto = crear_producto(token_admin, "Producto A", 50.0, 20)

    # 3. Crear vendedor
    token_vendedor = crear_usuario_y_login("vendedor@example.com", "vendedorpass", "vendedor")

    # 4. Registrar venta
    venta_data = {
        "producto_id": producto["id"],
        "cantidad": 3
    }
    headers = {"Authorization": f"Bearer {token_vendedor}"}
    response = client.post("/ventas/registrar", json=venta_data, headers=headers)

    # Debe retornar 201 Created
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["producto_id"] == producto["id"]
    assert json_response["cantidad"] == 3
    assert json_response["total"] == 150.0  # 50.0 * 3
    assert "id" in json_response
    assert "fecha" in json_response

def test_registrar_venta_sin_stock():
    """Test: No se puede registrar venta si no hay stock suficiente (400)"""
    # 1. Crear admin y producto con stock limitado
    token_admin = crear_usuario_y_login("admin@example.com", "adminpass", "admin")
    producto = crear_producto(token_admin, "Producto B", 30.0, 5)  # Solo 5 en stock

    # 2. Crear vendedor
    token_vendedor = crear_usuario_y_login("vendedor@example.com", "vendedorpass", "vendedor")

    # 3. Intentar vender más de lo disponible
    venta_data = {
        "producto_id": producto["id"],
        "cantidad": 10  # Pide 10 pero solo hay 5
    }
    headers = {"Authorization": f"Bearer {token_vendedor}"}
    response = client.post("/ventas/registrar", json=venta_data, headers=headers)

    # Debe retornar 400 Bad Request
    assert response.status_code == 400
    assert "Stock insuficiente" in response.json()["detail"]

def test_listar_ventas_vendedor_solo_propias():
    """Test: Vendedor solo ve sus propias ventas"""
    # 1. Crear admin y producto
    token_admin = crear_usuario_y_login("admin@example.com", "adminpass", "admin")
    producto = crear_producto(token_admin, "Producto C", 25.0, 50)

    # 2. Crear dos vendedores
    token_vendedor1 = crear_usuario_y_login("vendedor1@example.com", "pass1", "vendedor")
    token_vendedor2 = crear_usuario_y_login("vendedor2@example.com", "pass2", "vendedor")

    # 3. Vendedor 1 hace 2 ventas
    venta_data = {"producto_id": producto["id"], "cantidad": 1}
    headers1 = {"Authorization": f"Bearer {token_vendedor1}"}
    client.post("/ventas/registrar", json=venta_data, headers=headers1)
    client.post("/ventas/registrar", json=venta_data, headers=headers1)

    # 4. Vendedor 2 hace 1 venta
    headers2 = {"Authorization": f"Bearer {token_vendedor2}"}
    client.post("/ventas/registrar", json=venta_data, headers=headers2)

    # 5. Vendedor 1 lista sus ventas (debe ver solo 2)
    response1 = client.get("/ventas/listar", headers=headers1)
    assert response1.status_code == 200
    ventas1 = response1.json()
    assert len(ventas1) == 2

    # 6. Vendedor 2 lista sus ventas (debe ver solo 1)
    response2 = client.get("/ventas/listar", headers=headers2)
    assert response2.status_code == 200
    ventas2 = response2.json()
    assert len(ventas2) == 1

def test_listar_ventas_admin_ve_todas():
    """Test: Admin ve todas las ventas del sistema"""
    # 1. Crear admin y producto
    token_admin = crear_usuario_y_login("admin@example.com", "adminpass", "admin")
    producto = crear_producto(token_admin, "Producto D", 40.0, 100)

    # 2. Crear vendedores
    token_vendedor1 = crear_usuario_y_login("vendedor1@example.com", "pass1", "vendedor")
    token_vendedor2 = crear_usuario_y_login("vendedor2@example.com", "pass2", "vendedor")

    # 3. Vendedores hacen ventas
    venta_data = {"producto_id": producto["id"], "cantidad": 1}
    headers1 = {"Authorization": f"Bearer {token_vendedor1}"}
    headers2 = {"Authorization": f"Bearer {token_vendedor2}"}
    client.post("/ventas/registrar", json=venta_data, headers=headers1)
    client.post("/ventas/registrar", json=venta_data, headers=headers2)

    # 4. Admin lista ventas (debe ver todas: 2)
    headers_admin = {"Authorization": f"Bearer {token_admin}"}
    response_admin = client.get("/ventas/listar", headers=headers_admin)
    assert response_admin.status_code == 200
    ventas_admin = response_admin.json()
    assert len(ventas_admin) == 2

def test_calculo_total_y_reduccion_stock():
    """Test: Verificar cálculo de total y reducción de stock"""
    # 1. Crear admin y producto
    token_admin = crear_usuario_y_login("admin@example.com", "adminpass", "admin")
    producto = crear_producto(token_admin, "Producto E", 75.0, 30)
    producto_id = producto["id"]

    # 2. Crear vendedor
    token_vendedor = crear_usuario_y_login("vendedor@example.com", "vendedorpass", "vendedor")

    # 3. Registrar venta de 5 unidades
    venta_data = {"producto_id": producto_id, "cantidad": 5}
    headers = {"Authorization": f"Bearer {token_vendedor}"}
    response_venta = client.post("/ventas/registrar", json=venta_data, headers=headers)

    # Verificar cálculo de total
    assert response_venta.status_code == 201
    venta = response_venta.json()
    assert venta["total"] == 375.0  # 75.0 * 5

    # 4. Verificar reducción de stock (debe quedar 25)
    headers_admin = {"Authorization": f"Bearer {token_admin}"}
    response_productos = client.get("/productos/listar", headers=headers_admin)
    productos = response_productos.json()
    producto_actualizado = next(p for p in productos if p["id"] == producto_id)
    assert producto_actualizado["stock"] == 25  # 30 - 5

def test_resumen_solo_admin():
    """Test: Solo admin puede acceder a /ventas/resumen"""
    # 1. Crear admin y producto
    token_admin = crear_usuario_y_login("admin@example.com", "adminpass", "admin")
    producto = crear_producto(token_admin, "Producto F", 60.0, 50)

    # 2. Crear vendedor y hacer ventas
    token_vendedor = crear_usuario_y_login("vendedor@example.com", "vendedorpass", "vendedor")
    venta_data = {"producto_id": producto["id"], "cantidad": 2}
    headers_vendedor = {"Authorization": f"Bearer {token_vendedor}"}
    client.post("/ventas/registrar", json=venta_data, headers=headers_vendedor)
    client.post("/ventas/registrar", json=venta_data, headers=headers_vendedor)

    # 3. Admin puede acceder al resumen
    headers_admin = {"Authorization": f"Bearer {token_admin}"}
    response_admin = client.get("/ventas/resumen", headers=headers_admin)
    assert response_admin.status_code == 200
    resumen = response_admin.json()
    assert resumen["total_ventas"] == 2
    assert resumen["monto_total"] == 240.0  # 60.0 * 2 * 2

    # 4. Vendedor NO puede acceder (403 Forbidden)
    response_vendedor = client.get("/ventas/resumen", headers=headers_vendedor)
    assert response_vendedor.status_code == 403
    assert "Acceso denegado" in response_vendedor.json()["detail"]
