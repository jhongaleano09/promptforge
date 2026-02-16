# 🐛 Solución de Errores - Fase 6.5

## Problemas Identificados

### 1. Error: "Not Found" al intentar listar API keys

**Causa Raíz:**
La tabla `api_keys` **no existía** en la base de datos.

**Por qué pasó:**
El modelo `ApiKey` estaba definido en `backend/app/db/models.py`, pero NO estaba importado en `backend/app/db/database.py`. Por lo tanto, cuando se ejecutaba `Base.metadata.create_all(bind=engine)` en `main.py`, SQLAlchemy solo creaba las tablas para los modelos importados en `database.py`, que era solo `Settings`.

**Verificación:**
```bash
$ cd backend
$ python3 -c "import sqlite3; conn = sqlite3.connect('database.sqlite'); cursor = conn.cursor(); cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\" ORDER BY name;'); tables = [row[0] for row in cursor.fetchall()]; print('Tablas:', tables); conn.close()"

Tablas: ['settings']
# ❌ La tabla api_keys NO existe
```

**Result:**
- Endpoint `/api/settings/keys` no podía funcionar porque la tabla no existía
- La migración automática falló silenciosamente porque no había tabla `api_keys` para migrar a

---

### 2. Problema: Puertos incorrectos en configuración

**Causa:**
El archivo `frontend/src/config/api.ts` tenía el puerto 8000 como fallback:
```typescript
export const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
```

**Por qué es incorrecto:**
Según la documentación (`PLANIFICACION_MAESTRA.md`), el backend debe correr en el puerto **8001**, no en 8000.

**Situación:**
- Puerto 8000: Tenía otra aplicación corriendo (no PromptForge)
- Puerto 8001: Tenía PromptForge corriendo pero sin la tabla `api_keys` creada

---

## ✅ Soluciones Implementadas

### 1. Importar ApiKey en database.py

**Archivo:** `backend/app/db/database.py`

**Cambio:**
```python
# ANTES:
class Base(DeclarativeBase):
    pass

# DESPUÉS:
class Base(DeclarativeBase):
    pass

# Import models to register them with Base.metadata
from app.db.models import Settings, ApiKey
```

**Por qué funciona:**
Al importar `ApiKey` en `database.py`, el modelo se registra automáticamente en `Base.metadata`. Ahora cuando se ejecuta `Base.metadata.create_all(bind=engine)` en `main.py`, la tabla `api_keys` se creará.

---

### 2. Corregir puerto por defecto en frontend

**Archivo:** `frontend/src/config/api.ts`

**Cambio:**
```typescript
// ANTES:
export const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// DESPUÉS:
export const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api';
```

**Por qué funciona:**
Ahora si el `.env.local` no está cargado, el frontend usará el puerto correcto (8001) por defecto.

---

## 🚀 Instrucciones para Solucionar el Problema

### Paso 1: Detener el backend actual

Si tienes el backend corriendo, deténlo:

**Opción A: Usar el script proporcionado**
```bash
chmod +x restart_backend.sh
./restart_backend.sh
```

**Opción B: Manualmente**
```bash
# Encontrar el proceso
ps aux | grep python3 | grep main.py

# Detener el proceso (reemplazar PID con el número correcto)
kill <PID>
```

### Paso 2: Iniciar el backend

```bash
cd backend

# Activar entorno virtual si existe
source venv/bin/activate

# Iniciar el backend
python3 main.py
```

**Deberías ver logs similares a:**
```
INFO:     Starting PromptForge API...
INFO:     Checking if migration from settings to api_keys is needed...
INFO:     Both tables exist. Checking if migration is needed...
INFO:     Migration appears to have already been completed
INFO:     ✅ Migration check completed successfully
INFO:     PromptForge API startup completed
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### Paso 3: Verificar que la tabla api_keys existe

```bash
cd backend
python3 -c "import sqlite3; conn = sqlite3.connect('database.sqlite'); cursor = conn.cursor(); cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\" ORDER BY name;'); tables = [row[0] for row in cursor.fetchall()]; print('✅ Tablas:', tables); print('✅ Existe api_keys:', 'api_keys' in tables); conn.close()"
```

**Deberías ver:**
```
✅ Tablas: ['api_keys', 'settings']
✅ Existe api_keys: True
```

### Paso 4: Verificar que el endpoint funciona

```bash
curl http://localhost:8001/api/settings/keys
```

**Deberías ver:**
```json
{
  "keys": []
}
```

(O con las keys que ya tengas configuradas)

### Paso 5: Probar en el frontend

1. Ir a http://localhost:3000/settings
2. Deberías ver la interfaz de gestión de API keys
3. Intentar agregar una nueva API key
4. Debería aparecer en la lista después de guardar

---

## 📋 Scripts de Utilidad

### verify_migration.py

Script para verificar el estado de la migración de la base de datos:

```bash
python3 verify_migration.py
```

Muestra:
- Tablas existentes
- Si existe api_keys
- Cantidad de registros en api_keys
- Estado de la migración
- Acciones recomendadas

### restart_backend.sh

Script para reiniciar el backend con los cambios nuevos:

```bash
chmod +x restart_backend.sh
./restart_backend.sh
```

Hace:
- Detiene procesos existentes del backend
- Activa el entorno virtual
- Verifica el estado de la base de datos
- Inicia el backend en puerto 8001

---

## ✅ Verificación de Solución

Después de aplicar los pasos anteriores, verifica:

1. ✅ La tabla `api_keys` existe en la base de datos
2. ✅ El endpoint `/api/settings/keys` responde correctamente
3. ✅ Puedes agregar nuevas API keys desde el frontend
4. ✅ Las API keys se guardan y aparecen en la lista
5. ✅ Puedes activar/desactivar API keys
6. ✅ Puedes eliminar API keys con confirmación

---

## 📊 Resumen del Problema y Solución

| Item | Problema | Solución | Estado |
|------|-----------|-----------|--------|
| Modelo no registrado | ApiKey no importado en database.py | Importar ApiKey en database.py | ✅ Implementado |
| Tabla no creada | api_keys no existía en BD | Base.metadata.create_all() ahora la crea | ✅ Solucionado |
| Endpoint no encontrado | Tabla api_keys no existía | Tabla se crea automáticamente al iniciar | ✅ Solucionado |
| Puerto incorrecto | Puerto 8000 en lugar de 8001 | Cambiar fallback a 8001 | ✅ Implementado |
| Keys no aparecen | Tabla no existía | Tabla se crea automáticamente | ✅ Solucionado |

---

## 🚨 Nota Importante

**La migración automática se ejecutará al iniciar el backend**, pero si ya tienes datos en la tabla `settings` y la tabla `api_keys` está vacía, es posible que la migración no se haya ejecutado correctamente.

Si después de reiniciar el backend sigues sin datos en `api_keys`:

1. **Ejecutar la migración manualmente:**
   ```bash
   cd backend
   python3 migrations/002_migrate_to_api_keys.py
   ```

2. **Verificar los logs del backend** para ver si hay algún error

3. **Reiniciar el backend** para que los cambios surtan efecto

---

## 📝 Cambios en el Commit

**Commit:** `f7fde58`

**Archivos modificados:**
1. `backend/app/db/database.py` - Importar ApiKey
2. `frontend/src/config/api.ts` - Corregir puerto a 8001

**Archivos creados:**
1. `verify_migration.py` - Script de verificación de migración
2. `restart_backend.sh` - Script de reinicio del backend

---

**Estado:** ✅ Problema identificado y solucionado
**Fecha:** 16 de febrero de 2026
