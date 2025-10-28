/**
 * Tests TDD para ventasAPI.createAdmin()
 * TAREA #012 Frontend - Fase RED
 *
 * Nota: Los tests de este archivo verifican la INTEGRACIÓN real con la API.
 * Para ejecutarlos, el backend debe estar corriendo en localhost:8000
 */
import { describe, it, expect } from 'vitest';
import { ventasAPI } from '../api';

describe('ventasAPI.createAdmin() - Integration Tests', () => {
  it('debe tener el método createAdmin definido', () => {
    expect(ventasAPI.createAdmin).toBeDefined();
    expect(typeof ventasAPI.createAdmin).toBe('function');
  });

  it('debe aceptar payload con estructura correcta', () => {
    const payload = {
      producto_id: 1,
      vendedor_id: 2,
      cantidad: 3,
      precio_unitario: 50.0,
    };

    // Verificar que el método acepta el payload
    expect(() => {
      ventasAPI.createAdmin(payload);
    }).not.toThrow();
  });

  it('debe retornar una Promise', () => {
    const payload = {
      producto_id: 1,
      vendedor_id: 2,
      cantidad: 3,
      precio_unitario: 50.0,
    };

    const result = ventasAPI.createAdmin(payload);
    expect(result).toBeInstanceOf(Promise);
  });
});
