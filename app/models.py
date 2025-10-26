"""
Modelos SQLAlchemy
Definición de tablas para la base de datos
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Vendedor(Base):
    """Modelo de Vendedor Social"""
    __tablename__ = "vendedores"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    red_social = Column(String)
    usuario = Column(String, unique=True, index=True)

class Usuario(Base):
    """Modelo de Usuario para autenticación"""
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # Hashed password
    rol = Column(String, nullable=False, default="vendedor")  # vendedor o admin

class Producto(Base):
    """Modelo de Producto para inventario"""
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False, index=True)
    descripcion = Column(String)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    activo = Column(Boolean, default=True)

class Venta(Base):
    """Modelo de Venta para registro de transacciones"""
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    vendedor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)
    total = Column(Float, nullable=False)
    fecha = Column(DateTime, server_default=func.now())
