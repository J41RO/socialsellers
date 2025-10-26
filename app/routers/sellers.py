"""
Router para módulo de Vendedores
Endpoints relacionados con la gestión de vendedores sociales
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud, auth
from app.database import get_db

router = APIRouter(
    prefix="/vendedores",
    tags=["vendedores"]
)

@router.post("/registrar", response_model=schemas.VendedorResponse)
def registrar_vendedor(
    vendedor: schemas.VendedorRegistro,
    db: Session = Depends(get_db),
    usuario_actual = Depends(auth.rol_requerido(["vendedor", "admin"]))
):
    """
    Registra un nuevo vendedor en el sistema
    Persiste el registro en base de datos

    Requiere autenticación con rol 'vendedor' o 'admin'
    """
    db_vendedor = crud.crear_vendedor(db=db, vendedor=vendedor)
    return db_vendedor
