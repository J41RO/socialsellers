# 🚀 PASOS FINALES DE DEPLOY PÚBLICO - Social Sellers MVP

**Estado Actual**: Código preparado ✅ | Railway proyecto creado ✅ | Esperando deploy manual

---

## ✅ PREREQUISITOS COMPLETADOS

- [x] Tests: Backend 35/35, Frontend 25/29
- [x] Cobertura: 91%
- [x] Archivos Railway: Procfile, runtime.txt, railway.json
- [x] Script seed: `app/scripts/seed_database.py`
- [x] Frontend .env.production template
- [x] Sistema validado localmente

---

## 📋 PASO 1: CONFIGURAR RAILWAY (Web UI)

### 1.1 Acceder al Proyecto
URL: https://railway.com/project/730d41c4-5414-48ea-9504-7c403cf6407b

### 1.2 Agregar PostgreSQL
1. Click "New" → "Database" → "PostgreSQL"
2. Esperar provisión (1-2 minutos)
3. Copiar variable `DATABASE_URL` generada

### 1.3 Conectar Repositorio GitHub
1. Click "New" → "GitHub Repo"
2. Autorizar Railway en GitHub si es necesario
3. Seleccionar: `J41RO/socialsellers`
4. Branch: `main`
5. Root Directory: `.` (raíz)

### 1.4 Configurar Variables de Entorno
En Settings → Variables, agregar:

```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
APP_ENV=production
SECRET_KEY=07c6cee12f3b7735211dfed8b96cf4936338466d7f6adcafef91be4fce72ed55
PYTHONPATH=/app
```

**Importante**: `DATABASE_URL` debe referenciar al servicio PostgreSQL creado en 1.2

### 1.5 Deploy Automático
- Railway detectará `Procfile` y `railway.json`
- Build iniciará automáticamente
- Esperar 3-5 minutos
- Copiar URL pública generada (ej: `https://socialsellers-mvp-production.up.railway.app`)

---

## 📋 PASO 2: POBLAR BASE DE DATOS PRODUCCIÓN

Una vez el deploy de Railway esté **ACTIVO**:

### 2.1 Ejecutar Seed desde Railway CLI

```bash
railway run python -m app.scripts.seed_database
```

**Output esperado**:
```
============================================================
📊 SEED DATABASE - Social Sellers MVP
============================================================

🔧 Creando tablas...
✅ Tablas creadas/verificadas

🌱 Poblando datos iniciales...
✅ Seed completado exitosamente

📈 Datos en base de datos:
  - Usuarios: 2
  - Productos: 3
  - Ventas: 5

👤 Usuarios creados:
  - admin@socialsellers.com (admin)
  - vendedor@socialsellers.com (vendedor)

============================================================
✅ SEED COMPLETADO
============================================================
```

---

## 📋 PASO 3: VALIDAR BACKEND PÚBLICO

### 3.1 Probar Endpoint /docs
Abrir en navegador:
```
https://<TU-URL-RAILWAY>/docs
```

Debe mostrar: Swagger UI de FastAPI ✅

### 3.2 Probar Endpoint /auth/login
En Swagger UI:
1. Expandir `POST /auth/login`
2. Click "Try it out"
3. Ingresar:
   ```json
   {
     "email": "admin@socialsellers.com",
     "password": "admin123"
   }
   ```
4. Ejecutar
5. Copiar `access_token` de la respuesta

### 3.3 Probar Endpoint /auth/me
1. Click "Authorize" (candado arriba a la derecha)
2. Pegar token: `Bearer <access_token>`
3. Expandir `GET /auth/me`
4. Ejecutar
5. Verificar respuesta 200 OK con datos de admin

---

## 📋 PASO 4: DEPLOY FRONTEND EN VERCEL

### 4.1 Acceder a Vercel
URL: https://vercel.com/new

### 4.2 Import Repository
1. Click "Import Git Repository"
2. Conectar cuenta GitHub si es necesario
3. Buscar: `J41RO/socialsellers`
4. Click "Import"

### 4.3 Configurar Build Settings

**Framework Preset**: Vite

**Build & Development Settings**:
- **Root Directory**: `socialsellers-frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install` (default)

### 4.4 Configurar Environment Variables
Agregar variable:

```
Name: VITE_API_URL
Value: https://<TU-URL-RAILWAY>
```

**Importante**: Usar la URL de Railway del Paso 1.5 (sin `/` al final)

### 4.5 Deploy
1. Click "Deploy"
2. Esperar build (2-3 minutos)
3. Copiar URL pública generada (ej: `https://socialsellers-mvp.vercel.app`)

---

## 📋 PASO 5: VALIDACIÓN E2E PÚBLICA

### 5.1 Acceder a Frontend Público
Abrir en navegador:
```
https://<TU-URL-VERCEL>
```

### 5.2 Login
Credenciales:
- **Email**: admin@socialsellers.com
- **Password**: admin123

### 5.3 Verificar Funcionalidades

#### Dashboard
- [ ] Métricas generales cargan correctamente
- [ ] Gráficos de ventas visibles
- [ ] Top productos muestra datos
- [ ] Top vendedores muestra datos

