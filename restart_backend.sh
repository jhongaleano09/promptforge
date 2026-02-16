#!/bin/bash

echo "=========================================="
echo "Script de Reinicio del Backend"
echo "=========================================="
echo ""

# Detener procesos existentes del backend en puerto 8001
echo "📋 Buscando procesos del backend en puerto 8001..."
BACKEND_PID=$(lsof -ti:8001 2>/dev/null)

if [ -n "$BACKEND_PID" ]; then
    echo "⚠️  Proceso encontrado (PID: $BACKEND_PID)"
    echo "🔴 Deteniendo proceso..."
    kill $BACKEND_PID
    sleep 2
    echo "✅ Proceso detenido"
else
    echo "✅ No hay procesos corriendo en puerto 8001"
fi

echo ""

# Ir al directorio del backend
cd backend

# Activar entorno virtual
if [ -d "venv" ]; then
    echo "📦 Activando entorno virtual..."
    source venv/bin/activate
    echo "✅ Entorno virtual activado"
    echo ""
fi

# Verificar tabla api_keys antes de iniciar
echo "📋 Verificando estado de la base de datos..."
python3 -c "import sqlite3; conn = sqlite3.connect('database.sqlite'); cursor = conn.cursor(); cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\" ORDER BY name;'); tables = [row[0] for row in cursor.fetchall()]; print('Tablas:', tables); print('Existe api_keys:', 'api_keys' in tables); conn.close()" 2>/dev/null || echo "⚠️  No se pudo verificar la base de datos"

echo ""

# Iniciar el backend
echo "🚀 Iniciando el backend en puerto 8001..."
echo "=========================================="
echo ""

# Ejecutar el backend
python3 main.py
