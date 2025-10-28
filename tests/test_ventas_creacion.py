"""
Tests TDD para creación de ventas dinámicas
TAREA #012: POST /ventas con vendor_id y precio_unitario
"""
import pytest
from sqlalchemy.orm import Session
from app import models, schemas, crud, auth
from tests.conftest import crear_usuario_y_login


@pytest.fixture
def admin_token(client):
    """Crea usuario admin y retorna token JWT"""
    return crear_usuario_y_login(client, "admin@test.com", "admin123", "admin")


@pytest.fixture
def vendedor_token(client):
    """Crea usuario vendedor y retorna token JWT"""
    return crear_usuario_y_login(client, "vendedor@test.com", "vend123", "vendedor")


@pytest.fixture
def producto_test(db_session: Session):
    """Crea producto de prueba con stock"""
    producto = models.Producto(
        nombre="Producto Test",
        descripcion="Descripción test",
        precio=100.0,
        stock=10,
        activo=True
    )
    db_session.add(producto)
    db_session.commit()
    db_session.refresh(producto)
    return producto


@pytest.fixture
def vendedor_test(client, db_session: Session):
    """Crea vendedor de prueba y retorna el objeto Usuario"""
    # Crear vendedor usando helper
    crear_usuario_y_login(client, "juan@ventas.com", "secure123", "vendedor")

    # Buscar el usuario en la DB
    from app.models import Usuario
    vendedor = db_session.query(Usuario).filter(Usuario.email == "juan@ventas.com").first()
    return vendedor


# ============================================
# TEST 1: Crear venta OK retorna 201 y total correcto
# ============================================
def test_crear_venta_ok_retorna_201_y_total_correcto(
    client,
    admin_token: str,
    producto_test: models.Producto,
    vendedor_test: models.Usuario
):
    """
    Test RED: POST /ventas con datos válidos
    Debe retornar 201 y venta creada con total correcto
    """
    payload = {
        "producto_id": producto_test.id,
        "vendedor_id": vendedor_test.id,
        "cantidad": 2,
        "precio_unitario": 50.0
    }

    response = client.post(
        "/ventas",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 201
    data = response.json()

    # Verificar estructura de respuesta
    assert "id" in data
    assert data["producto_id"] == producto_test.id
    assert data["vendedor_id"] == vendedor_test.id
    assert data["cantidad"] == 2
    assert data["total"] == 100.0  # 2 * 50.0
    assert "fecha" in data


# ============================================
# TEST 2: Crear venta falla si cantidad inválida
# ============================================
def test_crear_venta_falla_si_cantidad_invalida(
    client,
    admin_token: str,
    producto_test: models.Producto,
    vendedor_test: models.Usuario
):
    """
    Test RED: POST /ventas con cantidad <= 0
    Debe retornar 422 Unprocessable Entity (validación de Pydantic)
    """
    payload = {
        "producto_id": producto_test.id,
        "vendedor_id": vendedor_test.id,
        "cantidad": 0,
        "precio_unitario": 50.0
    }

    response = client.post(
        "/ventas",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 422
    # Pydantic devuelve estructura de error diferente
    assert "detail" in response.json()


# ============================================
# TEST 3: Crear venta falla si producto inexistente
# ============================================
def test_crear_venta_falla_si_producto_inexistente(
    client,
    admin_token: str,
    vendedor_test: models.Usuario
):
    """
    Test RED: POST /ventas con producto_id que no existe
    Debe retornar 404 Not Found
    """
    payload = {
        "producto_id": 99999,  # ID inexistente
        "vendedor_id": vendedor_test.id,
        "cantidad": 2,
        "precio_unitario": 50.0
    }

    response = client.post(
        "/ventas",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 404
    assert "producto" in response.json()["detail"].lower()


# ============================================
# TEST 4: Crear venta falla si vendedor inexistente
# ============================================
def test_crear_venta_falla_si_vendedor_inexistente(
    client,
    admin_token: str,
    producto_test: models.Producto
):
    """
    Test RED: POST /ventas con vendedor_id que no existe
    Debe retornar 404 Not Found
    """
    payload = {
        "producto_id": producto_test.id,
        "vendedor_id": 99999,  # ID inexistente
        "cantidad": 2,
        "precio_unitario": 50.0
    }

    response = client.post(
        "/ventas",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 404
    assert "vendedor" in response.json()["detail"].lower()
