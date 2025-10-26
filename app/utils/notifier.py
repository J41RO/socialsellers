"""
Módulo de notificaciones simuladas para Social Sellers.
TAREA #011 - Sistema de Notificaciones Automáticas

Implementa envío simulado de emails y mensajes WhatsApp
mediante logs de consola (sin conexiones reales a SMTP o Twilio).
"""

import logging
from datetime import datetime
from typing import Optional

# Configurar logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def enviar_email_simulado(
    destinatario: str,
    asunto: str,
    mensaje: str
) -> bool:
    """
    Simula el envío de un correo electrónico.

    Args:
        destinatario: Email del destinatario
        asunto: Asunto del correo
        mensaje: Cuerpo del mensaje

    Returns:
        True si el envío fue exitoso (siempre en modo simulado)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    logger.info("📧 EMAIL SIMULADO ENVIADO")
    logger.info(f"⏰ Timestamp: {timestamp}")
    logger.info(f"📬 Destinatario: {destinatario}")
    logger.info(f"📌 Asunto: {asunto}")
    logger.info(f"📄 Mensaje: {mensaje}")
    logger.info("✅ Estado: Enviado exitosamente (simulado)")
    logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    return True


def enviar_whatsapp_simulado(
    telefono: str,
    mensaje: str
) -> bool:
    """
    Simula el envío de un mensaje de WhatsApp.

    Args:
        telefono: Número de teléfono del destinatario
        mensaje: Contenido del mensaje

    Returns:
        True si el envío fue exitoso (siempre en modo simulado)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    logger.info("📱 WHATSAPP SIMULADO ENVIADO")
    logger.info(f"⏰ Timestamp: {timestamp}")
    logger.info(f"📞 Teléfono: {telefono}")
    logger.info(f"💬 Mensaje: {mensaje}")
    logger.info("✅ Estado: Enviado exitosamente (simulado)")
    logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    return True


def notificar_venta(
    vendedor_nombre: str,
    vendedor_email: str,
    vendedor_telefono: str,
    producto_nombre: str,
    cantidad: int,
    total: float
) -> bool:
    """
    Envía notificaciones de venta por Email y WhatsApp al vendedor.

    Args:
        vendedor_nombre: Nombre del vendedor
        vendedor_email: Email del vendedor
        vendedor_telefono: Teléfono del vendedor
        producto_nombre: Nombre del producto vendido
        cantidad: Cantidad vendida
        total: Monto total de la venta

    Returns:
        True si ambas notificaciones fueron enviadas exitosamente
    """
    # Construir mensajes
    asunto = f"Venta registrada - {producto_nombre}"
    mensaje_email = f"""
Hola {vendedor_nombre},

Se ha registrado una nueva venta:
- Producto: {producto_nombre}
- Cantidad: {cantidad}
- Total: ${total:.2f}

¡Felicitaciones por tu venta!

Social Sellers
    """.strip()

    mensaje_whatsapp = f"🎉 Nueva venta registrada!\n" \
                      f"Producto: {producto_nombre}\n" \
                      f"Cantidad: {cantidad}\n" \
                      f"Total: ${total:.2f}"

    # Enviar notificaciones
    email_enviado = enviar_email_simulado(
        destinatario=vendedor_email,
        asunto=asunto,
        mensaje=mensaje_email
    )

    whatsapp_enviado = enviar_whatsapp_simulado(
        telefono=vendedor_telefono,
        mensaje=mensaje_whatsapp
    )

    return email_enviado and whatsapp_enviado


def notificar_stock_bajo(
    producto_nombre: str,
    stock_actual: int,
    stock_minimo: int,
    admin_email: str = "admin@socialsellers.com"
) -> bool:
    """
    Envía notificación de stock bajo al administrador por Email.

    Args:
        producto_nombre: Nombre del producto con stock bajo
        stock_actual: Stock actual del producto
        stock_minimo: Stock mínimo configurado
        admin_email: Email del administrador (default: admin@socialsellers.com)

    Returns:
        True si la notificación fue enviada exitosamente
    """
    asunto = f"⚠️ ALERTA: Stock bajo - {producto_nombre}"
    mensaje = f"""
ALERTA DE INVENTARIO

El siguiente producto tiene stock bajo:
- Producto: {producto_nombre}
- Stock actual: {stock_actual}
- Stock mínimo: {stock_minimo}
- Diferencia: {stock_minimo - stock_actual}

Se requiere reposición urgente.

Social Sellers - Sistema de Inventario
    """.strip()

    return enviar_email_simulado(
        destinatario=admin_email,
        asunto=asunto,
        mensaje=mensaje
    )
