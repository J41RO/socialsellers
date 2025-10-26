"""
Configuración de base de datos
SQLAlchemy + PostgreSQL (Railway)
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Detección automática de entorno y carga de variables
env = os.getenv("APP_ENV", "development")
if env == "production":
    load_dotenv(".env.production")
else:
    load_dotenv()

# URL de base de datos desde variables de entorno
# Fallback a SQLite para testing si no está configurada
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Fix para Railway: reemplazar postgres:// con postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configuración específica para SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency para obtener sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
