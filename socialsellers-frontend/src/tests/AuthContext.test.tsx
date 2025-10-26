import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { AuthProvider, useAuth } from '../context/AuthContext';
import { authAPI } from '../services/api';

// Mock del módulo API
vi.mock('../services/api', () => ({
  authAPI: {
    login: vi.fn(),
    getCurrentUser: vi.fn(),
  },
}));

// Componente de prueba que usa el contexto
function TestComponent() {
  const { usuario, isAuthenticated, isLoading } = useAuth();

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      <div>Authenticated: {isAuthenticated ? 'Yes' : 'No'}</div>
      {usuario && <div>User: {usuario.nombre}</div>}
    </div>
  );
}

describe('AuthContext', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  it('provides authentication state', async () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Authenticated: No')).toBeInTheDocument();
    });
  });

  it('loads user from localStorage if token exists', async () => {
    const mockUser = { id: 1, nombre: 'Test User', email: 'test@test.com', rol: 'admin' as const, activo: true };
    localStorage.setItem('access_token', 'fake-token');
    localStorage.setItem('usuario', JSON.stringify(mockUser));

    (authAPI.getCurrentUser as any).mockResolvedValue(mockUser);

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('User: Test User')).toBeInTheDocument();
      expect(screen.getByText('Authenticated: Yes')).toBeInTheDocument();
    });
  });

  it('handles invalid token gracefully', async () => {
    localStorage.setItem('access_token', 'invalid-token');
    localStorage.setItem('usuario', JSON.stringify({ nombre: 'Test' }));

    (authAPI.getCurrentUser as any).mockRejectedValue(new Error('Unauthorized'));

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Authenticated: No')).toBeInTheDocument();
    });
  });
});
