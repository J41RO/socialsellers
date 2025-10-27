"""
Social Sellers Backend - FastAPI Application
Entry point para la API de vendedores sociales
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Social Sellers API",
    description="API para gestión de vendedores sociales - Mesctocker v2",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    """Endpoint raíz - verificación de API activa"""
    return {"mensaje": "API Social Sellers activa"}

# Routers
# from app.routers import sellers, auth, admin, productos, ventas, reportes, notificaciones
# app.include_router(sellers.router)
# app.include_router(auth.router)
# app.include_router(admin.router)
# app.include_router(productos.router)
# app.include_router(ventas.router)
# app.include_router(reportes.router)
# app.include_router(reportes.comisiones_router)
# app.include_router(notificaciones.router)
