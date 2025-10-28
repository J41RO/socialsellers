/**
 * Tests TDD para ModalNuevaVenta
 * TAREA #012 Frontend - Fase RED
 */
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ModalNuevaVenta from '../ModalNuevaVenta';
import * as api from '../../services/api';

// Mock de las APIs
vi.mock('../../services/api', () => ({
  productosAPI: {
    getAll: vi.fn(),
  },
  vendedoresAPI: {
    getAll: vi.fn(),
  },
  ventasAPI: {
    createAdmin: vi.fn(),
  },
}));

describe('ModalNuevaVenta', () => {
  const mockProductos = [
    { id: 1, nombre: 'Producto 1', precio_venta: 100, codigo_producto: 'P001', stock_actual: 10, stock_minimo: 5, activo: true, fecha_creacion: '2025-01-01' },
    { id: 2, nombre: 'Producto 2', precio_venta: 200, codigo_producto: 'P002', stock_actual: 20, stock_minimo: 5, activo: true, fecha_creacion: '2025-01-01' },
  ];

  const mockVendedores = [
    { id: 1, nombre: 'Vendedor 1', email: 'v1@test.com', rol: 'vendedor' as const, activo: true },
    { id: 2, nombre: 'Vendedor 2', email: 'v2@test.com', rol: 'vendedor' as const, activo: true },
  ];

  const mockOnClose = vi.fn();
  const mockOnSuccess = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(api.productosAPI.getAll).mockResolvedValue(mockProductos);
    vi.mocked(api.vendedoresAPI.getAll).mockResolvedValue(mockVendedores);
  });

  it('debe cargar productos y vendedores al abrir el modal', async () => {
    render(
      <ModalNuevaVenta
        isOpen={true}
        onClose={mockOnClose}
        onSuccess={mockOnSuccess}
      />
    );

    await waitFor(() => {
      expect(api.productosAPI.getAll).toHaveBeenCalled();
      expect(api.vendedoresAPI.getAll).toHaveBeenCalled();
    });
  });

  it('debe auto-completar el precio unitario al seleccionar un producto', async () => {
    render(
      <ModalNuevaVenta
        isOpen={true}
        onClose={mockOnClose}
        onSuccess={mockOnSuccess}
      />
    );

    await waitFor(() => {
      expect(screen.getByLabelText(/producto/i)).toBeInTheDocument();
    });

    const productoSelect = screen.getByLabelText(/producto/i);
    fireEvent.change(productoSelect, { target: { value: '1' } });

    await waitFor(() => {
      const precioInput = screen.getByLabelText(/precio unitario/i) as HTMLInputElement;
      expect(precioInput.value).toBe('100');
    });
  });

  it('debe calcular el total correctamente', async () => {
    render(
      <ModalNuevaVenta
        isOpen={true}
        onClose={mockOnClose}
        onSuccess={mockOnSuccess}
      />
    );

    await waitFor(() => {
      expect(screen.getByLabelText(/cantidad/i)).toBeInTheDocument();
    });

    const cantidadInput = screen.getByLabelText(/cantidad/i);
    const precioInput = screen.getByLabelText(/precio unitario/i);

    fireEvent.change(cantidadInput, { target: { value: '5' } });
    fireEvent.change(precioInput, { target: { value: '100' } });

    await waitFor(() => {
      expect(screen.getByText(/Total:/i)).toBeInTheDocument();
      expect(screen.getByText(/\$500\.00/)).toBeInTheDocument();
    });
  });

  it('debe llamar a ventasAPI.createAdmin al enviar el formulario', async () => {
    vi.mocked(api.ventasAPI.createAdmin).mockResolvedValueOnce({
      id: 1,
      producto_id: 1,
      vendedor_id: 1,
      cantidad: 5,
      precio_unitario: 100,
      precio_total: 500,
      comision: 50,
      fecha_venta: '2025-10-28',
    });

    render(
      <ModalNuevaVenta
        isOpen={true}
        onClose={mockOnClose}
        onSuccess={mockOnSuccess}
      />
    );

    await waitFor(() => {
      expect(screen.getByLabelText(/producto/i)).toBeInTheDocument();
    });

    fireEvent.change(screen.getByLabelText(/producto/i), { target: { value: '1' } });
    fireEvent.change(screen.getByLabelText(/vendedor/i), { target: { value: '1' } });
    fireEvent.change(screen.getByLabelText(/cantidad/i), { target: { value: '5' } });
    fireEvent.change(screen.getByLabelText(/precio unitario/i), { target: { value: '100' } });

    const submitButton = screen.getByRole('button', { name: /guardar/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(api.ventasAPI.createAdmin).toHaveBeenCalledWith({
        producto_id: 1,
        vendedor_id: 1,
        cantidad: 5,
        precio_unitario: 100,
      });
      expect(mockOnSuccess).toHaveBeenCalled();
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it('debe mostrar error si falla la creación de venta', async () => {
    vi.mocked(api.ventasAPI.createAdmin).mockRejectedValueOnce({
      response: {
        status: 404,
        data: { detail: 'Producto no encontrado' },
      },
    });

    render(
      <ModalNuevaVenta
        isOpen={true}
        onClose={mockOnClose}
        onSuccess={mockOnSuccess}
      />
    );

    await waitFor(() => {
      expect(screen.getByLabelText(/producto/i)).toBeInTheDocument();
    });

    fireEvent.change(screen.getByLabelText(/producto/i), { target: { value: '1' } });
    fireEvent.change(screen.getByLabelText(/vendedor/i), { target: { value: '1' } });
    fireEvent.change(screen.getByLabelText(/cantidad/i), { target: { value: '5' } });
    fireEvent.change(screen.getByLabelText(/precio unitario/i), { target: { value: '100' } });

    const submitButton = screen.getByRole('button', { name: /guardar/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/Producto no encontrado/i)).toBeInTheDocument();
      expect(mockOnSuccess).not.toHaveBeenCalled();
      expect(mockOnClose).not.toHaveBeenCalled();
    });
  });
});
