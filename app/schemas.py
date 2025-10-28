"""
Schemas Pydantic v2
Validación y serialización de datos
"""
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from datetime import datetime

class VendedorBase(BaseModel):
    """Schema base para Vendedor"""
    nombre: str
    red_social: str
    usuario: str

class VendedorRegistro(VendedorBase):
    """Schema para registro de vendedor"""
    pass

class VendedorResponse(VendedorBase):
    """Schema para respuesta de vendedor"""
    id: int

    model_config = ConfigDict(from_attributes=True)

# Schemas de Usuario (Autenticación)
class UsuarioBase(BaseModel):
    """Schema base para Usuario"""
    nombre: str
    email: EmailStr

class UsuarioRegistro(UsuarioBase):
    """Schema para registro de usuario"""
    password: str
    rol: str = "vendedor"  # vendedor o admin

class UsuarioLogin(BaseModel):
    """Schema para login de usuario"""
    email: EmailStr
    password: str

class UsuarioResponse(UsuarioBase):
    """Schema para respuesta de usuario (sin password)"""
    id: int
    rol: str

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    """Schema para respuesta de token JWT"""
    access_token: str
    token_type: str = "bearer"

class TokenWithUser(Token):
    """Schema para respuesta de token JWT con datos del usuario"""
    usuario: UsuarioResponse

class TokenData(BaseModel):
    """Schema para datos contenidos en el token"""
    email: str | None = None

# Schemas de Producto (Inventario)
class ProductoBase(BaseModel):
    """Schema base para Producto"""
    nombre: str
    descripcion: str | None = None
    precio: float
    stock: int = 0
    activo: bool = True

class ProductoCrear(ProductoBase):
    """Schema para creación de producto"""
    pass

class ProductoActualizar(BaseModel):
    """Schema para actualización de producto (campos opcionales)"""
    nombre: str | None = None
    descripcion: str | None = None
    precio: float | None = None
    stock: int | None = None
    activo: bool | None = None

class ProductoResponse(ProductoBase):
    """Schema para respuesta de producto"""
    id: int

    model_config = ConfigDict(from_attributes=True)

# Schemas de Venta (Ventas y Comisiones)
class VentaBase(BaseModel):
    """Schema base para Venta"""
    producto_id: int
    cantidad: int = 1

class VentaCrear(VentaBase):
    """Schema para creación de venta (vendedor autenticado)"""
    pass

class VentaCrearAdmin(BaseModel):
    """Schema para creación de venta por admin (especifica vendedor_id y precio_unitario)"""
    producto_id: int
    vendedor_id: int
    cantidad: int = 1
    precio_unitario: float

    @field_validator('cantidad')
    @classmethod
    def validar_cantidad(cls, v):
        if v <= 0:
            raise ValueError('La cantidad debe ser mayor que 0')
        return v

class VentaResponse(BaseModel):
    """Schema para respuesta de venta"""
    id: int
    producto_id: int
    vendedor_id: int
    cantidad: int
    total: float
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)

# Schemas de Reportes y Comisiones
class ResumenPeriodo(BaseModel):
    """Schema para resumen de ventas por período"""
    total_ventas: int
    monto_total: float
    fecha_desde: datetime | None = None
    fecha_hasta: datetime | None = None

class TopProducto(BaseModel):
    """Schema para ranking de productos"""
    producto_id: int
    nombre_producto: str
    cantidad_vendida: int
    monto_total: float

class TopVendedor(BaseModel):
    """Schema para ranking de vendedores"""
    vendedor_id: int
    nombre_vendedor: str
    total_ventas: int
    monto_total: float

class ComisionVendedor(BaseModel):
    """Schema para comisiones por vendedor"""
    vendedor_id: int
    nombre_vendedor: str
    total_ventas: int
    monto_total_vendido: float
    porcentaje_comision: float
    monto_comision: float
