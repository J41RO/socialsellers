"""
Router para módulo de Reportes y Comisiones
Endpoints para análisis de ventas, rankings y cálculo de comisiones
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app import schemas, crud, auth
from app.database import get_db

router = APIRouter(
    prefix="/reportes",
    tags=["reportes"]
)

comisiones_router = APIRouter(
    prefix="/comisiones",
    tags=["comisiones"]
)

@router.get("/resumen", response_model=schemas.ResumenPeriodo)
def obtener_resumen_periodo(
    desde: Optional[datetime] = Query(None, description="Fecha de inicio (YYYY-MM-DDTHH:MM:SS)"),
    hasta: Optional[datetime] = Query(None, description="Fecha de fin (YYYY-MM-DDTHH:MM:SS)"),
    db: Session = Depends(get_db),
    usuario_actual = Depends(auth.rol_requerido(["admin"]))
):
    """
    Obtiene resumen de ventas filtrado por período

    Requiere autenticación con rol 'admin'

    Query params:
        - desde: Fecha de inicio del período (opcional)
        - hasta: Fecha de fin del período (opcional)

    Args:
        desde: Fecha de inicio (opcional)
        hasta: Fecha de fin (opcional)
        db: Sesión de base de datos
        usuario_actual: Usuario autenticado (debe ser admin)

    Returns:
        Resumen con total_ventas, monto_total y fechas del período
    """
    resumen = crud.obtener_resumen_por_periodo(db, fecha_desde=desde, fecha_hasta=hasta)
    return resumen

@router.get("/top-productos", response_model=list[schemas.TopProducto])
def obtener_top_productos(
    limite: int = Query(5, ge=1, le=20, description="Número de productos a retornar"),
    db: Session = Depends(get_db),
    usuario_actual = Depends(auth.rol_requerido(["admin"]))
):
    """
    Obtiene el ranking de productos más vendidos

    Requiere autenticación con rol 'admin'

    Query params:
        - limite: Número de productos a retornar (default 5, max 20)

    Args:
        limite: Número de productos en el ranking
        db: Sesión de base de datos
        usuario_actual: Usuario autenticado (debe ser admin)

    Returns:
        Lista de productos ordenados por cantidad vendida
    """
    top_productos = crud.obtener_top_productos(db, limite=limite)
    return top_productos

@router.get("/top-vendedores", response_model=list[schemas.TopVendedor])
def obtener_top_vendedores(
    limite: int = Query(10, ge=1, le=50, description="Número de vendedores a retornar"),
    db: Session = Depends(get_db),
    usuario_actual = Depends(auth.rol_requerido(["admin"]))
):
    """
    Obtiene el ranking de vendedores por monto vendido

    Requiere autenticación con rol 'admin'

    Query params:
        - limite: Número de vendedores a retornar (default 10, max 50)

    Args:
        limite: Número de vendedores en el ranking
        db: Sesión de base de datos
        usuario_actual: Usuario autenticado (debe ser admin)

    Returns:
        Lista de vendedores ordenados por monto total vendido
    """
    top_vendedores = crud.obtener_top_vendedores(db, limite=limite)
    return top_vendedores

@comisiones_router.get("/calcular", response_model=list[schemas.ComisionVendedor])
def calcular_comisiones(
    porcentaje: float = Query(10.0, ge=0, le=100, description="Porcentaje de comisión"),
    db: Session = Depends(get_db),
    usuario_actual = Depends(auth.rol_requerido(["admin"]))
):
    """
    Calcula las comisiones por vendedor

    Requiere autenticación con rol 'admin'

    Query params:
        - porcentaje: Porcentaje de comisión (default 10%, max 100%)

    Args:
        porcentaje: Porcentaje de comisión a aplicar
        db: Sesión de base de datos
        usuario_actual: Usuario autenticado (debe ser admin)

    Returns:
        Lista de vendedores con sus comisiones calculadas
    """
    comisiones = crud.calcular_comisiones(db, porcentaje=porcentaje)
    return comisiones
