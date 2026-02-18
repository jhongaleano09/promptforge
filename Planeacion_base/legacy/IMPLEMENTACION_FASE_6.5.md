# Fase 6.5: Sistema de Gestión de API Keys

## 📋 Resumen de Implementación

**Estado:** ✅ COMPLETADO
**Fecha:** 16 de febrero de 2026
**Prioridad:** 1 (CRÍTICA)

---

## 🎯 Objetivos Alcanzados

1. ✅ **Rediseñar Modelo de Base de Datos**
   - Nuevo modelo `ApiKey` con campos adicionales
   - Soporte para múltiples proveedores simultáneamente
   - Campos de tracking: `usage_count`, `last_used_at`
   - Tabla `settings` mantenida hasta v2.0

2. ✅ **Script de Migración de Datos**
   - Migración automática de `settings` a `api_keys`
   - Logging completo de operaciones
   - Rollback automático en caso de error
   - Ejecución automática al iniciar backend

3. ✅ **Endpoints CRUD para API Keys**
   - `GET /api/settings/keys` - Listar API keys
   - `POST /api/settings/keys` - Agregar nueva API key
   - `DELETE /api/settings/keys/{key_id}` - Eliminar API key
   - `PUT /api/settings/keys/{key_id}/activate` - Activar API key
   - `GET /api/settings/validate-active` - Validar configuración

4. ✅ **UI de Settings para Gestión de API Keys**
   - Componente `ApiKeysManager` en `frontend/src/components/api-keys-manager.tsx`
   - Vista simplificada: key activa + botón para ver todas
   - Modales para agregar y eliminar keys
   - Validación en tiempo real
   - Reintento automático de 10 segundos en errores

5. ✅ **Integración con UI Existente**
   - Botón de settings en header (`/settings`)
   - Validación de configuración al iniciar
   - Actualización de `workflowStore` con `checkActiveKeys()`
   - Compatibilidad con onboarding existente

6. ✅ **Testing y Validación**
   - Validación de API keys con servicios reales
   - Tests de formato de API keys
   - Manejo de errores con reintentos
   - Logging completo en backend

---

## 🗂 Archivos Creados/Modificados

### Backend

#### Archivos Creados
1. `backend/migrations/002_migrate_to_api_keys.py` - Script de migración
   - Detecta tablas existentes
   - Migra datos de `settings` a `api_keys`
   - Logging completo
   - Manejo de errores con rollback

#### Archivos Modificados
1. `backend/app/db/models.py`
   - Nuevo modelo `ApiKey`
   - Campos adicionales: `user_id`, `usage_count`, `last_used_at`, `is_active`, `created_at`, `updated_at`
   - Índices: `idx_provider_active`

2. `backend/app/api/schemas.py`
   - `ApiKeyCreate` - Schema para crear API keys
   - `ApiKeyResponse` - Schema de respuesta
   - `ApiKeysListResponse` - Lista de API keys
   - `ValidationActiveResponse` - Validación de configuración

3. `backend/app/api/endpoints.py`
   - 5 nuevos endpoints CRUD
   - Actualización de endpoints existentes para usar `ApiKey`
   - Fallback a `Settings` por compatibilidad
   - Validación de API keys con servicios
   - Logging completo

4. `backend/main.py`
   - Ejecución automática de migración al iniciar
   - Logging de migración

### Frontend

#### Archivos Creados
1. `frontend/src/components/api-keys-manager.tsx` - Componente de gestión de API keys
   - Vista simplificada (key activa + botón para ver todas)
   - Modal para agregar nueva key
   - Modal de confirmación para eliminar
   - Validación en tiempo real
   - Reintento automático de 10 segundos

2. `frontend/src/app/settings/page.tsx` - Página de settings
   - Integración con `ApiKeysManager`

3. `frontend/src/components/ui/card.tsx` - Componente Card (Shadcn/UI)

#### Archivos Modificados
1. `frontend/src/app/page.tsx`
   - Botón de settings en header
   - Validación de configuración al iniciar
   - Manejo de errores con reintentos

2. `frontend/src/store/workflowStore.ts`
   - Nueva función `checkActiveKeys()`
   - Integración en `startWorkflow()`
   - Validación antes de ejecutar workflow

---

## 🚀 Instrucciones de Instalación y Ejecución

### Paso 1: Instalar Dependencias del Backend

```bash
cd backend
pip install -r requirements.txt
```

### Paso 2: Ejecutar Migración Manual (Opcional)

La migración se ejecuta automáticamente al iniciar el backend, pero puedes ejecutarla manualmente:

```bash
cd backend
python3 migrations/002_migrate_to_api_keys.py
```