#### Productos
- [ ] Lista de productos carga
- [ ] Datos correctos (Shampoo, Acondicionador, Tratamiento)

#### Ventas
- [ ] Historial de ventas visible
- [ ] 5 ventas registradas

#### Reportes
- [ ] Ranking de vendedores funciona
- [ ] Métricas por período funcionan

#### Centro de Notificaciones
- [ ] Botón "Probar Notificaciones" visible (solo admin)
- [ ] Click ejecuta endpoint /notificaciones/test
- [ ] Respuesta muestra email_sent y whatsapp_sent

### 5.4 Verificar Consola del Navegador
Abrir DevTools (F12) → Console:
- [ ] Sin errores de conexión
- [ ] Sin errores 401/403/404/500
- [ ] Requests a backend exitosos (200 OK)

### 5.5 Capturar Screenshots
1. Dashboard principal
2. Login exitoso
3. Lista de productos
4. Centro de notificaciones activo

---

## 📋 PASO 6: REGISTRO FINAL Y TAG

### 6.1 Actualizar Bitácora

Agregar entrada en `docs/bitacora_proyecto.md`:

```markdown
### ✅ DEPLOY PÚBLICO COMPLETADO (TAREA #MVP-DEPLOY-FINAL)

**Fecha**: 27 de Octubre 2025

**URLs Productivas**:
- Backend Railway: https://<TU-URL-RAILWAY>
- Frontend Vercel: https://<TU-URL-VERCEL>

**Tests Finales**:
- Backend: 35/35 PASSED (100%)
- Frontend: 25/29 PASSED (86%)
- Cobertura: 91%

**Base de Datos**:
- PostgreSQL en Railway ✅
- Seed ejecutado ✅
- 2 usuarios, 3 productos, 5 ventas ✅

**Validación E2E Pública**:
- Login funcional ✅
- Dashboard carga datos ✅
- Reportes funcionan ✅
- Notificaciones activas ✅

**Versión**: v1.0.0 (MVP Release)
```

### 6.2 Commit y Tag

```bash
# Agregar cambios
git add app/scripts/ FINAL_DEPLOY_STEPS.md docs/bitacora_proyecto.md

# Commit
git commit -m "[RELEASE] v1.0.0 - Deploy público completado

URLs Productivas:
- Backend: https://<TU-URL-RAILWAY>
- Frontend: https://<TU-URL-VERCEL>

🤖 Generated with Claude Code"

# Crear tag
git tag -a v1.0.0 -m "MVP Release - Deploy público completado

Tests: 35/35 backend, 25/29 frontend
Cobertura: 91%
PostgreSQL Railway + Frontend Vercel
Sistema validado E2E en producción"

# Push
git push origin main
git push origin v1.0.0
```

---

## 🎉 CHECKLIST FINAL

- [ ] Railway: PostgreSQL agregado
- [ ] Railway: Repo GitHub conectado
- [ ] Railway: Variables de entorno configuradas
- [ ] Railway: Deploy exitoso, URL pública obtenida
- [ ] Railway: Seed ejecutado (`python -m app.scripts.seed_database`)
- [ ] Backend: /docs accesible públicamente
- [ ] Backend: /auth/login retorna token
- [ ] Backend: /auth/me retorna datos de usuario
- [ ] Vercel: Repo GitHub conectado
- [ ] Vercel: Build settings configurados (root: socialsellers-frontend)
- [ ] Vercel: VITE_API_URL configurada con URL Railway
- [ ] Vercel: Deploy exitoso, URL pública obtenida
- [ ] E2E: Login exitoso con admin@socialsellers.com
- [ ] E2E: Dashboard carga métricas
- [ ] E2E: Productos visibles
- [ ] E2E: Ventas históricas visibles
- [ ] E2E: Reportes funcionan
- [ ] E2E: Notificaciones test funciona
- [ ] E2E: Sin errores en consola del navegador
- [ ] Screenshots capturados
- [ ] Bitácora actualizada con URLs finales
- [ ] Git tag v1.0.0 creado
- [ ] Push a origin/main completado

---

## 📚 RECURSOS

- **Railway Project**: https://railway.com/project/730d41c4-5414-48ea-9504-7c403cf6407b
- **Vercel**: https://vercel.com/new
- **GitHub Repo**: https://github.com/J41RO/socialsellers
- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs

---

## 🔧 TROUBLESHOOTING

### Backend no inicia en Railway
- Verificar logs: `railway logs`
- Verificar DATABASE_URL está configurada
- Verificar Procfile existe en root del repo

### Seed falla
- Verificar DATABASE_URL apunta a PostgreSQL Railway
- Ejecutar manualmente: `railway run python -m app.scripts.seed_database`
- Revisar logs de Railway

### Frontend no conecta con Backend
- Verificar VITE_API_URL en Vercel settings
- Verificar URL Railway correcta (sin `/` al final)
- Verificar CORS en FastAPI (debe permitir origin Vercel)
- Verificar Network tab en DevTools del navegador

### Error 401 en /auth/me
- Token expirado o inválido
- Obtener nuevo token desde /auth/login
- Verificar formato: `Bearer <token>`

---

**🤖 Generado con Claude Code - Metodología TDD Estricta**
