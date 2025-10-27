"""
Test para validar población inicial de base de datos (seed data)
TDD: Este test debe fallar primero, luego implementamos el seed
"""
import pytest
from app.database import SessionLocal
from app.models import Usuario, Producto, Venta
from app.crud import seed_database

def test_seed_database_creates_initial_data():
    """
    Valida que seed_database() crea usuarios, productos y ventas iniciales
    """
    db = SessionLocal()

    try:
        # Limpiar base de datos para test limpio
        db.query(Venta).delete()
        db.query(Producto).delete()
        db.query(Usuario).delete()
        db.commit()

        # Ejecutar seed
        seed_database(db)

        # Validaciones
        usuarios_count = db.query(Usuario).count()
        productos_count = db.query(Producto).count()
        ventas_count = db.query(Venta).count()

        # Assertions
        assert usuarios_count >= 2, f"Debe haber al menos 2 usuarios (admin + vendedor), encontrados: {usuarios_count}"
        assert productos_count >= 3, f"Debe haber al menos 3 productos, encontrados: {productos_count}"
        assert ventas_count >= 5, f"Debe haber al menos 5 ventas, encontradas: {ventas_count}"

        # Validar que existe usuario admin
        admin = db.query(Usuario).filter(Usuario.email == "admin@socialsellers.com").first()
        assert admin is not None, "Debe existir usuario admin@socialsellers.com"
        assert admin.rol == "admin", "Usuario admin debe tener rol 'admin'"

        # Validar que existe al menos un vendedor
        vendedor = db.query(Usuario).filter(Usuario.rol == "vendedor").first()
        assert vendedor is not None, "Debe existir al menos un vendedor"

        # Validar que productos tienen datos válidos
        productos = db.query(Producto).all()
        for producto in productos:
            assert producto.nombre, "Producto debe tener nombre"
            assert producto.precio > 0, f"Producto {producto.nombre} debe tener precio > 0"
            assert producto.stock >= 0, f"Producto {producto.nombre} debe tener stock >= 0"

        # Validar que ventas están asociadas correctamente
        ventas = db.query(Venta).all()
        for venta in ventas:
            assert venta.vendedor_id, "Venta debe tener vendedor_id"
            assert venta.producto_id, "Venta debe tener producto_id"
            assert venta.cantidad > 0, "Venta debe tener cantidad > 0"
            assert venta.total > 0, "Venta debe tener total > 0"

    finally:
        db.close()

def test_seed_database_is_idempotent():
    """
    Valida que ejecutar seed_database() múltiples veces no duplica datos
    """
    db = SessionLocal()

    try:
        # Ejecutar seed dos veces
        seed_database(db)
        usuarios_count_1 = db.query(Usuario).count()

        seed_database(db)
        usuarios_count_2 = db.query(Usuario).count()

        # No debe duplicar usuarios
        assert usuarios_count_1 == usuarios_count_2, "Seed debe ser idempotente (no duplicar datos)"

    finally:
        db.close()
