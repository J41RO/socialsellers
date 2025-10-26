"""
Router para funciones administrativas
Endpoints exclusivos para administradores
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud, auth
from app.database import get_db

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.get("/usuarios", response_model=list[schemas.UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db),
    usuario_actual = Depends(auth.rol_requerido(["admin"]))
):
    """
    Lista todos los usuarios del sistema

    Requiere autenticación con rol 'admin'

    Args:
        db: Sesión de base de datos
        usuario_actual: Usuario autenticado (debe ser admin)

    Returns:
        Lista de todos los usuarios
    """
    usuarios = crud.listar_usuarios(db)
    return usuarios
