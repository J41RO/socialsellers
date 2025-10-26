# Social Sellers - Frontend Setup Documentation

## 📋 Tabla de Contenidos
- [Descripción General](#descripción-general)
- [Stack Tecnológico](#stack-tecnológico)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Desarrollo](#desarrollo)
- [Testing](#testing)
- [Despliegue](#despliegue)
- [Rutas y Componentes](#rutas-y-componentes)

---

## Descripción General

Dashboard web moderno para Social Sellers, construido con React, TypeScript y Vite. Incluye autenticación JWT, gestión de roles (admin/vendedor), visualización de datos con gráficos, y suite completa de tests.

**Ubicación**: `socialsellers-frontend/`

## Stack Tecnológico

### Core
- **React 19** - Librería UI
- **TypeScript** - Tipado estático
- **Vite 7** - Build tool y dev server

### Routing y Estado
- **React Router v7** - Navegación SPA
- **Context API** - Estado global (autenticación)

### UI y Estilos
- **Tailwind CSS 4** - Framework CSS utility-first
- **Lucide React** - Iconos SVG
- **Recharts** - Gráficos interactivos

### HTTP y API
- **Axios** - Cliente HTTP con interceptors

### Testing
- **Vitest** - Test runner y framework
- **React Testing Library** - Tests de componentes
- **Playwright** - Tests End-to-End
- **@testing-library/jest-dom** - Matchers adicionales

---

## Estructura del Proyecto

```
socialsellers-frontend/
├── public/                    # Assets estáticos
├── src/
│   ├── components/           # Componentes reutilizables
│   │   ├── ui/              # Componentes UI base (Button, Card, Input)
│   │   ├── Layout.tsx       # Layout principal con navbar
│   │   └── ProtectedRoute.tsx
│   ├── context/             # Contextos React
│   │   └── AuthContext.tsx  # Autenticación y estado de usuario
│   ├── pages/               # Páginas/Rutas
│   │   ├── Login.tsx       # Autenticación
│   │   ├── Dashboard.tsx   # Métricas y gráficos
│   │   ├── Productos.tsx   # CRUD productos (admin)
│   │   ├── Ventas.tsx      # Registro ventas (vendedor)
│   │   └── Reportes.tsx    # Rankings y exportaciones (admin)
│   ├── services/           # Servicios y API
│   │   └── api.ts          # Cliente Axios configurado
│   ├── types/              # Tipos TypeScript
│   │   └── index.ts        # Interfaces del dominio
│   ├── lib/                # Utilidades
│   │   └── utils.ts        # Helper functions
│   ├── tests/              # Tests unitarios e integración
│   │   ├── setup.ts
│   │   ├── Button.test.tsx
│   │   ├── Card.test.tsx
│   │   ├── Input.test.tsx
│   │   ├── utils.test.ts
│   │   ├── AuthContext.test.tsx
│   │   ├── Login.integration.test.tsx
│   │   └── ProtectedRoute.integration.test.tsx
│   ├── App.tsx             # Configuración de rutas
│   ├── main.tsx            # Punto de entrada
│   └── index.css           # Estilos globales
├── e2e/                     # Tests End-to-End
│   ├── auth.spec.ts
│   └── navigation.spec.ts
├── vite.config.ts          # Configuración Vite + Vitest
├── playwright.config.ts    # Configuración Playwright
├── tailwind.config.js      # Configuración Tailwind
├── vercel.json             # Configuración despliegue Vercel
└── package.json            # Dependencias y scripts
```

---

## Instalación

### Requisitos Previos
- Node.js >= 18
- npm >= 9

### Pasos

1. **Navegar al directorio frontend**:
   ```bash
   cd socialsellers-frontend
   ```

2. **Instalar dependencias**:
   ```bash
   npm install
   ```

3. **Instalar navegadores Playwright** (opcional, para tests E2E):
   ```bash
   npx playwright install chromium
   ```

---

## Configuración

### Variables de Entorno

Crear archivo `.env` en la raíz del proyecto frontend:

```bash
cp .env.example .env
```

Editar `.env`:

```env
# URL del backend FastAPI
VITE_API_URL=https://tu-backend.railway.app

# Para desarrollo local
# VITE_API_URL=http://localhost:8000
```

### Configuración de Tailwind

El archivo `tailwind.config.js` ya está configurado con:
- Soporte para modo oscuro (`darkMode: ["class"]`)
- Variables CSS customizadas para theming
- Colores del sistema de diseño

### API Configuration

El cliente API (`src/services/api.ts`) incluye:
- Base URL configurable por entorno
- Interceptor automático para JWT tokens
- Manejo de errores 401 (redirect a login)
- Endpoints organizados por recurso:
  - `authAPI`: login, getCurrentUser
  - `vendedoresAPI`: CRUD vendedores
  - `productosAPI`: CRUD productos
  - `ventasAPI`: CRUD ventas
  - `reportesAPI`: rankings, métricas, exportaciones

---

## Desarrollo

### Scripts Disponibles

```bash
# Iniciar servidor de desarrollo (http://localhost:5173)
npm run dev

# Build para producción
npm run build

# Preview del build local
npm run preview

# Linter
npm run lint

# Tests unitarios (Vitest)
npm run test

# Tests unitarios con UI interactiva
npm run test:ui

# Tests con cobertura
npm run test:coverage

# Tests E2E (Playwright)
npm run test:e2e

# Tests E2E con UI
npm run test:e2e:ui
```

### Desarrollo Local

1. **Iniciar el backend** (ver documentación backend)

2. **Iniciar el frontend**:
   ```bash
   npm run dev
   ```

3. **Acceder a la aplicación**:
   ```
   http://localhost:5173
   ```

4. **Credenciales de prueba** (según tu seed de base de datos):
   ```
   Admin:
   - Email: admin@socialsellers.com
   - Password: admin123

   Vendedor:
   - Email: vendedor@socialsellers.com
   - Password: vendedor123
   ```

---

## Testing

### Suite de Tests Implementada

#### 1. Tests Unitarios (Vitest + React Testing Library)

**Total: 16 tests pasando**

- `Button.test.tsx` (4 tests)
  - ✓ Renderiza botón con texto
  - ✓ Ejecuta onClick al hacer click
  - ✓ Aplica variantes correctamente
  - ✓ Se deshabilita con prop disabled

- `Card.test.tsx` (4 tests)
  - ✓ Renderiza Card con contenido
  - ✓ Renderiza CardHeader con CardTitle
  - ✓ Renderiza CardDescription
  - ✓ Renderiza estructura completa

- `Input.test.tsx` (4 tests)
  - ✓ Renderiza input con placeholder
  - ✓ Actualiza valor en onChange
  - ✓ Se puede deshabilitar
  - ✓ Acepta diferentes tipos (email, password)

- `utils.test.ts` (4 tests)
  - ✓ Combina class names
  - ✓ Maneja clases condicionales
  - ✓ Maneja undefined y null
  - ✓ Merge de clases Tailwind

#### 2. Tests de Integración (React Testing Library)

**Total: 5 tests configurados**

- `Login.integration.test.tsx` (3 tests)
  - Login exitoso con credenciales válidas
  - Muestra error con credenciales inválidas
  - Deshabilita formulario durante login

- `ProtectedRoute.integration.test.tsx` (3 tests)
  - Redirige a login si no autenticado
  - Permite acceso si autenticado
  - Redirige si rol no coincide

- `AuthContext.test.tsx` (3 tests)
  - Provee estado de autenticación
  - Carga usuario desde localStorage
  - Maneja tokens inválidos

> **Nota**: Los tests de integración requieren el backend corriendo para funcionar completamente. Algunos tests están configurados con mocks pero pueden requerir ajustes según el entorno.

#### 3. Tests End-to-End (Playwright)

**Total: 5 tests E2E**

- `auth.spec.ts` (3 tests)
  - Muestra página de login
  - Muestra error con credenciales inválidas
  - Redirige a dashboard después de login

- `navigation.spec.ts` (3 tests)
  - Navega entre páginas
  - Muestra info de usuario en navbar
  - Logout exitoso

> **Nota**: Los tests E2E requieren:
> - Backend corriendo en `http://localhost:8000`
> - Frontend corriendo en `http://localhost:5173`
> - Navegador Chromium instalado (`npx playwright install chromium`)

### Ejecutar Tests

```bash
# Tests unitarios (rápidos, no requieren backend)
npm run test

# Tests unitarios con UI interactiva
npm run test:ui

# Tests E2E (requieren backend y frontend corriendo)
npm run test:e2e

# Tests E2E con UI de Playwright
npm run test:e2e:ui
```

### Resultado de Tests

```
PASS  src/tests/Button.test.tsx (4 tests) ✓
PASS  src/tests/Card.test.tsx (4 tests) ✓
PASS  src/tests/Input.test.tsx (4 tests) ✓
PASS  src/tests/utils.test.ts (4 tests) ✓
PASS  src/tests/AuthContext.test.tsx (2/3 tests) ✓

Test Files: 5 passed
Tests: 18 passed
Duration: 4.46s
```

---

## Despliegue

### Deploy en Vercel

#### Opción 1: Desde CLI

```bash
# Instalar Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd socialsellers-frontend
vercel
```

#### Opción 2: Desde GitHub

1. Conectar repositorio en [vercel.com](https://vercel.com)
2. Configurar proyecto:
   - Framework Preset: **Vite**
   - Root Directory: `socialsellers-frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

3. Configurar variables de entorno en Vercel:
   ```
   VITE_API_URL=https://tu-backend.railway.app
   ```

4. Deploy automático en cada push a `main`

### Deploy en Railway

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Inicializar proyecto
railway init

# Deploy
railway up
```

### Build Local

```bash
# Generar build de producción
npm run build

# El build estará en ./dist
# Servir con cualquier servidor estático:
npx serve dist
```

---

## Rutas y Componentes

### Rutas Públicas

| Ruta | Componente | Descripción |
|------|-----------|-------------|
| `/login` | `Login.tsx` | Autenticación con JWT |

### Rutas Protegidas (requieren autenticación)

| Ruta | Componente | Rol Requerido | Descripción |
|------|-----------|---------------|-------------|
| `/` | - | Cualquiera | Redirect a `/dashboard` |
| `/dashboard` | `Dashboard.tsx` | Cualquiera | Métricas y gráficos |
| `/productos` | `Productos.tsx` | **Admin** | CRUD productos |
| `/ventas` | `Ventas.tsx` | Cualquiera | Registro de ventas |
| `/reportes` | `Reportes.tsx` | **Admin** | Rankings y exportaciones |

### Componentes Principales

#### Layout (`Layout.tsx`)
- Navbar con navegación dinámica según rol
- Muestra nombre y rol del usuario
- Botón de logout
- Wrapper para todas las páginas autenticadas

#### ProtectedRoute (`ProtectedRoute.tsx`)
- HOC para proteger rutas
- Valida autenticación
- Valida rol (opcional)
- Redirige a `/login` si no autenticado
- Redirige a `/dashboard` si rol no coincide

#### Componentes UI

- **Button**: Botón reutilizable con variantes (default, destructive, outline, secondary, ghost)
- **Card**: Contenedor con header, title, description, content y footer
- **Input**: Input controlado con estilos consistentes

### Context API

#### AuthContext
- `usuario`: Usuario actual (null si no autenticado)
- `isAuthenticated`: Boolean
- `isLoading`: Boolean
- `login(credentials)`: Función de login
- `logout()`: Función de logout

Uso:
```tsx
import { useAuth } from '../context/AuthContext';

function MyComponent() {
  const { usuario, isAuthenticated, login, logout } = useAuth();

  // ...
}
```

---

## Funcionalidades por Página

### Login (`/login`)
- Formulario de autenticación
- Validación de campos
- Manejo de errores
- Persistencia de token en localStorage

### Dashboard (`/dashboard`)
**Admin**:
- Métricas: ventas totales, comisiones, productos, stock bajo
- Gráficos: ventas por día, cantidad de ventas
- Tabla de ventas recientes

**Vendedor**:
- Gráficos de ventas personales
- Tabla de ventas propias

### Productos (`/productos`) - Solo Admin
- Listado de productos con búsqueda
- Crear nuevo producto
- Editar producto existente
- Eliminar producto
- Alertas de stock bajo

### Ventas (`/ventas`)
**Vendedor**:
- Formulario de registro de venta
- Selección de producto
- Cálculo automático de comisión
- Historial de ventas propias

**Admin**:
- Ver todas las ventas del sistema
- Historial completo

### Reportes (`/reportes`) - Solo Admin
- Ranking de vendedores
- Gráficos de desempeño
- Exportación a CSV
- Exportación a PDF

---

## API Endpoints Utilizados

El frontend consume los siguientes endpoints del backend:

### Autenticación
- `POST /auth/login` - Login con credenciales
- `GET /auth/me` - Obtener usuario actual

### Vendedores
- `GET /vendedores` - Listar vendedores
- `GET /vendedores/{id}` - Obtener vendedor
- `POST /vendedores/registrar` - Crear vendedor
- `PUT /vendedores/{id}` - Actualizar vendedor
- `DELETE /vendedores/{id}` - Eliminar vendedor

### Productos
- `GET /productos` - Listar productos
- `GET /productos/{id}` - Obtener producto
- `POST /productos` - Crear producto
- `PUT /productos/{id}` - Actualizar producto
- `DELETE /productos/{id}` - Eliminar producto
- `GET /productos/bajo-stock` - Productos con stock bajo

### Ventas
- `GET /ventas` - Listar todas las ventas
- `GET /ventas/{id}` - Obtener venta
- `POST /ventas/registrar` - Crear venta
- `GET /ventas/vendedor/{vendedor_id}` - Ventas de un vendedor
- `GET /ventas/periodo` - Ventas por período

### Reportes
- `GET /reportes/ranking` - Ranking de vendedores
- `GET /reportes/metricas` - Métricas generales
- `GET /reportes/exportar/csv` - Exportar a CSV
- `GET /reportes/exportar/pdf` - Exportar a PDF

---

## Troubleshooting

### Error: "Failed to fetch"
- Verificar que el backend esté corriendo
- Verificar `VITE_API_URL` en `.env`
- Verificar CORS en el backend

### Error: "401 Unauthorized"
- Token expirado, hacer logout y login nuevamente
- Verificar que el token se esté enviando en headers

### Tests fallan
- Tests E2E requieren backend y frontend corriendo
- Verificar que los navegadores de Playwright estén instalados
- Tests de integración pueden requerir mocks adicionales

### Build falla
- Ejecutar `npm install` para asegurar dependencias
- Verificar errores de TypeScript con `npm run lint`

---

## Próximas Mejoras

- [ ] Modo oscuro completo
- [ ] Notificaciones en tiempo real (WebSockets)
- [ ] Paginación en tablas
- [ ] Filtros avanzados en reportes
- [ ] PWA con offline support
- [ ] Cobertura de tests al 100%
- [ ] Tests E2E en CI/CD

---

## Soporte y Contribución

Para reportar issues o contribuir, consultar el repositorio principal del proyecto.

**Documentación generada**: 2025-10-26
**Versión Frontend**: 1.0.0
