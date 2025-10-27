# Social Sellers MVP - Full Stack Application

**Versión: 1.0.0-mvp**

Sistema completo de gestión de vendedores sociales con dashboard interactivo, gestión de inventario, ventas y reportes.

## 🎯 Estado del Proyecto

- ✅ **MVP Completado**
- ✅ **Tests: Backend 35/35 (100%), Frontend 25/29 (86%)**
- ✅ **Cobertura: 91%**
- ✅ **Preparado para deploy público**

## Stack Tecnológico

- **FastAPI** - Framework web
- **SQLAlchemy** - ORM
- **PostgreSQL** - Base de datos (Railway)
- **Python 3.11**
- **Alembic** - Migraciones de BD
- **Pydantic v2** - Validación de datos
- **Docker** - Containerización

## Instalación

```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con credenciales de Railway
```

## Ejecución

```bash
# Modo desarrollo
uvicorn app.main:app --reload

# Modo producción
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Testing

```bash
# Ejecutar todos los tests
pytest -v

# Ejecutar test específico
pytest tests/test_sellers.py -v
```

## Documentación API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Estructura del Proyecto

```
socialseller/
├── app/
│   ├── main.py          # Entry point FastAPI
│   ├── database.py      # Configuración BD
│   ├── models.py        # Modelos SQLAlchemy
│   ├── schemas.py       # Schemas Pydantic
│   ├── crud.py          # Operaciones BD
│   └── routers/         # Endpoints por módulo
├── tests/               # Tests con Pytest
├── docs/                # Documentación del proyecto
│   └── bitacora_proyecto.md
└── requirements.txt
```

## Metodología

- **TDD (Test-Driven Development)**
- Un endpoint = un test primero
- Deploy solo si todos los tests pasan

## Roles del Proyecto

- **Estratega**: GPT-5 (Arquitectura y decisiones)
- **Ejecutor**: Claude Code (Implementación)
- **Validador**: Jairo Colina (Revisión final)
