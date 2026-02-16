#!/usr/bin/env python3
"""Script simple para verificar la migración de la base de datos."""

import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

try:
    from app.db.database import engine
    from app.db.models import ApiKey, Settings

    # Check if tables exist
    with engine.connect() as conn:
        result = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        )
        tables = [row[0] for row in result.fetchall()]

    print("\n=== Verificación de Base de Datos ===\n")
    print(f"Tablas encontradas: {tables}")

    # Check if api_keys table exists
    if 'api_keys' in tables:
        print("✅ Tabla 'api_keys' existe")

        # Check records in api_keys
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()

        try:
            apikeys = session.query(ApiKey).all()
            print(f"✅ Registros en 'api_keys': {len(apikeys)}")

            for key in apikeys:
                print(f"   - ID: {key.id}, Provider: {key.provider}, Active: {key.is_active}, Usage: {key.usage_count}")

        finally:
            session.close()
    else:
        print("❌ Tabla 'api_keys' NO existe - Migración no se ejecutó")

    # Check if settings table exists
    if 'settings' in tables:
        print("✅ Tabla 'settings' existe (compatibilidad v1.x)")

        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()

        try:
            settings = session.query(Settings).all()
            print(f"   Registros en 'settings': {len(settings)}")
        finally:
            session.close()
    else:
        print("⚠️  Tabla 'settings' no existe")

    print("\n=== Estado de Migración ===\n")

    if 'api_keys' in tables and len(apikeys) > 0:
        print("✅ Migración COMPLETADA")
        print("✅ La tabla api_keys tiene datos")
    elif 'api_keys' in tables and len(apikeys) == 0:
        print("⚠️  Migración INCOMPLETA")
        print("⚠️  La tabla api_keys existe pero no tiene datos")
    else:
        print("❌ Migración NO EJECUTADA")
        print("❌ La tabla api_keys no existe")

    print("\n=== Acciones Recomendadas ===\n")

    if 'api_keys' not in tables:
        print("📋 ACCIÓN: Ejecutar la migración manualmente")
        print("   Comando: cd backend && python3 migrations/002_migrate_to_api_keys.py")
    elif len(apikeys) == 0:
        print("📋 ACCIÓN: Ejecutar la migración para migrar datos de settings a api_keys")
        print("   Comando: cd backend && python3 migrations/002_migrate_to_api_keys.py")

except Exception as e:
    print(f"\n❌ Error al verificar base de datos: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
