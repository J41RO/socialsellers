"""
Tests para módulo de Reportes y Comisiones
Verificación de análisis de ventas, rankings y cálculos
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
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
        "nombre": f"Usuario {email.split('@')[0]}",
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

def crear_producto(token_admin: str, nombre: str, precio: float, stock: int):
    """Helper para crear producto"""
    producto_data = {
        "nombre": nombre,
        "descripcion": f"Descripción de {nombre}",
        "precio": precio,
        "stock": stock,
        "activo": True
    }
    headers = {"Authorization": f"Bearer {token_admin}"}
    response = client.post("/productos/registrar", json=producto_data, headers=headers)
    return response.json()

def crear_venta(token: str, producto_id: int, cantidad: int):
    """Helper para crear venta"""
    venta_data = {"producto_id": producto_id, "cantidad": cantidad}
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/ventas/registrar", json=venta_data, headers=headers)
    return response.json()

def test_filtrado_por_fechas():
    """Test: Filtrar ventas por período de fechas"""
    # 1. Crear admin y productos
    token_admin = crear_usuario_y_login("admin@example.com", "adminpass", "admin")
    producto = crear_producto(token_admin, "Producto A", 100.0, 100)

    # 2. Crear vendedor y hacer ventas
    token_vendedor = crear_usuario_y_login("vendedor@example.com", "vendedorpass", "vendedor")
    crear_venta(token_vendedor, producto["id"], 2)
    crear_venta(token_vendedor, producto["id"], 3)

    # 3. Obtener resumen completo
    headers_admin = {"Authorization": f"Bearer {token_admin}"}
    response = client.get("/reportes/resumen", headers=headers_admin)

    assert response.status_code == 200
    resumen = response.json()
    assert resumen["total_ventas"] == 2
    assert resumen["monto_total"] == 500.0  # 200 + 300

    # 4. Filtrar por fecha futura (debe retornar 0)
    fecha_futura = (datetime.now() + timedelta(days=1)).isoformat()
    response_filtrado = client.get(
        f"/reportes/resumen?desde={fecha_futura}",
        headers=headers_admin
    )
    assert response_filtrado.status_code == 200
    resumen_filtrado = response_filtrado.json()
    assert resumen_filtrado["total_ventas"] == 0
    assert resumen_filtrado["monto_total"] == 0

def test_calculo_totales():
    """Test: Verificar cálculos correctos en resumen"""
    # 1. Crear admin y múltiples productos
    token_admin = crear_usuario_y_login("admin@example.com", "adminpass", "admin")
    prod1 = crear_producto(token_admin, "Producto A", 50.0, 50)
    prod2 = crear_producto(token_admin, "Producto B", 100.0, 50)

    # 2. Crear vendedor y hacer ventas variadas
    token_vendedor = crear_usuario_y_login("vendedor@example.com", "vendedorpass", "vendedor")
    crear_venta(token_vendedor, prod1["id"], 2)   # 50 * 2 = 100
    crear_venta(token_vendedor, prod2["id"], 3)   # 100 * 3 = 300
    crear_venta(token_vendedor, prod1["id"], 1)   # 50 * 1 = 50

    # 3. Obtener resumen y verificar cálculos
    headers_admin = {"Authorization": f"Bearer {token_admin}"}
    response = client.get("/reportes/resumen", headers=headers_admin)

    assert response.status_code == 200
    resumen = response.json()
    assert resumen["total_ventas"] == 3
    assert resumen["monto_total"] == 450.0  # 100 + 300 + 50

def test_ranking_productos():
    """Test: Top 5 productos más vendidos"""
    # 1. Crear admin y productos
    token_admin = crear_usuario_y_login("admin@example.com", "adminpass", "admin")
    prod_a = crear_producto(token_admin, "Producto A", 30.0, 100)
    prod_b = crear_producto(token_admin, "Producto B", 50.0, 100)
    prod_c = crear_producto(token_admin, "Producto C", 70.0, 100)

    # 2. Crear vendedor y hacer ventas con diferentes cantidades
    token_vendedor = crear_usuario_y_login("vendedor@example.com", "vendedorpass", "vendedor")
    # Producto B: 10 unidades
    crear_venta(token_vendedor, prod_b["id"], 5)
    crear_venta(token_vendedor, prod_b["id"], 5)
    # Producto C: 7 unidades
    crear_venta(token_vendedor, prod_c["id"], 7)
    # Producto A: 3 unidades
    crear_venta(token_vendedor, prod_a["id"], 3)

    # 3. Obtener top productos
    headers_admin = {"Authorization": f"Bearer {token_admin}"}
    response = client.get("/reportes/top-productos?limite=5", headers=headers_admin)

    assert response.status_code == 200
    top_productos = response.json()
    assert len(top_productos) == 3

    # Verificar orden (B primero con 10 unidades, C segundo con 7, A tercero con 3)
    assert top_productos[0]["nombre_producto"] == "Producto B"
    assert top_productos[0]["cantidad_vendida"] == 10
    assert top_productos[0]["monto_total"] == 500.0  # 50 * 10

    assert top_productos[1]["nombre_producto"] == "Producto C"
    assert top_productos[1]["cantidad_vendida"] == 7

    assert top_productos[2]["nombre_producto"] == "Producto A"
    assert top_productos[2]["cantidad_vendida"] == 3

def test_ranking_vendedores():
    """Test: Ranking de vendedores por monto vendido"""
    # 1. Crear admin y producto
    token_admin = crear_usuario_y_login("admin@example.com", "adminpass", "admin")
    producto = crear_producto(token_admin, "Producto Test", 100.0, 500)

    # 2. Crear tres vendedores
    token_v1 = crear_usuario_y_login("vendedor1@example.com", "pass1", "vendedor")
    token_v2 = crear_usuario_y_login("vendedor2@example.com", "pass2", "vendedor")
    token_v3 = crear_usuario_y_login("vendedor3@example.com", "pass3", "vendedor")

    # 3. Hacer ventas con diferentes montos
    # Vendedor 1: 5 ventas x 100 = 500
    crear_venta(token_v1, producto["id"], 5)
    # Vendedor 2: 10 ventas x 100 = 1000
    crear_venta(token_v2, producto["id"], 10)
    # Vendedor 3: 3 ventas x 100 = 300
    crear_venta(token_v3, producto["id"], 3)

    # 4. Obtener top vendedores
    headers_admin = {"Authorization": f"Bearer {token_admin}"}
    response = client.get("/reportes/top-vendedores?limite=10", headers=headers_admin)

    assert response.status_code == 200
    top_vendedores = response.json()
    assert len(top_vendedores) == 3

    # Verificar orden (V2 primero con 1000, V1 segundo con 500, V3 tercero con 300)
    assert top_vendedores[0]["nombre_vendedor"] == "Usuario vendedor2"
    assert top_vendedores[0]["monto_total"] == 1000.0
    assert top_vendedores[0]["total_ventas"] == 1

    assert top_vendedores[1]["nombre_vendedor"] == "Usuario vendedor1"
    assert top_vendedores[1]["monto_total"] == 500.0

    assert top_vendedores[2]["nombre_vendedor"] == "Usuario vendedor3"
    assert top_vendedores[2]["monto_total"] == 300.0

def test_comisiones_por_vendedor():
    """Test: Cálculo de comisiones con 10% por defecto"""
    # 1. Crear admin y producto
    token_admin = crear_usuario_y_login("admin@example.com", "adminpass", "admin")
    producto = crear_producto(token_admin, "Producto Test", 200.0, 100)

    # 2. Crear vendedores y hacer ventas
    token_v1 = crear_usuario_y_login("vendedor1@example.com", "pass1", "vendedor")
    token_v2 = crear_usuario_y_login("vendedor2@example.com", "pass2", "vendedor")

    # Vendedor 1: 1000 en total
    crear_venta(token_v1, producto["id"], 5)  # 5 * 200 = 1000
    # Vendedor 2: 600 en total
    crear_venta(token_v2, producto["id"], 3)  # 3 * 200 = 600

    # 3. Calcular comisiones con 10% (default)
    headers_admin = {"Authorization": f"Bearer {token_admin}"}
    response = client.get("/comisiones/calcular", headers=headers_admin)

    assert response.status_code == 200
    comisiones = response.json()
    assert len(comisiones) == 2

    # Buscar comisión del vendedor1
    comision_v1 = next(c for c in comisiones if c["nombre_vendedor"] == "Usuario vendedor1")
    assert comision_v1["monto_total_vendido"] == 1000.0
    assert comision_v1["porcentaje_comision"] == 10.0
    assert comision_v1["monto_comision"] == 100.0  # 10% de 1000

    # Buscar comisión del vendedor2
    comision_v2 = next(c for c in comisiones if c["nombre_vendedor"] == "Usuario vendedor2")
    assert comision_v2["monto_total_vendido"] == 600.0
    assert comision_v2["monto_comision"] == 60.0  # 10% de 600

    # 4. Calcular comisiones con 15%
    response_15 = client.get("/comisiones/calcular?porcentaje=15.0", headers=headers_admin)
    assert response_15.status_code == 200
    comisiones_15 = response_15.json()

    comision_v1_15 = next(c for c in comisiones_15 if c["nombre_vendedor"] == "Usuario vendedor1")
    assert comision_v1_15["porcentaje_comision"] == 15.0
    assert comision_v1_15["monto_comision"] == 150.0  # 15% de 1000