**Resultados esperados:**
```
============================================================
Starting Migration 002: settings → api_keys
============================================================
Existing tables: ['settings']
Has 'settings' table: True
Has 'api_keys' table: False
Found 1 settings record(s) to migrate
Migrated provider 'openai' to api_keys table
✅ Successfully migrated 1 API key(s)
Validation: 0 active keys, providers: []
✅ Migration verification: SUCCESS
============================================================
✅ Migration completed successfully
============================================================
```

### Paso 3: Iniciar Backend

```bash
cd backend
python3 main.py
```

**Logs esperados:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Starting PromptForge API...
Checking if migration from settings to api_keys is needed...
INFO:     Existing tables: ['settings', 'api_keys']
INFO:     Has 'settings' table: True
INFO:     Has 'api_keys' table: True
INFO:     Both tables exist. Checking if migration is needed...
INFO:     Migration appears to have already been completed
INFO:     ✅ Migration check completed successfully
INFO:     PromptForge API startup completed
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

### Paso 4: Iniciar Frontend

```bash
cd frontend
npm install
npm run dev
```

### Paso 5: Probar la Aplicación

1. **Acceder a la aplicación:** http://localhost:3000

2. **Configurar API Key (si es necesario):**
   - Si no hay keys configuradas, aparecerá el onboarding
   - Ingresa tu API key de OpenAI, Anthropic, o Ollama
   - Selecciona el modelo preferido
   - Haz clic en "Validate & Save"

3. **Acceder a Settings:**
   - Haz clic en el icono de ⚙️ (Settings) en el header
   - Verás la lista de API keys configuradas
   - Por defecto, solo se muestra la key activa

4. **Agregar Nueva API Key:**
   - Haz clic en "Add New Key"
   - Selecciona el proveedor
   - Ingresa la API key
   - Selecciona el modelo
   - Haz clic en "Add Key"
   - La nueva key se activará automáticamente y desactivará las otras del mismo proveedor

5. **Ver Todas las Keys:**
   - Haz clic en "Show All Keys (X inactive)"
   - Verás todas las keys configuradas
   - Puedes activar cualquier key haciendo clic en "Activate"

6. **Eliminar API Key:**
   - Haz clic en el icono de 🗑️ (Trash) en la key que deseas eliminar
   - Se mostrará un modal de confirmación
   - Si es la última key activa, verás una advertencia
   - Haz clic en "Delete" para eliminar

7. **Probar el Workflow:**
   - Regresa a la página principal
   - Ingresa una descripción de tu prompt
   - Haz clic en "Start Forging"
   - El workflow validará que haya una key activa antes de iniciar

---

## 🧪 Pruebas de Validación

### 1. Validación de API Key

**Endpoint:** `POST /api/settings/validate`

**Request:**
```json
{
  "provider": "openai",
  "api_key": "sk-..."
}
```

**Response exitoso:**
```json
{
  "status": "success",
  "message": "API Key is valid"
}
```

**Response con error:**
```json
{
  "detail": "Invalid API Key"
}
```

### 2. Listar API Keys

**Endpoint:** `GET /api/settings/keys`

**Response:**
```json
{
  "keys": [
    {
      "id": 1,
      "provider": "openai",
      "model_preference": "gpt-4-turbo",
      "is_active": true,
      "usage_count": 150,
      "created_at": "2026-02-16T12:00:00",
      "updated_at": "2026-02-16T14:30:00"
    }
  ]
}
```

### 3. Validar Configuración Activa

**Endpoint:** `GET /api/settings/validate-active`

**Response con keys activas:**
```json
{
  "has_active_key": true,
  "active_providers": ["openai", "anthropic"],
  "all_providers": ["openai", "anthropic", "ollama"],
  "warning": null
}
```

**Response sin keys activas:**
```json
{
  "has_active_key": false,
  "active_providers": [],
  "all_providers": ["openai"],
  "warning": "No hay ninguna API key activa configurada. Por favor configura una para usar PromptForge."
}
```

---

## 📊 Características Implementadas

### Gestión de Múltiples API Keys
- ✅ Soporte para múltiples proveedores (OpenAI, Anthropic, Ollama)
- ✅ Una API key por proveedor activa a la vez
- ✅ Sin límite de keys por proveedor
- ✅ Activación/desactivación con un clic

### Seguridad
- ✅ Encriptación de API keys con Fernet
- ✅ API keys no expuestas en respuestas
- ✅ Validación real con servicios de proveedores
- ✅ Logging de todas las operaciones

### UX Mejorada
- ✅ Vista simplificada: key activa + botón para ver todas
- ✅ Validación en tiempo real de API keys
- ✅ Indicadores visuales de estado (activo/inactivo)
- ✅ Badges de colores por proveedor
- ✅ Contador de tokens por API key
- ✅ Reintento automático de 10 segundos en errores
- ✅ Mensajes de error claros y específicos

