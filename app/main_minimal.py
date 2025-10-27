"""
Social Sellers Backend - MINIMAL VERSION FOR TESTING
Esta versión NO importa database ni models para diagnosticar el problema 502
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Social Sellers API - MINIMAL",
    description="Versión mínima para diagnosticar 502 Bad Gateway",
    version="1.0.0-minimal"
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
    return {
        "mensaje": "API Social Sellers activa (versión minimal)",
        "version": "1.0.0-minimal",
        "status": "operational"
    }

@app.get("/health")
def health_check():
    """Health check endpoint para Railway"""
    return {
        "status": "healthy",
        "service": "social-sellers-minimal"
    }

@app.get("/test")
def test_endpoint():
    """Endpoint de prueba adicional"""
    return {
        "test": "success",
        "message": "FastAPI está funcionando correctamente"
    }
