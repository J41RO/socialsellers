"""
Router para módulo de Ventas
Endpoints relacionados con el registro y seguimiento de ventas
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud, auth
from app.database import get_db

router = APIRouter(
    prefix="/ventas",
    tags=["ventas"]
)

@router.post("", response_model=schemas.VentaResponse, status_code=status.HTTP_201_CREATED)
def crear_venta_desde_admin(
    venta: schemas.VentaCrearAdmin,
    db: Session = Depends(get_db),
    usuario_actual = Depends(auth.rol_requerido(["admin"]))
):
    """
    Crea una nueva venta especificando vendedor y precio (solo admin)

    Requiere autenticación con rol 'admin'

    Permite al admin crear ventas para cualquier vendedor con precio personalizado

    Args:
        venta: Datos de la venta (producto_id, vendedor_id, cantidad, precio_unitario)
        db: Sesión de base de datos
        usuario_actual: Usuario autenticado (debe ser admin)

    Returns:
        Venta creada con total calculado

    Raises:
        HTTPException 400: Si la cantidad es inválida
        HTTPException 404: Si el producto o vendedor no existen
    """
    try:
        nueva_venta = crud.crear_venta_admin(db=db, venta=venta)
        return nueva_venta
    except ValueError as e:
        error_msg = str(e)
        if "no encontrado" in error_msg or "no existe" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_msg
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )

@router.post("/registrar", response_model=schemas.VentaResponse, status_code=status.HTTP_201_CREATED)
def registrar_venta(
    venta: schemas.VentaCrear,
    db: Session = Depends(get_db),
    usuario_actual = Depends(auth.rol_requerido(["vendedor", "admin"]))
):
    """
    Registra una nueva venta

    Requiere autenticación con rol 'vendedor' o 'admin'

    Valida stock disponible y calcula total automáticamente
    Reduce el stock del producto

    Args:
        venta: Datos de la venta (producto_id, cantidad)
        db: Sesión de base de datos
        usuario_actual: Usuario autenticado (vendedor o admin)

    Returns:
        Venta creada con total calculado y fecha

    Raises:
        HTTPException 400: Si no hay stock suficiente
        HTTPException 404: Si el producto no existe
    """
    try:
        nueva_venta = crud.crear_venta(db=db, venta=venta, vendedor_id=usuario_actual.id)
        return nueva_venta
    except ValueError as e:
        error_msg = str(e)
        if "no encontrado" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_msg
            )
        else:
            # Error de stock insuficiente
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )

@router.get("/listar", response_model=list[schemas.VentaResponse])
def listar_ventas(
    db: Session = Depends(get_db),
    usuario_actual = Depends(auth.obtener_usuario_actual)
):
    """
    Lista las ventas

    - Admin: ve todas las ventas del sistema
    - Vendedor: ve solo sus propias ventas

    Requiere autenticación (cualquier rol)

    Args:
        db: Sesión de base de datos
        usuario_actual: Usuario autenticado

    Returns:
        Lista de ventas (filtrada según rol)
    """
    if usuario_actual.rol == "admin":
        # Admin ve todas las ventas
        ventas = crud.listar_ventas(db)
    else:
        # Vendedor ve solo sus ventas
        ventas = crud.listar_ventas_por_vendedor(db, usuario_actual.id)

    return ventas

@router.get("/resumen")
def obtener_resumen(
    db: Session = Depends(get_db),
    usuario_actual = Depends(auth.rol_requerido(["admin"]))
):
    """
    Obtiene resumen global de ventas

    Requiere autenticación con rol 'admin'

    Args:
        db: Sesión de base de datos
        usuario_actual: Usuario autenticado (debe ser admin)

    Returns:
        Resumen con total_ventas y monto_total
    """
    resumen = crud.obtener_resumen_ventas(db)
    return resumen
