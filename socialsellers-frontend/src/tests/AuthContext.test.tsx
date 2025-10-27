import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { AuthProvider, useAuth } from '../context/AuthContext';

// Use vi.hoisted to ensure mocks are available before the mock factory runs
const mocks = vi.hoisted(() => ({
  get: vi.fn(),
  post: vi.fn(),
}));

vi.mock('axios', () => {
  return {
    default: {
      create: () => ({
        get: mocks.get,
        post: mocks.post,
        put: vi.fn(),
        delete: vi.fn(),
        interceptors: {
          request: { use: vi.fn(() => 0), eject: vi.fn() },
          response: { use: vi.fn(() => 0), eject: vi.fn() },
        },
      }),
    },
  };
});

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
    mocks.get.mockRejectedValue(new Error('No token'));

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

    // Mock axios GET request for /auth/me
    mocks.get.mockResolvedValue({ data: mockUser });

    // Set localStorage
    localStorage.setItem('access_token', 'fake-token');
    localStorage.setItem('usuario', JSON.stringify(mockUser));

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    // Wait for authentication to complete
    const userText = await screen.findByText('User: Test User', {}, { timeout: 5000 });
    const authText = await screen.findByText('Authenticated: Yes', {}, { timeout: 5000 });

    expect(userText).toBeInTheDocument();
    expect(authText).toBeInTheDocument();
  });

  it('handles invalid token gracefully', async () => {
    localStorage.setItem('access_token', 'invalid-token');
    localStorage.setItem('usuario', JSON.stringify({ nombre: 'Test' }));

    mocks.get.mockRejectedValue(new Error('Unauthorized'));

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
