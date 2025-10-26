import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from '../context/AuthContext';
import ProtectedRoute from '../components/ProtectedRoute';
import { authAPI } from '../services/api';

vi.mock('../services/api', () => ({
  authAPI: {
    login: vi.fn(),
    getCurrentUser: vi.fn(),
  },
}));

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
    render(
      <BrowserRouter>
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
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Login Page')).toBeInTheDocument();
    });
  });

  it('allows access when authenticated', async () => {
    const mockUser = {
      id: 1,
      nombre: 'Test User',
      email: 'test@test.com',
      rol: 'admin' as const,
      activo: true,
    };

    localStorage.setItem('access_token', 'test-token');
    localStorage.setItem('usuario', JSON.stringify(mockUser));
    (authAPI.getCurrentUser as any).mockResolvedValue(mockUser);

    render(
      <BrowserRouter>
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
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Admin Page')).toBeInTheDocument();
    });
  });

  it('redirects when role does not match required role', async () => {
    const mockUser = {
      id: 2,
      nombre: 'Vendedor Test',
      email: 'vendedor@test.com',
      rol: 'vendedor' as const,
      activo: true,
    };

    localStorage.setItem('access_token', 'test-token');
    localStorage.setItem('usuario', JSON.stringify(mockUser));
    (authAPI.getCurrentUser as any).mockResolvedValue(mockUser);

    render(
      <BrowserRouter>
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
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Dashboard Page')).toBeInTheDocument();
    });
  });
});
