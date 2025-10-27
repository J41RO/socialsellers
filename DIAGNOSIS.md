# DIAGNÓSTICO: Error 502 Bad Gateway en Railway

**Fecha**: 2025-10-26
**Servicio**: Social Sellers Backend (FastAPI + PostgreSQL)
**Plataforma**: Railway
**Estado Inicial**: Uvicorn inicia exitosamente pero requests HTTP devuelven 502

---

## 🔍 SÍNTOMAS

1. **Logs de Railway muestran**:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   INFO:     Application startup complete
   ```

2. **Comportamiento HTTP**:
   - Todos los requests devuelven `502 Bad Gateway`
   - Incluso el endpoint raíz `/` falla
   - Railway muestra el servicio como "Active" (verde)

3. **No hay errores visibles** en los logs de deployment

---

## 🐛 PROBLEMA IDENTIFICADO

### Causa Raíz #1: Conflicto entre Alembic y `Base.metadata.create_all()`

**Ubicación**: `app/main.py` línea 11

```python
# ❌ PROBLEMA
from app.database import engine, Base
from app import models

Base.metadata.create_all(bind=engine)  # Línea problemática
```

**Por qué falla**:

1. **Inconsistencia de Schema**:
   - Los modelos en `app/models.py` definen Foreign Keys:
     ```python
     class Venta(Base):
         producto_id = Column(Integer, ForeignKey("productos.id"))
         vendedor_id = Column(Integer, ForeignKey("usuarios.id"))
     ```

   - Pero la migración de Alembic NO creó esas FK (las removimos temporalmente):
     ```python
     # alembic/versions/56ffef2608ca_*.py
     op.create_table('ventas',
         sa.Column('producto_id', sa.Integer(), nullable=False),
         # ❌ SIN ForeignKeyConstraint
     )
     ```

2. **Ejecución en Module-Level**:
   - `Base.metadata.create_all()` se ejecuta al importar el módulo
   - Intenta crear tablas basándose en los modelos (CON FK)
   - Encuentra que las tablas ya existen (creadas por Alembic SIN FK)
   - Genera conflicto que causa un crash silencioso

3. **Timing del Error**:
   - Uvicorn inicia correctamente (antes de procesar requests)
   - El error ocurre cuando se intenta acceder a la base de datos
   - Railway no captura el error porque Uvicorn ya reportó "startup complete"

### Causa Raíz #2: Redundancia con Alembic

**Alembic ya maneja las migraciones**:
- Railway ejecuta `alembic upgrade head` en el startCommand
- Todas las tablas ya están creadas correctamente
- `Base.metadata.create_all()` es innecesario y causa conflictos

---

## ✅ SOLUCIÓN APLICADA

### Fix #1: Remover `Base.metadata.create_all()`

**Archivo**: `app/main.py`

```python
# ✅ ANTES (causaba el error)
from app.database import engine, Base
from app import models

Base.metadata.create_all(bind=engine)

# ✅ DESPUÉS (correcto)
# from app.database import engine, Base
# from app import models

# NOTA: Base.metadata.create_all() removido intencionalmente
# Usamos Alembic para migraciones de base de datos
# Ejecutar: alembic upgrade head
```

**Beneficios**:
- Elimina el conflicto entre Alembic y SQLAlchemy
- Confía en Alembic como única fuente de verdad para el schema
- Previene crashes silenciosos al iniciar

### Fix #2: Crear `main_minimal.py` para Testing

**Archivo creado**: `app/main_minimal.py`

Versión mínima de la aplicación SIN imports de database/models:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Social Sellers API - MINIMAL",
    version="1.0.0-minimal"
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)

@app.get("/")
def root():
    return {"mensaje": "API activa (minimal)", "status": "operational"}
```

**Uso**:
```bash
# Para probar si FastAPI funciona sin database
uvicorn app.main_minimal:app --host 0.0.0.0 --port 8000
```

---

## 🚀 PASOS PARA DESPLEGAR EL FIX

### Opción A: Deploy Inmediato (Recomendado)

```bash
cd ~/socialseller

# 1. Verificar cambios
git status
git diff app/main.py

# 2. Commit del fix
git add app/main.py app/main_minimal.py DIAGNOSIS.md
git commit -m "fix: remove Base.metadata.create_all() conflicting with Alembic"

# 3. Push a Railway
git push origin main
```

**Railway detectará el push automáticamente y redeployará.**

### Opción B: Testing Local Primero

