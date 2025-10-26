# Social Sellers Dashboard - Frontend

Dashboard web para el sistema de gestión de ventas Social Sellers.

## Stack Tecnológico

- **React 18** + **TypeScript**
- **Vite** - Build tool
- **Tailwind CSS** - Estilos
- **React Router** - Navegación
- **Axios** - Cliente HTTP
- **Recharts** - Gráficos
- **Lucide React** - Iconos

## Estructura del Proyecto

```
src/
├── components/         # Componentes reutilizables
│   ├── ui/            # Componentes UI base
│   ├── Layout.tsx     # Layout principal
│   └── ProtectedRoute.tsx
├── context/           # Contextos React
│   └── AuthContext.tsx
├── pages/             # Páginas/Rutas
│   ├── Login.tsx
│   ├── Dashboard.tsx
│   ├── Productos.tsx
│   ├── Ventas.tsx
│   └── Reportes.tsx
├── services/          # Servicios API
│   └── api.ts
├── types/             # Tipos TypeScript
│   └── index.ts
└── lib/               # Utilidades
    └── utils.ts
```

## Instalación y Desarrollo

### 1. Instalar dependencias

```bash
npm install
```

### 2. Configurar variables de entorno

Crear archivo `.env` basado en `.env.example`:

```bash
cp .env.example .env
```

Editar `.env` con la URL de tu backend:

```
VITE_API_URL=https://tu-backend.railway.app
```

### 3. Iniciar servidor de desarrollo

```bash
npm run dev
```

El servidor estará disponible en `http://localhost:5173`

### 4. Build para producción

```bash
npm run build
```

## Despliegue en Vercel

### Opción 1: Desde la CLI

```bash
npm install -g vercel
vercel login
vercel
```

### Opción 2: Desde GitHub

1. Conectar repositorio en [vercel.com](https://vercel.com)
2. Configurar variable de entorno `VITE_API_URL`
3. Deploy automático en cada push

### Variables de entorno en Vercel

Configurar en el dashboard de Vercel:

- `VITE_API_URL` - URL del backend FastAPI

## Funcionalidades

### Autenticación
- Login con email y contraseña
- JWT Token en localStorage
- Rutas protegidas por autenticación
- Redirección automática según rol

### Roles

#### Admin
- Dashboard con métricas generales
- Gestión CRUD de productos
- Visualización de todas las ventas
- Reportes y rankings de vendedores
- Exportación de datos (CSV/PDF)

#### Vendedor
- Dashboard personal
- Registro de ventas
- Historial de ventas propias
- Visualización de comisiones

### Páginas

#### `/login`
Autenticación de usuarios

#### `/dashboard`
- Métricas principales (admin)
- Gráficos de ventas
- Tabla de ventas recientes

#### `/productos` (solo admin)
- Listado de productos
- Crear/editar/eliminar productos
- Alertas de stock bajo

#### `/ventas`
- Registro de nuevas ventas
- Historial de ventas
- Cálculo automático de comisiones

#### `/reportes` (solo admin)
- Ranking de vendedores
- Gráficos de desempeño
- Exportación de reportes

## Comandos Disponibles

```bash
npm run dev          # Servidor desarrollo
npm run build        # Build producción
npm run preview      # Preview build local
npm run lint         # Linter ESLint
```

## Dependencias Principales

```json
{
  "react": "^18.3.1",
  "react-router-dom": "^6.x",
  "axios": "^1.x",
  "recharts": "^2.x",
  "lucide-react": "^0.x",
  "tailwindcss": "^3.x"
}
```

## Configuración de API

Todas las llamadas a la API están centralizadas en `src/services/api.ts`:

- Interceptor automático para JWT
- Manejo de errores 401 (redirect a login)
- Base URL configurable por entorno

## Estilos

Sistema de diseño basado en Tailwind CSS con variables CSS para temas:

- Sistema light/dark preparado
- Componentes UI reutilizables
- Diseño responsivo mobile-first

## Próximas Mejoras

- [ ] Filtros avanzados en reportes
- [ ] Gráficos más interactivos
- [ ] Notificaciones en tiempo real
- [ ] Modo oscuro
- [ ] PWA offline support
- [ ] Tests E2E con Playwright
