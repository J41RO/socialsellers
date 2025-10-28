"""
Router para autenticación
Endpoints relacionados con registro, login y gestión de usuarios
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, crud, auth
from app.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["autenticación"]
)

@router.post("/registrar", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(
    usuario: schemas.UsuarioRegistro,
    db: Session = Depends(get_db)
):
    """
    Registra un nuevo usuario en el sistema

    Args:
        usuario: Datos del usuario a registrar
        db: Sesión de base de datos

    Returns:
        Usuario creado

    Raises:
        HTTPException: Si el email ya está registrado
    """
    # Verificar si el email ya existe
    db_usuario = crud.obtener_usuario_por_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Hashear password
    password_hash = auth.hashear_password(usuario.password)

    # Crear usuario
    nuevo_usuario = crud.crear_usuario(db=db, usuario=usuario, password_hash=password_hash)

    return nuevo_usuario

@router.post("/login", response_model=schemas.TokenWithUser)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login de usuario y generación de token JWT

    Args:
        form_data: Formulario con username (email) y password
        db: Sesión de base de datos

    Returns:
        Token JWT con datos del usuario

    Raises:
        HTTPException: Si las credenciales son incorrectas
    """
    # Verificar credenciales
    usuario = auth.verificar_credenciales(db, form_data.username, form_data.password)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.crear_access_token(
        data={"sub": usuario.email},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": usuario
    }

@router.get("/me", response_model=schemas.UsuarioResponse)
async def obtener_usuario_actual(
    usuario_actual = Depends(auth.obtener_usuario_actual)
):
    """
    Obtiene información del usuario actualmente autenticado

    Args:
        usuario_actual: Usuario obtenido del token JWT

    Returns:
        Información del usuario actual
    """
    return usuario_actual