```bash
# 1. Test con versión minimal (sin DB)
uvicorn app.main_minimal:app --reload

# Abrir: http://localhost:8000
# Verificar que carga correctamente

# 2. Test con versión corregida (con Alembic)
alembic upgrade head
uvicorn app.main:app --reload

# Verificar que /docs carga sin error

# 3. Deploy a Railway (mismo comando que Opción A)
```

---

## 📊 VERIFICACIÓN POST-DEPLOYMENT

### 1. Monitorear Logs de Railway

**Esperado** (exitoso):
```
Building...
✓ Installing dependencies
✓ Running: alembic upgrade head
INFO [alembic.runtime.migration] Running upgrade 126c3f44915f -> 56ffef2608ca
✓ Starting Uvicorn
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Application startup complete
INFO: 172.x.x.x:xxxxx - "GET / HTTP/1.1" 200 OK  ✅ SUCCESS
```

**NO debería aparecer**:
- ❌ `sqlalchemy.exc.ProgrammingError`
- ❌ `relation "productos" does not exist`
- ❌ `502 Bad Gateway`

### 2. Probar Endpoints

```bash
# Endpoint raíz
curl https://socialsellers-production.up.railway.app/

# Respuesta esperada:
{"mensaje": "API Social Sellers activa"}

# Health check
curl https://socialsellers-production.up.railway.app/docs

# Debe cargar Swagger UI correctamente
```

### 3. Verificar Database

Railway → Postgres → Data

**Tablas esperadas**:
- ✓ `usuarios`
- ✓ `vendedores`
- ✓ `productos`
- ✓ `ventas` (SIN FK por ahora)
- ✓ `alembic_version`

---

## 🔄 PRÓXIMOS PASOS (OPCIONAL)

### Reagregar Foreign Keys Correctamente

Una vez que la aplicación funcione:

```bash
# 1. Crear nueva migración
alembic revision -m "add foreign keys to ventas table"

# 2. Editar la nueva migración
# alembic/versions/[nueva_revision].py
def upgrade() -> None:
    op.create_foreign_key(
        'fk_ventas_producto_id',
        'ventas', 'productos',
        ['producto_id'], ['id']
    )
    op.create_foreign_key(
        'fk_ventas_vendedor_id',
        'ventas', 'usuarios',
        ['vendedor_id'], ['id']
    )

# 3. Commit y deploy
git add alembic/versions/[nueva_revision].py
git commit -m "feat: add foreign keys to ventas table"
git push origin main
```

---

## 📝 LECCIONES APRENDIDAS

### ❌ Anti-Patterns Evitados

1. **NO usar `Base.metadata.create_all()` con Alembic**
   - Causa conflictos de schema
   - Duplica responsabilidades
   - Oculta errores

2. **NO definir FK en migraciones que dependen de tablas no creadas**
   - Usar orden de creación correcto
   - O crear FK en migraciones separadas

3. **NO ejecutar operaciones de DB en module-level**
   - Usar eventos de startup de FastAPI
   - O confiar completamente en Alembic

### ✅ Best Practices Aplicadas

1. **Alembic como única fuente de verdad** para schema de DB
2. **Separación de concerns**: FastAPI para API, Alembic para migraciones
3. **Versión minimal** para testing y diagnóstico
4. **Documentación clara** de por qué se removió código

---

## 🛠️ ARCHIVOS MODIFICADOS

```
MODIFICADOS:
  app/main.py                    (removido Base.metadata.create_all)

CREADOS:
  app/main_minimal.py            (versión de testing)
  DIAGNOSIS.md                   (este archivo)

PENDIENTES:
  alembic/versions/56ffef2608ca  (ya corregido en commit anterior)
```

---

## 📞 SOPORTE

Si el problema persiste después del deployment:

1. **Capturar logs completos** de Railway (Build + Runtime)
2. **Verificar variable de entorno** `DATABASE_URL` en Railway
3. **Probar localmente** con la misma DATABASE_URL
4. **Usar main_minimal.py** para aislar el problema

---

## ✅ CHECKLIST DE DEPLOYMENT

- [ ] Commit realizado: `fix: remove Base.metadata.create_all()`
- [ ] Push a GitHub: `git push origin main`
- [ ] Railway detecta cambio y inicia build
- [ ] Build exitoso (verde en Railway)
- [ ] Deployment activo (verde en Railway)
- [ ] GET `/` retorna 200 OK
- [ ] GET `/docs` carga Swagger UI
- [ ] No hay errores 502 en logs

---

**Autor**: Claude Code (Ejecutor IA)
**Validado por**: Jairo
**Estado**: ✅ Fix aplicado, pendiente deployment
