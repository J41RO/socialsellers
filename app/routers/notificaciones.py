"""
Router de notificaciones automáticas.
TAREA #011 - Sistema de Notificaciones Automáticas
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from app.utils import notifier
from app import auth

router = APIRouter(prefix="/notificaciones", tags=["notificaciones"])


# Schemas
class NotificacionVenta(BaseModel):
    """Schema para notificación de venta."""
    vendedor_nombre: str
    vendedor_email: EmailStr
    vendedor_telefono: str
    producto_nombre: str
    cantidad: int
    total: float


class NotificacionStockBajo(BaseModel):
    """Schema para notificación de stock bajo."""
    producto_nombre: str
    stock_actual: int
    stock_minimo: int
    admin_email: EmailStr


class RespuestaTest(BaseModel):
    """Schema de respuesta para endpoint de prueba."""
    mensaje: str
    email_enviado: bool
    whatsapp_enviado: bool


# Endpoints
@router.get("/test", response_model=RespuestaTest)
async def test_notificaciones():
    """
    Endpoint de prueba para verificar el sistema de notificaciones.

    Envía notificaciones simuladas de Email y WhatsApp.

    Returns:
        RespuestaTest con estado de envío de ambas notificaciones
    """
    email_enviado = notifier.enviar_email_simulado(
        destinatario="test@socialsellers.com",
        asunto="Test de notificaciones",
        mensaje="Este es un mensaje de prueba del sistema de notificaciones."
    )

    whatsapp_enviado = notifier.enviar_whatsapp_simulado(
        telefono="+1234567890",
        mensaje="Test de notificación WhatsApp - Social Sellers"
    )

    return RespuestaTest(
        mensaje="Notificaciones de prueba enviadas exitosamente",
        email_enviado=email_enviado,
        whatsapp_enviado=whatsapp_enviado
    )


@router.post("/venta", dependencies=[Depends(auth.obtener_usuario_actual)])
async def enviar_notificacion_venta(notificacion: NotificacionVenta):
    """
    Envía notificaciones de venta por Email y WhatsApp.

    Requiere autenticación JWT.

    Args:
        notificacion: Datos de la venta para notificar

    Returns:
        Confirmación de envío de notificaciones
    """
    resultado = notifier.notificar_venta(
        vendedor_nombre=notificacion.vendedor_nombre,
        vendedor_email=notificacion.vendedor_email,
        vendedor_telefono=notificacion.vendedor_telefono,
        producto_nombre=notificacion.producto_nombre,
        cantidad=notificacion.cantidad,
        total=notificacion.total
    )

    if not resultado:
        raise HTTPException(
            status_code=500,
            detail="Error al enviar notificaciones de venta"
        )

    return {
        "mensaje": "Notificaciones de venta enviadas exitosamente",
        "vendedor": notificacion.vendedor_nombre,
        "producto": notificacion.producto_nombre
    }


@router.post(
    "/stock-bajo",
    dependencies=[Depends(auth.rol_requerido(["admin"]))]
)
async def enviar_notificacion_stock_bajo(notificacion: NotificacionStockBajo):
    """
    Envía notificación de stock bajo al administrador.

    Requiere rol de admin.

    Args:
        notificacion: Datos del producto con stock bajo

    Returns:
        Confirmación de envío de notificación
    """
    resultado = notifier.notificar_stock_bajo(
        producto_nombre=notificacion.producto_nombre,
        stock_actual=notificacion.stock_actual,
        stock_minimo=notificacion.stock_minimo,
        admin_email=notificacion.admin_email
    )

    if not resultado:
        raise HTTPException(
            status_code=500,
            detail="Error al enviar notificación de stock bajo"
        )

    return {
        "mensaje": "Notificación de stock bajo enviada exitosamente",
        "producto": notificacion.producto_nombre,
        "stock_actual": notificacion.stock_actual
    }