### Integración
- ✅ Botón de settings en header
- ✅ Validación automática al iniciar
- ✅ Compatibilidad con onboarding existente
- ✅ Integración con workflow existente
- ✅ Compatibilidad con tabla `settings` (hasta v2.0)

---

## 🐛 Manejo de Errores

### Error de Validación de API Key
- **Mensaje:** "Invalid API Key"
- **Acción:** Muestra error + reintento automático en 10 segundos
- **Log:** "Invalid API key for provider: {provider}"

### Error de Red
- **Mensaje:** "Backend server not reachable"
- **Acción:** Muestra error + reintento automático en 10 segundos
- **Log:** "Failed to validate configuration: {error}"

### Error de Conexión
- **Mensaje:** "Connection lost"
- **Acción:** Muestra error + detiene workflow
- **Log:** "SSE Error: {error}"

### Sin API Key Activa
- **Mensaje:** "No hay ninguna API key activa configurada"
- **Acción:** Redirige a settings
- **Log:** "Configuration required: No active API key"

---

## 📝 Logs y Auditoría

### Backend Logs

**Operación exitosa:**
```
INFO: Listed 2 API key(s)
INFO: API key validated successfully for provider: openai
INFO: New API key created for provider: openai, id: 2
INFO: Activated API key id=2, provider=openai
INFO: Using API key from ApiKey table, provider: openai
```

**Operación con error:**
```
WARNING: Invalid API key for provider: openai
ERROR: Failed to create API key: Invalid API Key
WARNING: Failed to get API key from ApiKey table, trying legacy Settings: {error}
INFO: Using API key from legacy Settings table, provider: openai
```

### Frontend Logs

**Consola del navegador:**
```
Validation warning: No hay ninguna API key activa configurada
SSE Error: Connection lost
Failed to start workflow: Configuración requerida
```

---

## 🔄 Proceso de Migración

### Pasos Automáticos

1. **Detección de tablas:**
   - Busca tabla `settings`
   - Busca tabla `api_keys`

2. **Validación:**
   - Si `settings` existe y `api_keys` no existe → Migrar
   - Si ambas existen → Verificar si migración está completa
   - Si solo `api_keys` existe → Ya migrado

3. **Migración:**
   - Lee datos de `settings`
   - Crea registros en `api_keys`
   - Mantiene `settings` intacta (hasta v2.0)

4. **Verificación:**
   - Compara cantidad de registros
   - Valida integridad de datos
   - Log de resultados

### Rollback

Si la migración falla:
- **Rollback automático** de la transacción
- **Log de error** detallado
- **Continúa ejecución** con configuración vacía
- **Permite al usuario** reintentar manualmente

---

## 🚨 Notas Importantes

1. **Tabla `settings` mantenida hasta v2.0:**
   - Proporciona compatibilidad hacia atrás
   - Permite rollback si es necesario
   - Se eliminará en la versión mayor 2.0

2. **Validación de API keys:**
   - Se hace una llamada real al proveedor
   - Usa el modelo seleccionado por el usuario
   - Guarda log de intentos fallidos

3. **Reintento automático:**
   - Se activa en errores transitorios
   - Espera 10 segundos antes de reintentar
   - Máximo 2 reintentos antes de detenerse

4. **Logging completo:**
   - Todas las operaciones se logean
   - Logs en backend (`INFO`, `WARNING`, `ERROR`)
   - Logs en frontend (consola del navegador)

---

## 🎯 Criterios de Éxito Alcanzados

1. ✅ Soportar múltiples proveedores (OpenAI, Anthropic, Ollama)
2. ✅ Permitir agregar, activar, desactivar, eliminar API keys
3. ✅ Validar que al menos una key esté activa antes de usar el sistema
4. ✅ Confirmar eliminación con el usuario
5. ✅ Ofrecer agregar nueva key al eliminar la última
6. ✅ UI intuitiva para gestión de API keys
7. ✅ Integración fluida con la UI existente
8. ✅ Migración segura de datos existentes
9. ✅ Validación real de API keys con servicios
10. ✅ Documentación actualizada

---

## 📚 Próximos Pasos (Fases Futuras)

1. **Fase 7.5:** Internacionalización i18n (español, inglés)
2. **Fase 8:** Tipos de Prompt Modulares (Basic, System, Image, Additional)
3. **Fase 9:** Validación de API Key de Test

---

**Implementación Completada:** 16 de febrero de 2026
**Desarrollado por:** OpenCode Assistant
**Versión:** 1.0 (Producción)
