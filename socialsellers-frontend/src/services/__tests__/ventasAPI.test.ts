/**
 * Tests TDD para ventasAPI.create()
 * TAREA #012 Frontend - Fase RED
 */
import { describe, it, expect, beforeEach, vi } from 'vitest';
import axios from 'axios';
import { ventasAPI } from '../api';

// Mock axios
vi.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('ventasAPI.create()', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Mock localStorage
    Storage.prototype.getItem = vi.fn(() => 'fake-jwt-token');
  });

  it('debe llamar a POST /ventas con payload correcto', async () => {
    const mockVenta = {
      id: 1,
      producto_id: 1,
      vendedor_id: 2,
      cantidad: 3,
      total: 150.0,
      fecha: '2025-10-28T10:00:00',
    };

    mockedAxios.post.mockResolvedValueOnce({ data: mockVenta });

    const payload = {
      producto_id: 1,
      vendedor_id: 2,
      cantidad: 3,
      precio_unitario: 50.0,
    };

    const result = await ventasAPI.create(payload);

    // Verificar que se llamó con los parámetros correctos
    expect(mockedAxios.post).toHaveBeenCalledWith('/ventas', payload);
    expect(result).toEqual(mockVenta);
  });

  it('debe incluir header Authorization con Bearer token', async () => {
    const mockVenta = {
      id: 1,
      producto_id: 1,
      vendedor_id: 2,
      cantidad: 3,
      total: 150.0,
      fecha: '2025-10-28T10:00:00',
    };

    mockedAxios.post.mockResolvedValueOnce({ data: mockVenta });

    const payload = {
      producto_id: 1,
      vendedor_id: 2,
      cantidad: 3,
      precio_unitario: 50.0,
    };

    await ventasAPI.create(payload);

    // El interceptor de axios debería agregar el token automáticamente
    // Verificamos que localStorage.getItem fue llamado
    expect(localStorage.getItem).toHaveBeenCalledWith('access_token');
  });

  it('debe propagar error si la API devuelve error', async () => {
    const errorResponse = {
      response: {
        status: 400,
        data: { detail: 'Cantidad debe ser mayor que 0' },
      },
    };

    mockedAxios.post.mockRejectedValueOnce(errorResponse);

    const payload = {
      producto_id: 1,
      vendedor_id: 2,
      cantidad: 0, // Cantidad inválida
      precio_unitario: 50.0,
    };

    await expect(ventasAPI.create(payload)).rejects.toEqual(errorResponse);
  });
});
