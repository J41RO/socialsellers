import axios from 'axios';
import type {
  AuthResponse,
  LoginCredentials,
  Usuario,
  Producto,
  ProductoCreate,
  Venta,
  VentaCreate,
  RankingVendedor,
  MetricasGenerales,
  Notificacion,
  NotificacionTest,
} from '../types';

// URL de la API - se puede configurar con variable de entorno
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token JWT a todas las peticiones
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('usuario');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Autenticación
export const authAPI = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const params = new URLSearchParams();
    params.append('username', credentials.email);
    params.append('password', credentials.password);
    const { data } = await api.post<AuthResponse>('/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return data;
  },

  getCurrentUser: async (): Promise<Usuario> => {
    const { data } = await api.get<Usuario>('/auth/me');
    return data;
  },
};

// Vendedores
export const vendedoresAPI = {
  getAll: async (): Promise<Usuario[]> => {
    const { data } = await api.get<Usuario[]>('/vendedores');
    return data;
  },

  getById: async (id: number): Promise<Usuario> => {
    const { data } = await api.get<Usuario>(`/vendedores/${id}`);
    return data;
  },

  create: async (vendedor: Partial<Usuario>): Promise<Usuario> => {
    const { data } = await api.post<Usuario>('/vendedores/registrar', vendedor);
    return data;
  },

  update: async (id: number, vendedor: Partial<Usuario>): Promise<Usuario> => {
    const { data } = await api.put<Usuario>(`/vendedores/${id}`, vendedor);
    return data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/vendedores/${id}`);
  },
};

// Productos
export const productosAPI = {
  getAll: async (): Promise<Producto[]> => {
    const { data } = await api.get<Producto[]>('/productos');
    return data;
  },

  getById: async (id: number): Promise<Producto> => {
    const { data } = await api.get<Producto>(`/productos/${id}`);
    return data;
  },

  create: async (producto: ProductoCreate): Promise<Producto> => {
    const { data } = await api.post<Producto>('/productos', producto);
    return data;
  },

  update: async (id: number, producto: Partial<ProductoCreate>): Promise<Producto> => {
    const { data } = await api.put<Producto>(`/productos/${id}`, producto);
    return data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/productos/${id}`);
  },

  getBajoStock: async (): Promise<Producto[]> => {
    const { data } = await api.get<Producto[]>('/productos/bajo-stock');
    return data;
  },
};

// Ventas
export const ventasAPI = {
  getAll: async (): Promise<Venta[]> => {
    const { data } = await api.get<Venta[]>('/ventas');
    return data;
  },

  getById: async (id: number): Promise<Venta> => {
    const { data } = await api.get<Venta>(`/ventas/${id}`);
    return data;
  },

  create: async (venta: VentaCreate): Promise<Venta> => {
    const { data } = await api.post<Venta>('/ventas/registrar', venta);
    return data;
  },

  getByVendedor: async (vendedorId: number): Promise<Venta[]> => {
    const { data } = await api.get<Venta[]>(`/ventas/vendedor/${vendedorId}`);
    return data;
  },

  getPorPeriodo: async (fechaInicio: string, fechaFin: string): Promise<Venta[]> => {
    const { data } = await api.get<Venta[]>('/ventas/periodo', {
      params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin },
    });
    return data;
  },
};

// Reportes
export const reportesAPI = {
  getRanking: async (
    fechaInicio?: string,
    fechaFin?: string
  ): Promise<RankingVendedor[]> => {
    const { data } = await api.get<RankingVendedor[]>('/reportes/ranking', {
      params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin },
    });
    return data;
  },

  getMetricas: async (): Promise<MetricasGenerales> => {
    const { data } = await api.get<MetricasGenerales>('/reportes/metricas');
    return data;
  },

  exportarVentas: async (formato: 'csv' | 'pdf'): Promise<Blob> => {
    const { data } = await api.get(`/reportes/exportar/${formato}`, {
      responseType: 'blob',
    });
    return data;
  },
};

// Notificaciones
export const notificacionesAPI = {
  getAll: async (): Promise<Notificacion[]> => {
    const { data } = await api.get<Notificacion[]>('/notificaciones');
    return data;
  },

  test: async (): Promise<NotificacionTest> => {
    const { data } = await api.post<NotificacionTest>('/notificaciones/test');
    return data;
  },

  marcarComoLeida: async (id: number): Promise<void> => {
    await api.patch(`/notificaciones/${id}/leida`);
  },
};

export default api;
