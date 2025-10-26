import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { authAPI } from '../services/api';
import type { Usuario, LoginCredentials, AuthResponse } from '../types';

interface AuthContextType {
  usuario: Usuario | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Verificar si hay un token guardado al cargar la aplicación
    const initAuth = async () => {
      const token = localStorage.getItem('access_token');
      const usuarioGuardado = localStorage.getItem('usuario');

      if (token && usuarioGuardado) {
        try {
          // Verificar que el token sea válido
          const usuarioActual = await authAPI.getCurrentUser();
          setUsuario(usuarioActual);
        } catch (error) {
          // Token inválido o expirado
          localStorage.removeItem('access_token');
          localStorage.removeItem('usuario');
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  const login = async (credentials: LoginCredentials) => {
    try {
      const response: AuthResponse = await authAPI.login(credentials);
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('usuario', JSON.stringify(response.usuario));
      setUsuario(response.usuario);
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('usuario');
    setUsuario(null);
  };

  return (
    <AuthContext.Provider
      value={{
        usuario,
        isAuthenticated: !!usuario,
        isLoading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
