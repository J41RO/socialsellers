"""
Autenticación JWT y Password Hashing
Funciones para generación de tokens y validación de contraseñas
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

# Configuración de seguridad
SECRET_KEY = "tu-clave-secreta-super-segura-cambiala-en-produccion"  # Cambiar en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verificar_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si la contraseña plana coincide con el hash

    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Contraseña hasheada

    Returns:
        True si coinciden, False caso contrario
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def hashear_password(password: str) -> str:
    """
    Genera hash de una contraseña

    Args:
        password: Contraseña en texto plano

    Returns:
        Hash de la contraseña
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def crear_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT

    Args:
        data: Datos a codificar en el token
        expires_delta: Tiempo de expiración opcional

    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verificar_credenciales(db: Session, email: str, password: str):
    """
    Verifica credenciales de usuario

    Args:
        db: Sesión de base de datos
        email: Email del usuario
        password: Contraseña en texto plano

    Returns:
        Usuario si las credenciales son correctas, None caso contrario
    """
    usuario = crud.obtener_usuario_por_email(db, email)
    if not usuario:
        return None
    if not verificar_password(password, usuario.password):
        return None
    return usuario

async def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Obtiene el usuario actual desde el token JWT

    Args:
        token: Token JWT
        db: Sesión de base de datos

    Returns:
        Usuario actual

    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    usuario = crud.obtener_usuario_por_email(db, email=token_data.email)
    if usuario is None:
        raise credentials_exception

    return usuario

def rol_requerido(roles_permitidos: list[str]):
    """
    Dependency factory para verificar que el usuario tenga uno de los roles permitidos

    Args:
        roles_permitidos: Lista de roles que pueden acceder al endpoint

    Returns:
        Función de dependencia que valida el rol del usuario

    Raises:
        HTTPException: Si el usuario no tiene un rol permitido
    """
    async def verificar_rol(usuario_actual = Depends(obtener_usuario_actual)):
        if usuario_actual.rol not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Roles permitidos: {', '.join(roles_permitidos)}"
            )
        return usuario_actual

    return verificar_rol
