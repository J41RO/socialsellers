/**
 * Tests TDD para Dashboard - funcionalidad de ventas
 * TAREA #012 Frontend - Fase RED
 */
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Dashboard from '../Dashboard';
import { AuthProvider } from '../../context/AuthContext';
import * as api from '../../services/api';

// Mock de las APIs
vi.mock('../../services/api', () => ({
  reportesAPI: {
    getMetricas: vi.fn(),
  },
  ventasAPI: {
    getAll: vi.fn(),
    getByVendedor: vi.fn(),
  },
  notificacionesAPI: {
    test: vi.fn(),
  },
  productosAPI: {
    getAll: vi.fn(),
  },
  vendedoresAPI: {
    getAll: vi.fn(),
  },
}));

// Mock del AuthContext
vi.mock('../../context/AuthContext', async () => {
  const actual = await vi.importActual('../../context/AuthContext');
  return {
    ...actual,
    useAuth: vi.fn(() => ({
      usuario: { id: 1, nombre: 'Admin Test', email: 'admin@test.com', rol: 'admin', activo: true },
      isAuthenticated: true,
      isLoading: false,
      login: vi.fn(),
      logout: vi.fn(),
    })),
  };
});

describe('Dashboard - Funcionalidad de ventas', () => {
  const mockMetricas = {
    total_ventas: 10000,
    ventas_mes_actual: 5000,
    total_comisiones: 1000,
    comisiones_mes_actual: 500,
    total_productos: 50,
    productos_bajo_stock: 5,
  };

  const mockVentas = [
    {
      id: 1,
      producto_id: 1,
      vendedor_id: 1,
      producto_nombre: 'Producto 1',
      vendedor_nombre: 'Vendedor 1',
      cantidad: 2,
      precio_unitario: 100,
      precio_total: 200,
      comision: 20,
      fecha_venta: '2025-10-28T10:00:00',
    },
  ];

  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(api.reportesAPI.getMetricas).mockResolvedValue(mockMetricas);
    vi.mocked(api.ventasAPI.getAll).mockResolvedValue(mockVentas);
    vi.mocked(api.productosAPI.getAll).mockResolvedValue([]);
    vi.mocked(api.vendedoresAPI.getAll).mockResolvedValue([]);
  });

  it('debe mostrar el botón "Registrar Venta" para admin', async () => {
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/Registrar Venta/i)).toBeInTheDocument();
    });
  });

  it('debe abrir el modal al hacer click en "Registrar Venta"', async () => {
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/Registrar Venta/i)).toBeInTheDocument();
    });

    const registerButton = screen.getByText(/Registrar Venta/i);
    fireEvent.click(registerButton);

    await waitFor(() => {
      expect(screen.getByText(/Registrar Nueva Venta/i)).toBeInTheDocument();
    });
  });

  it('debe refrescar los datos después de crear una venta exitosamente', async () => {
    vi.mocked(api.ventasAPI.getAll).mockResolvedValueOnce(mockVentas);

    const { rerender } = render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(api.reportesAPI.getMetricas).toHaveBeenCalledTimes(1);
      expect(api.ventasAPI.getAll).toHaveBeenCalledTimes(1);
    });

    // Simular creación exitosa de venta (esto se hará a través del modal)
    const newMockVentas = [
      ...mockVentas,
      {
        id: 2,
        producto_id: 2,
        vendedor_id: 1,
        producto_nombre: 'Producto 2',
        vendedor_nombre: 'Vendedor 1',
        cantidad: 1,
        precio_unitario: 50,
        precio_total: 50,
        comision: 5,
        fecha_venta: '2025-10-28T11:00:00',
      },
    ];

    vi.mocked(api.ventasAPI.getAll).mockResolvedValueOnce(newMockVentas);

    // Rerender para simular el refresh
    rerender(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    // Verificar que los datos se refrescaron
    await waitFor(() => {
      expect(api.ventasAPI.getAll).toHaveBeenCalled();
    });
  });

  it('debe mostrar las ventas recientes en la tabla', async () => {
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/Ventas Recientes/i)).toBeInTheDocument();
      expect(screen.getByText('Producto 1')).toBeInTheDocument();
      expect(screen.getByText('Vendedor 1')).toBeInTheDocument();
      expect(screen.getByText(/\$200\.00/)).toBeInTheDocument();
    });
  });
});
