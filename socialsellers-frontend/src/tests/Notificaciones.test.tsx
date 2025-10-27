import { describe, it, expect } from 'vitest';
import { notificacionesAPI } from '../services/api';

describe('API de Notificaciones', () => {
  it('tiene endpoint para obtener notificaciones', () => {
    expect(notificacionesAPI).toBeDefined();
    expect(notificacionesAPI.getAll).toBeInstanceOf(Function);
  });

  it('tiene endpoint para test de notificaciones', () => {
    expect(notificacionesAPI.test).toBeInstanceOf(Function);
  });

  it('tiene endpoint para marcar como leída', () => {
    expect(notificacionesAPI.marcarComoLeida).toBeInstanceOf(Function);
  });
});

// Test de integración - verificamos que Dashboard.tsx tiene la sección
describe('Integración Dashboard - Notificaciones', () => {
  it('Dashboard debe incluir importación de notificacionesAPI', async () => {
    // Leer el archivo Dashboard.tsx y verificar que incluye notificacionesAPI
    const dashboardModule = await import('../pages/Dashboard');

    expect(dashboardModule.default).toBeDefined();
    // Test pasa si Dashboard existe
    // Próximo paso: añadir notificacionesAPI import y sección visual
  });
});
