"""
CRUD Operations
Operaciones de base de datos para cada modelo
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime
from app import models, schemas

def crear_vendedor(db: Session, vendedor: schemas.VendedorRegistro):
    """
    Crea un nuevo vendedor en la base de datos

    Args:
        db: Sesión de base de datos
        vendedor: Datos del vendedor a crear

    Returns:
        Vendedor creado con su ID
    """
    db_vendedor = models.Vendedor(**vendedor.model_dump())
    db.add(db_vendedor)
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

# CRUD de Usuarios (Autenticación)
def obtener_usuario_por_email(db: Session, email: str):
    """
    Obtiene un usuario por su email

    Args:
        db: Sesión de base de datos
        email: Email del usuario

    Returns:
        Usuario encontrado o None
    """
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def crear_usuario(db: Session, usuario: schemas.UsuarioRegistro, password_hash: str):
    """
    Crea un nuevo usuario en la base de datos con password hasheado

    Args:
        db: Sesión de base de datos
        usuario: Datos del usuario a crear
        password_hash: Password ya hasheado

    Returns:
        Usuario creado con su ID
    """
    db_usuario = models.Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password=password_hash,
        rol=usuario.rol
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def listar_usuarios(db: Session):
    """
    Lista todos los usuarios del sistema

    Args:
        db: Sesión de base de datos

    Returns:
        Lista de todos los usuarios
    """
    return db.query(models.Usuario).all()

# CRUD de Productos (Inventario)
def crear_producto(db: Session, producto: schemas.ProductoCrear):
    """
    Crea un nuevo producto en el inventario

    Args:
        db: Sesión de base de datos
        producto: Datos del producto a crear

    Returns:
        Producto creado con su ID
    """
    db_producto = models.Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def listar_productos(db: Session):
    """
    Lista todos los productos del inventario

    Args:
        db: Sesión de base de datos

    Returns:
        Lista de todos los productos
    """
    return db.query(models.Producto).all()

def obtener_producto_por_id(db: Session, producto_id: int):
    """
    Obtiene un producto por su ID

    Args:
        db: Sesión de base de datos
        producto_id: ID del producto

    Returns:
        Producto encontrado o None
    """
    return db.query(models.Producto).filter(models.Producto.id == producto_id).first()

def actualizar_producto(db: Session, producto_id: int, producto_update: schemas.ProductoActualizar):
    """
    Actualiza un producto existente

    Args:
        db: Sesión de base de datos
        producto_id: ID del producto a actualizar
        producto_update: Datos a actualizar

    Returns:
        Producto actualizado o None si no existe
    """
    db_producto = obtener_producto_por_id(db, producto_id)
    if db_producto is None:
        return None

    # Actualizar solo los campos que se enviaron
    update_data = producto_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_producto, field, value)

    db.commit()
    db.refresh(db_producto)
    return db_producto

# CRUD de Ventas
def crear_venta(db: Session, venta: schemas.VentaCrear, vendedor_id: int):
    """
    Crea una nueva venta en la base de datos

    Valida stock disponible, calcula total y reduce stock del producto

    Args:
        db: Sesión de base de datos
        venta: Datos de la venta a crear
        vendedor_id: ID del vendedor que realiza la venta

    Returns:
        Venta creada o None si no hay stock suficiente

    Raises:
        ValueError: Si el producto no existe o no hay stock suficiente
    """
    # Obtener producto
    producto = obtener_producto_por_id(db, venta.producto_id)
    if producto is None:
        raise ValueError("Producto no encontrado")

    # Validar stock disponible
    if producto.stock < venta.cantidad:
        raise ValueError(f"Stock insuficiente. Disponible: {producto.stock}, solicitado: {venta.cantidad}")

    # Calcular total
    total = producto.precio * venta.cantidad

    # Crear venta
    db_venta = models.Venta(
        producto_id=venta.producto_id,
        vendedor_id=vendedor_id,
        cantidad=venta.cantidad,
        total=total
    )
    db.add(db_venta)

    # Reducir stock del producto
    producto.stock -= venta.cantidad

    db.commit()
    db.refresh(db_venta)
    return db_venta

def listar_ventas(db: Session):
    """
    Lista todas las ventas del sistema

    Args:
        db: Sesión de base de datos

    Returns:
        Lista de todas las ventas
    """
    return db.query(models.Venta).all()

def listar_ventas_por_vendedor(db: Session, vendedor_id: int):
    """
    Lista las ventas de un vendedor específico

    Args:
        db: Sesión de base de datos
        vendedor_id: ID del vendedor

    Returns:
        Lista de ventas del vendedor
    """
    return db.query(models.Venta).filter(models.Venta.vendedor_id == vendedor_id).all()

def obtener_resumen_ventas(db: Session):
    """
    Obtiene un resumen de todas las ventas del sistema

    Args:
        db: Sesión de base de datos

    Returns:
        Dict con total de ventas y monto total recaudado
    """
    ventas = listar_ventas(db)
    total_ventas = len(ventas)
    monto_total = sum(venta.total for venta in ventas)

    return {
        "total_ventas": total_ventas,
        "monto_total": monto_total
    }

# CRUD de Reportes y Comisiones
def obtener_resumen_por_periodo(db: Session, fecha_desde: datetime = None, fecha_hasta: datetime = None):
    """
    Obtiene resumen de ventas filtrado por período

    Args:
        db: Sesión de base de datos
        fecha_desde: Fecha de inicio del período (opcional)
        fecha_hasta: Fecha de fin del período (opcional)

    Returns:
        Dict con total_ventas, monto_total y fechas del período
    """
    query = db.query(models.Venta)

    # Aplicar filtros de fecha si se proporcionan
    if fecha_desde:
        query = query.filter(models.Venta.fecha >= fecha_desde)
    if fecha_hasta:
        query = query.filter(models.Venta.fecha <= fecha_hasta)

    ventas = query.all()
    total_ventas = len(ventas)
    monto_total = sum(venta.total for venta in ventas)

    return {
        "total_ventas": total_ventas,
        "monto_total": monto_total,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta
    }

def obtener_top_productos(db: Session, limite: int = 5):
    """
    Obtiene el ranking de productos más vendidos

    Args:
        db: Sesión de base de datos
        limite: Número de productos a retornar (default 5)

    Returns:
        Lista de dicts con producto_id, nombre, cantidad_vendida y monto_total
    """
    # Agrupar ventas por producto y calcular totales
    resultados = db.query(
        models.Venta.producto_id,
        models.Producto.nombre.label('nombre_producto'),
        func.sum(models.Venta.cantidad).label('cantidad_vendida'),
        func.sum(models.Venta.total).label('monto_total')
    ).join(
        models.Producto, models.Venta.producto_id == models.Producto.id
    ).group_by(
        models.Venta.producto_id, models.Producto.nombre
    ).order_by(
        desc('cantidad_vendida')
    ).limit(limite).all()

    return [
        {
            "producto_id": r.producto_id,
            "nombre_producto": r.nombre_producto,
            "cantidad_vendida": r.cantidad_vendida,
            "monto_total": r.monto_total
        }
        for r in resultados
    ]

def obtener_top_vendedores(db: Session, limite: int = 10):
    """
    Obtiene el ranking de vendedores por monto vendido

    Args:
        db: Sesión de base de datos
        limite: Número de vendedores a retornar (default 10)

    Returns:
        Lista de dicts con vendedor_id, nombre, total_ventas y monto_total
    """
    # Agrupar ventas por vendedor y calcular totales
    resultados = db.query(
        models.Venta.vendedor_id,
        models.Usuario.nombre.label('nombre_vendedor'),
        func.count(models.Venta.id).label('total_ventas'),
        func.sum(models.Venta.total).label('monto_total')
    ).join(
        models.Usuario, models.Venta.vendedor_id == models.Usuario.id
    ).group_by(
        models.Venta.vendedor_id, models.Usuario.nombre
    ).order_by(
        desc('monto_total')
    ).limit(limite).all()

    return [
        {
            "vendedor_id": r.vendedor_id,
            "nombre_vendedor": r.nombre_vendedor,
            "total_ventas": r.total_ventas,
            "monto_total": r.monto_total
        }
        for r in resultados
    ]

def calcular_comisiones(db: Session, porcentaje: float = 10.0):
    """
    Calcula las comisiones por vendedor

    Args:
        db: Sesión de base de datos
        porcentaje: Porcentaje de comisión (default 10%)

    Returns:
        Lista de dicts con vendedor_id, nombre, total_ventas, monto_total_vendido,
        porcentaje_comision y monto_comision
    """
    # Agrupar ventas por vendedor
    resultados = db.query(
        models.Venta.vendedor_id,
        models.Usuario.nombre.label('nombre_vendedor'),
        func.count(models.Venta.id).label('total_ventas'),
        func.sum(models.Venta.total).label('monto_total_vendido')
    ).join(
        models.Usuario, models.Venta.vendedor_id == models.Usuario.id
    ).group_by(
        models.Venta.vendedor_id, models.Usuario.nombre
    ).all()

    return [
        {
            "vendedor_id": r.vendedor_id,
            "nombre_vendedor": r.nombre_vendedor,
            "total_ventas": r.total_ventas,
            "monto_total_vendido": r.monto_total_vendido,
            "porcentaje_comision": porcentaje,
            "monto_comision": round(r.monto_total_vendido * (porcentaje / 100), 2)
        }
        for r in resultados
    ]

# ======================================
# SEED DATA para MVP
# ======================================
def seed_database(db: Session):
    """
    Pobla la base de datos con datos iniciales para MVP
    Es idempotente: no duplica datos si ya existen
    """
    from app.auth import hashear_password
    from datetime import timedelta
    import random

    # 1. USUARIOS
    # Admin
    if not db.query(models.Usuario).filter(models.Usuario.email == "admin@socialsellers.com").first():
        admin = models.Usuario(
            nombre="Admin Demo",
            email="admin@socialsellers.com",
            password=hashear_password("admin123"),
            rol="admin"
        )
        db.add(admin)

    # Vendedor
    if not db.query(models.Usuario).filter(models.Usuario.email == "vendedor@socialsellers.com").first():
        vendedor = models.Usuario(
            nombre="Carlos Vendedor",
            email="vendedor@socialsellers.com",
            password=hashear_password("vendedor123"),
            rol="vendedor"
        )
        db.add(vendedor)

    db.commit()

    # 2. PRODUCTOS (usando campos correctos del modelo)
    productos_data = [
        ("Shampoo Keratina", "Shampoo restaurador con keratina", 12.50, 15),
        ("Acondicionador Argán", "Acondicionador nutritivo con aceite de argán", 15.00, 20),
        ("Tratamiento Capilar", "Tratamiento intensivo para cabello dañado", 25.00, 10),
    ]

    for nombre, desc, precio, stock in productos_data:
        if not db.query(models.Producto).filter(models.Producto.nombre == nombre).first():
            producto = models.Producto(
                nombre=nombre,
                descripcion=desc,
                precio=precio,
                stock=stock,
                activo=True
            )
            db.add(producto)

    db.commit()

    # 3. VENTAS
    vendedor = db.query(models.Usuario).filter(models.Usuario.rol == "vendedor").first()
    productos = db.query(models.Producto).all()

    # Solo crear ventas si no existen
    ventas_existentes = db.query(models.Venta).count()
    if ventas_existentes == 0 and vendedor and productos:
        for i in range(5):
            producto = random.choice(productos)
            cantidad = random.randint(1, 3)
            fecha_venta = datetime.now() - timedelta(days=random.randint(1, 30))

            venta = models.Venta(
                vendedor_id=vendedor.id,
                producto_id=producto.id,
                cantidad=cantidad,
                total=producto.precio * cantidad,
                fecha=fecha_venta
            )
            db.add(venta)

        db.commit()
