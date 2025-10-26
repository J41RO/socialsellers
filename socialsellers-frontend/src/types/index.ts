export interface Usuario {
  id: number;
  nombre: string;
  email: string;
  rol: 'admin' | 'vendedor';
  comision_porcentaje?: number;
  activo: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  usuario: Usuario;
}

export interface Producto {
  id: number;
  codigo_producto: string;
  nombre: string;
  descripcion?: string;
  precio_venta: number;
  precio_compra: number;
  stock_actual: number;
  stock_minimo: number;
  activo: boolean;
  fecha_creacion: string;
}

export interface Venta {
  id: number;
  vendedor_id: number;
  vendedor_nombre?: string;
  producto_id: number;
  producto_nombre?: string;
  cantidad: number;
  precio_unitario: number;
  precio_total: number;
  comision: number;
  fecha_venta: string;
}

export interface VentaCreate {
  producto_id: number;
  cantidad: number;
  precio_unitario: number;
}

export interface ProductoCreate {
  codigo_producto: string;
  nombre: string;
  descripcion?: string;
  precio_venta: number;
  precio_compra: number;
  stock_actual: number;
  stock_minimo: number;
}

export interface RankingVendedor {
  vendedor_id: number;
  vendedor_nombre: string;
  total_ventas: number;
  total_comisiones: number;
  cantidad_ventas: number;
}

export interface MetricasGenerales {
  total_ventas: number;
  total_comisiones: number;
  total_productos: number;
  productos_bajo_stock: number;
  ventas_mes_actual: number;
  comisiones_mes_actual: number;
}
