#!/usr/bin/env python3
"""
Script para poblar base de datos de producción con datos iniciales
Ejecutar: python -m app.scripts.seed_database
"""
import sys
from pathlib import Path

# Agregar root al path
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from app.database import SessionLocal, engine
from app.models import Base
from app.crud import seed_database

def main():
    """Ejecutar seed de base de datos"""
    print("=" * 60)
    print("📊 SEED DATABASE - Social Sellers MVP")
    print("=" * 60)
    
    # Crear tablas si no existen
    print("\n🔧 Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas/verificadas")
    
    # Poblar datos
    print("\n🌱 Poblando datos iniciales...")
    db = SessionLocal()
    try:
        seed_database(db)
        print("✅ Seed completado exitosamente")
        
        # Verificar
        from app.models import Usuario, Producto, Venta
        usuarios_count = db.query(Usuario).count()
        productos_count = db.query(Producto).count()
        ventas_count = db.query(Venta).count()
        
        print("\n📈 Datos en base de datos:")
        print(f"  - Usuarios: {usuarios_count}")
        print(f"  - Productos: {productos_count}")
        print(f"  - Ventas: {ventas_count}")
        
        if usuarios_count >= 2:
            print("\n👤 Usuarios creados:")
            for u in db.query(Usuario).all():
                print(f"  - {u.email} ({u.rol})")
        
        print("\n" + "=" * 60)
        print("✅ SEED COMPLETADO")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error durante seed: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
