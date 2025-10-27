# 🚀 INSTRUCCIONES DE DEPLOY MVP - Social Sellers

## ✅ PREPARACIÓN COMPLETADA

### Backend (Railway)
- ✅ Proyecto creado: `socialsellers-mvp`
- ✅ URL: https://railway.com/project/730d41c4-5414-48ea-9504-7c403cf6407b
- ✅ Configuración: Procfile, runtime.txt, railway.json

### Frontend (Vercel)  
- ✅ Configuración: .env.production con VITE_API_URL

### Tests
- ✅ Backend: 35/35 tests PASSED (91% cobertura)
- ✅ Frontend: 25/29 tests PASSED (86%)

---

## 📋 PASOS PENDIENTES (Requieren UI web)

### 1. COMPLETAR SETUP RAILWAY (Web UI)

Ir a: https://railway.com/project/730d41c4-5414-48ea-9504-7c403cf6407b

1. **Agregar Base de Datos PostgreSQL**:
   - Click "New" → "Database" → "Add PostgreSQL"
   - Esperar que se provisione

2. **Crear Servicio Backend**:
   - Click "New" → "GitHub Repo" → Conectar `J41RO/socialsellers`
   - O usar "Empty Service" y conectar después

3. **Configurar Variables de Entorno**:
   ```
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   APP_ENV=production
   SECRET_KEY=<generar con: openssl rand -hex 32>
   PYTHONPATH=/app
   ```

4. **Deploy**:
   - Railway detectará automáticamente Procfile y railway.json
   - Esperar a que termine el build
   - Copiar la URL pública generada (ej: `https://socialsellers-mvp-production.up.railway.app`)

5. **Probar Endpoint**:
   ```bash
   curl https://<TU-URL-RAILWAY>/
   curl https://<TU-URL-RAILWAY>/auth/me
   ```

6. **Ejecutar Seed Data** (opcional):
   ```bash
   railway run python -c "from app.database import SessionLocal; from app.crud import seed_database; db = SessionLocal(); seed_database(db); db.close()"
   ```

---

### 2. DEPLOY FRONTEND EN VERCEL

1. **Ir a**: https://vercel.com/new

2. **Import Git Repository**:
   - Conectar cuenta GitHub
   - Seleccionar repositorio `J41RO/socialsellers`
   - Framework Preset: Vite

3. **Configurar Build Settings**:
   - **Root Directory**: `socialsellers-frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

4. **Variables de Entorno**:
   ```
   VITE_API_URL=<TU-URL-RAILWAY-BACKEND>
   ```
   (Usar la URL de Railway del paso anterior)

5. **Deploy**:
   - Click "Deploy"
   - Esperar build
   - Copiar URL pública generada (ej: `https://socialsellers-mvp.vercel.app`)

---

### 3. ACTUALIZAR .env.production

Una vez tengas la URL de Railway, actualizar:

```bash
# socialsellers-frontend/.env.production
VITE_API_URL=https://<TU-URL-RAILWAY>
```

Luego:
```bash
git add socialsellers-frontend/.env.production
git commit -m "chore: actualizar URL Railway en .env.production"
```

Y hacer redeploy en Vercel.

---

### 4. PRUEBA E2E PÚBLICA

1. **Acceder a URL Vercel**: `https://<TU-URL-VERCEL>`

2. **Login como Admin**:
   - Email: `admin@socialsellers.com`
   - Password: `admin123`

3. **Validar Funcionalidad**:
   - ✅ Dashboard carga con métricas
   - ✅ Productos listados
   - ✅ Ventas registradas
   - ✅ Reportes funcionando
   - ✅ Centro de Notificaciones responde

4. **Capturar Evidencia**:
   - Screenshots de Dashboard
   - Screenshot de Login exitoso
   - Screenshot de Reportes

---

### 5. ACTUALIZAR BITÁCORA

Registrar en `docs/bitacora_proyecto.md`:

```markdown
## ✅ TAREA #MVP-VALIDACIÓN Y DEPLOY PÚBLICO COMPLETADA

**Fecha**: 2025-10-27

### Resultados Auditoría
- Backend: 35/35 tests (100%), 91% cobertura
- Frontend: 25/29 tests (86%)

### Deploy Completado
- **Backend Railway**: <TU-URL-RAILWAY>
- **Frontend Vercel**: <TU-URL-VERCEL>
- **Base de Datos**: PostgreSQL en Railway

### Credenciales Demo
- Admin: admin@socialsellers.com / admin123
- Vendedor: vendedor@socialsellers.com / vendedor123

### Versión
- **v1.0.0 - MVP Release**
```

---

## 🔧 TROUBLESHOOTING

### Backend no inicia en Railway
1. Verificar logs: `railway logs`
2. Verificar DATABASE_URL está configurada
3. Verificar Procfile existe en root

### Frontend no conecta con Backend
1. Verificar VITE_API_URL en Vercel settings
2. Verificar CORS configurado en FastAPI main.py
3. Verificar Railway permite requests HTTPS

### Database no migra
1. Railway ejecuta automáticamente el código
2. Las tablas se crean con `Base.metadata.create_all()`
3. Verificar en Railway logs que SQLAlchemy ejecutó

---

## 📚 RECURSOS

- Railway Project: https://railway.com/project/730d41c4-5414-48ea-9504-7c403cf6407b
- GitHub Repo: https://github.com/J41RO/socialsellers
- Railway Docs: https://docs.railway.app/
- Vercel Docs: https://vercel.com/docs
