"""
Tests TDD para el módulo de notificaciones automáticas.
TAREA #011 - Sistema de Notificaciones Automáticas
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.utils.notifier import (
    enviar_email_simulado,
    enviar_whatsapp_simulado,
    notificar_venta,
    notificar_stock_bajo,
)

# Base de datos de testing en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override de la dependencia de base de datos para tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """Crear tablas antes de cada test y limpiar después"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestNotificadorSimulado:
    """Tests unitarios para funciones de notificación simuladas."""

    def test_enviar_email_simulado_retorna_exito(self):
        """Test: enviar_email_simulado debe retornar True y loggear mensaje."""
        resultado = enviar_email_simulado(
            destinatario="test@example.com",
            asunto="Test",
            mensaje="Mensaje de prueba"
        )
        assert resultado is True

    def test_enviar_whatsapp_simulado_retorna_exito(self):
        """Test: enviar_whatsapp_simulado debe retornar True y loggear mensaje."""
        resultado = enviar_whatsapp_simulado(
            telefono="+1234567890",
            mensaje="Mensaje de prueba WhatsApp"
        )
        assert resultado is True

    def test_notificar_venta_envia_ambas_notificaciones(self):
        """Test: notificar_venta debe enviar email y WhatsApp."""
        with patch('app.utils.notifier.enviar_email_simulado') as mock_email, \
             patch('app.utils.notifier.enviar_whatsapp_simulado') as mock_whatsapp:

            mock_email.return_value = True
            mock_whatsapp.return_value = True

            resultado = notificar_venta(
                vendedor_nombre="Juan Pérez",
                vendedor_email="juan@example.com",
                vendedor_telefono="+1234567890",
                producto_nombre="Producto A",
                cantidad=5,
                total=500.0
            )

            assert resultado is True
            assert mock_email.called
            assert mock_whatsapp.called

    def test_notificar_stock_bajo_envia_email_admin(self):
        """Test: notificar_stock_bajo debe enviar email al admin."""
        with patch('app.utils.notifier.enviar_email_simulado') as mock_email:
            mock_email.return_value = True

            resultado = notificar_stock_bajo(
                producto_nombre="Producto B",
                stock_actual=2,
                stock_minimo=10,
                admin_email="admin@socialsellers.com"
            )

            assert resultado is True
            assert mock_email.called
            mock_email.assert_called_once()


class TestEndpointNotificaciones:
    """Tests de integración para el router de notificaciones."""

    def test_endpoint_test_notificaciones_retorna_200(self):
        """Test: GET /notificaciones/test debe retornar 200 OK."""
        response = client.get("/notificaciones/test")
        assert response.status_code == 200
        assert "email_enviado" in response.json()
        assert "whatsapp_enviado" in response.json()

    def test_notificacion_venta_requiere_autenticacion(self):
        """Test: POST /notificaciones/venta requiere token JWT."""
        response = client.post("/notificaciones/venta", json={
            "vendedor_nombre": "Test",
            "vendedor_email": "test@test.com",
            "vendedor_telefono": "+123",
            "producto_nombre": "Producto",
            "cantidad": 1,
            "total": 100.0
        })
        assert response.status_code == 401

    def test_notificacion_stock_bajo_solo_admin(self):
        """Test: POST /notificaciones/stock-bajo solo permite rol admin."""
        # Registrar y hacer login como vendedor
        client.post("/auth/registrar", json={
            "nombre": "Vendedor Test",
            "email": "vendedor@test.com",
            "password": "test123",
            "rol": "vendedor"
        })

        login_response = client.post("/auth/login", data={
            "username": "vendedor@test.com",
            "password": "test123"
        })
        token = login_response.json()["access_token"]

        # Intentar enviar notificación de stock bajo como vendedor
        response = client.post(
            "/notificaciones/stock-bajo",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "producto_nombre": "Producto",
                "stock_actual": 1,
                "stock_minimo": 10,
                "admin_email": "admin@test.com"
            }
        )
        assert response.status_code == 403  # Forbidden
