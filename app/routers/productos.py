"""
Router para módulo de Productos (Inventario)
Endpoints relacionados con la gestión de productos
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud, auth
from app.database import get_db

router = APIRouter(
    prefix="/productos",
    tags=["productos"]
)

@router.post("/registrar", response_model=schemas.ProductoResponse, status_code=status.HTTP_201_CREATED)
def registrar_producto(
    producto: schemas.ProductoCrear,
    db: Session = Depends(get_db),
    usuario_actual = Depends(auth.rol_requerido(["admin"]))
):
    """
    Registra un nuevo producto en el inventario

    Requiere autenticación con rol 'admin'

    Args:
        producto: Datos del producto a crear
        db: Sesión de base de datos
        usuario_actual: Usuario autenticado (debe ser admin)

    Returns:
        Producto creado
    """
    nuevo_producto = crud.crear_producto(db=db, producto=producto)
    return nuevo_producto

@router.get("/listar", response_model=list[schemas.ProductoResponse])
def listar_productos(
    db: Session = Depends(get_db),
    usuario_actual = Depends(auth.obtener_usuario_actual)
):
    """
    Lista todos los productos del inventario

    Requiere autenticación (cualquier rol)

    Args:
        db: Sesión de base de datos
        usuario_actual: Usuario autenticado

    Returns:
        Lista de todos los productos
    """
    productos = crud.listar_productos(db)
    return productos

@router.patch("/{producto_id}", response_model=schemas.ProductoResponse)
def actualizar_producto(
    producto_id: int,
    producto_update: schemas.ProductoActualizar,
    db: Session = Depends(get_db),
    usuario_actual = Depends(auth.rol_requerido(["admin"]))
):
    """
    Actualiza un producto existente (stock, precio, estado)

    Requiere autenticación con rol 'admin'

    Args:
        producto_id: ID del producto a actualizar
        producto_update: Datos a actualizar
        db: Sesión de base de datos
        usuario_actual: Usuario autenticado (debe ser admin)

    Returns:
        Producto actualizado

    Raises:
        HTTPException: Si el producto no existe
    """
    producto_actualizado = crud.actualizar_producto(db, producto_id, producto_update)

    if producto_actualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return producto_actualizado
