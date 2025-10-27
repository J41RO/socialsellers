import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from '../context/AuthContext';
import ProtectedRoute from '../components/ProtectedRoute';

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

function AdminPage() {
  return <div>Admin Page</div>;
}

function LoginPage() {
  return <div>Login Page</div>;
}

function DashboardPage() {
  return <div>Dashboard Page</div>;
}

describe('ProtectedRoute Integration Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  it('redirects to login when not authenticated', async () => {
    mocks.get.mockRejectedValue(new Error('No token'));

    render(
      <MemoryRouter initialEntries={['/admin']}>
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/admin"
              element={
                <ProtectedRoute>
                  <AdminPage />
                </ProtectedRoute>
              }
            />
          </Routes>
        </AuthProvider>
      </MemoryRouter>
    );

    // Wait for loading to finish and redirect to happen
    await waitFor(() => {
      expect(screen.queryByText('Cargando...')).not.toBeInTheDocument();
    }, { timeout: 3000 });

    await waitFor(() => {
      expect(screen.getByText('Login Page')).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  it('allows access when authenticated', async () => {
    const mockUser = {
      id: 1,
      nombre: 'Test User',
      email: 'test@test.com',
      rol: 'admin' as const,
      activo: true,
    };

    // Mock axios GET request for /auth/me
    mocks.get.mockResolvedValue({ data: mockUser });

    localStorage.setItem('access_token', 'test-token');
    localStorage.setItem('usuario', JSON.stringify(mockUser));

    render(
      <MemoryRouter initialEntries={['/admin']}>
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/admin"
              element={
                <ProtectedRoute>
                  <AdminPage />
                </ProtectedRoute>
              }
            />
          </Routes>
        </AuthProvider>
      </MemoryRouter>
    );

    // Wait for authentication and page render
    const adminPage = await screen.findByText('Admin Page', {}, { timeout: 5000 });
    expect(adminPage).toBeInTheDocument();
  });

  it('redirects when role does not match required role', async () => {
    const mockUser = {
      id: 2,
      nombre: 'Vendedor Test',
      email: 'vendedor@test.com',
      rol: 'vendedor' as const,
      activo: true,
    };

    // Mock axios GET request for /auth/me
    mocks.get.mockResolvedValue({ data: mockUser });

    localStorage.setItem('access_token', 'test-token');
    localStorage.setItem('usuario', JSON.stringify(mockUser));

    render(
      <MemoryRouter initialEntries={['/admin']}>
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route
              path="/admin"
              element={
                <ProtectedRoute requiredRole="admin">
                  <AdminPage />
                </ProtectedRoute>
              }
            />
          </Routes>
        </AuthProvider>
      </MemoryRouter>
    );

    // Wait for redirect to dashboard
    const dashboardPage = await screen.findByText('Dashboard Page', {}, { timeout: 5000 });
    expect(dashboardPage).toBeInTheDocument();
  });
});
