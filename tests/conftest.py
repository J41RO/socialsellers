"""
Configuración centralizada de tests para Social Sellers Backend
Fixtures compartidos para todos los módulos de testing
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import Base, get_db

# Base de datos en memoria para testing (no usa archivo físico)
# El uso de StaticPool y check_same_thread=False es necesario para SQLite en memoria con FastAPI
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Mantiene una sola conexión para toda la sesión de tests
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Fixture que proporciona una sesión de base de datos para cada test.
    Scope=function asegura que cada test tiene una BD limpia.
    """
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)

    # Crear sesión
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        # Limpiar todas las tablas después del test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Fixture que proporciona un TestClient de FastAPI configurado con la BD de test.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # El cierre se maneja en db_session fixture

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Limpiar overrides después del test
    app.dependency_overrides.clear()


def crear_usuario_y_login(client_instance, email: str, password: str, rol: str = "vendedor"):
    """
    Helper compartido para crear usuario y obtener token JWT.

    Args:
        client_instance: TestClient de FastAPI
        email: Email del usuario
        password: Password del usuario
        rol: Rol del usuario (vendedor/admin)

    Returns:
        str: Token JWT de autenticación
    """
    # Crear usuario
    usuario_data = {
        "nombre": f"Usuario {email.split('@')[0]}",
        "email": email,
        "password": password,
        "rol": rol
    }
    client_instance.post("/auth/registrar", json=usuario_data)

    # Login y obtener token
    login_data = {
        "username": email,
        "password": password
    }
    login_response = client_instance.post("/auth/login", data=login_data)
    return login_response.json()["access_token"]
