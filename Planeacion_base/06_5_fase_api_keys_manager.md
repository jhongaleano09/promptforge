# 06.5. Fase: Sistema de Gestión de API Keys

**Estado:** 🆕 PLANIFICADA - Lista para Implementación  
**Prioridad:** 1 (CRÍTICA - Bloquea otras funcionalidades)  
**Estimado:** 2-3 días

---

## 🎯 Objetivos

Implementar un sistema completo de gestión de API keys que permita:
1. Múltiples proveedores simultáneamente (OpenAI, Anthropic, Ollama)
2. Una API key por proveedor activa a la vez
3. Eliminar API keys de forma segura con confirmación
4. Ofrecer agregar nueva key al eliminar la última
5. Validar que al menos una key esté activa antes de usar el sistema
6. Reconfigurar API keys en cualquier momento desde settings

---

## 🗺 Desglose de Tareas

### Tarea 6.5.1: Rediseñar Modelo de Base de Datos

**Archivo:** `backend/app/db/models.py`

**Objetivo:** Migrar del modelo actual (tabla `settings` simple) a un modelo robusto que soporte múltiples API keys por proveedor.

**Estado Actual:**
```python
class Settings(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True)
    provider = Column(String, default="openai")
    api_key_encrypted = Column(LargeBinary, nullable=False)
    model_preference = Column(String, default="gpt-4-turbo")
```

**Estado Objetivo:**
```python
class ApiKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, nullable=False, index=True)
    api_key_encrypted = Column(LargeBinary, nullable=False)
    model_preference = Column(String, default="gpt-4-turbo")
    is_active = Column(Integer, default=1)
    created_at = Column(String)
    updated_at = Column(String)
```

**Pasos de Implementación:**

1. **Crear nueva clase `ApiKey`**
   - Definir la estructura de la tabla
   - Agregar constraint único para evitar múltiples keys activas del mismo proveedor
   - Usar `LargeBinary` para mantener compatibilidad con encriptación

2. **Definir indices y constraints**
   - Índice en `provider` para búsquedas rápidas
   - Constraint único: `(provider, is_active)` → Solo una key activa por proveedor
   - Esto garantiza que al activar una, se desactiven las otras automáticamente

3. **Mantener compatibilidad con seguridad**
   - Asegurar que `api_key_encrypted` use el mismo formato que el modelo anterior
   - Verificar que `security_service.decrypt_key()` funcione con el nuevo formato

4. **Considerar migración de datos**
   - ¿Cómo migrar los datos existentes en `settings` a `api_keys`?
   - ¿Qué hacer si ya hay datos en `settings`?

**❓ Preguntas Clave:**

1. ¿Deseas crear la nueva tabla `api_keys` y eliminar la vieja `settings` en el mismo script de migración, o prefieres hacerlo en pasos separados?
2. ¿Deberíamos agregar un campo `user_id` o `session_id` para soportar múltiples usuarios en el futuro?
3. ¿Deberíamos agregar campos adicionales como `last_used_at` o `usage_count` para estadísticas?
4. ¿Qué hacer con los datos existentes en `settings` cuando se realice la migración? ¿Migrarlos o solicitar al usuario que reingrese la API key?

---

### Tarea 6.5.2: Crear Script de Migración de Datos

**Archivo:** `backend/migrations/002_migrate_to_api_keys.py`

**Objetivo:** Migrar los datos existentes de la tabla `settings` a la nueva estructura `api_keys` de forma segura.

**Pasos de Implementación:**

1. **Crear directorio de migraciones**
   - Crear `backend/migrations/` si no existe
   - Establecer convención de nombres: `001_...`, `002_...`, etc.

2. **Crear script de migración**
   - Función `upgrade()`: Realizar la migración
   - Función `downgrade()`: Revertir la migración (opcional)
   - Manejo de errores con rollback automático

3. **Lógica de migración**
   a. **Conexión a base de datos**
      - Usar la misma conexión que usa el backend
      - Obtener sesión de SQLAlchemy

   b. **Leer datos existentes**
      - Consultar tabla `settings`
      - Verificar si hay datos
      - Manejar caso de tabla vacía

   c. **Transformar datos**
      - Mapear campos de `settings` a `api_keys`
      - `provider` → `provider` (mismo campo)
      - `api_key_encrypted` → `api_key_encrypted` (mismo campo)
      - `model_preference` → `model_preference` (mismo campo)
      - Marcar como `is_active = 1`
      - Generar `created_at` y `updated_at` con timestamps actuales

   d. **Insertar en nueva tabla**
      - Crear registros en `api_keys`
      - Manejar duplicados (si aplica)

   e. **Verificar migración**
      - Confirmar que los datos se migraron correctamente
      - Comparar cantidad de registros

   f. **Eliminar tabla vieja** (opcional)
      - Pregunta clave: ¿Eliminar inmediatamente o marcar como obsoleta?
      - Recomendación: Marcar como obsoleta por un período antes de eliminar

4. **Ejecutar migración**
   - Ejecutar script al iniciar el backend
   - Verificar logs de migración
   - Confirmar que no haya errores

**❓ Preguntas Clave:**

1. ¿Deseas que la migración se ejecute automáticamente al iniciar el backend si detecta que la tabla `settings` existe y `api_keys` no?
2. ¿O prefieres que la migración sea un comando manual que el usuario ejecute?
3. ¿Qué debería pasar si la migración falla? ¿Mostrar error y bloquear el sistema, o permitir continuar con configuración vacía?
4. ¿Deberíamos guardar un registro de la migración en un archivo `migration_log.txt` o solo en logs del backend?
5. ¿Deberíamos mantener la tabla `settings` por un tiempo por si el usuario quiere revertir la migración?

---

### Tarea 6.5.3: Crear Endpoints CRUD para API Keys

**Archivo:** `backend/app/api/endpoints.py`

**Objetivo:** Implementar endpoints REST para gestionar completamente las API keys (CRUD completo).

**Pasos de Implementación:**

#### 1. GET `/api/settings/keys` - Listar API Keys

**Objetivo:** Retornar todas las API keys del usuario con su estado.

**Implementación:**
- Consultar tabla `api_keys`
- Retornar lista de keys con sus metadatos
- Incluir campos: `id`, `provider`, `model_preference`, `is_active`, `created_at`
- **NO** incluir `api_key_encrypted` (seguridad)

**Response esperado:**
```json
{
  "keys": [
    {
      "id": 1,
      "provider": "openai",
      "model_preference": "gpt-4-turbo",
      "is_active": true,
      "created_at": "2026-02-16T12:00:00Z"
    }
  ]
}
```

**Consideraciones:**
- Ordenar por `created_at` descendente (más nuevas primero)
- Incluir metadatos útiles (cuándo se creó, estado)
- NO exponer información sensible

**❓ Pregunta Clave:**
¿Deberíamos incluir también el `model_preference` en la respuesta o solo el `provider` y el estado?

#### 2. POST `/api/settings/keys` - Agregar Nueva API Key

**Objetivo:** Agregar una nueva API key con validación completa.

**Implementación:**
- Validar proveedor (`openai`, `anthropic`, `ollama`)
- Validar formato de API key
- Validar que no haya más de 3 keys por proveedor
- **Validar API key con el servicio** (llamada real a OpenAI/Anthropic)
- Desactivar otras keys del mismo proveedor
- Encriptar la key antes de guardar
- Guardar en base de datos
- Retornar resultado

**Request:**
```json
{
  "provider": "openai",
  "api_key": "sk-...",
  "model_preference": "gpt-4-turbo"
}
```

**Validaciones requeridas:**
- `provider` debe ser uno de: `openai`, `anthropic`, `ollama`
- `api_key` no debe estar vacío
- `api_key` debe tener el formato correcto para el proveedor
- `model_preference` debe ser un modelo válido para el proveedor
- Máximo 3 keys por proveedor (evitar spam)
- **Validación real con el servicio** (critical for UX)

**Lógica de validación con servicio:**
```python
# Pseudocódigo
try:
    response = completion(
        model=get_test_model(provider),
        messages=[{"role": "user", "content": "Hello"}],
        api_key=api_key,
        max_tokens=5
    )
    return True  # Key válida
except Exception:
    return False  # Key inválida
```

**Lógica de desactivación automática:**
```python
# Al agregar nueva key, desactivar las otras del mismo proveedor
db.query(ApiKey).filter(
    ApiKey.provider == provider,
    ApiKey.id != new_key_id
).update({"is_active": 0})
```

**❓ Preguntas Clave:**

1. ¿Deseas que la validación con el servicio se haga de forma síncrona o asíncrona?
2. ¿Qué modelo usar para la validación? ¿Uno económico (`gpt-3.5-turbo`) o el que el usuario seleccionó como preferido?
3. ¿Deberíamos guardar un registro de intentos fallidos de validación para detectar posibles ataques?
4. ¿Cuál debería ser el límite de keys por proveedor? ¿3, 5, o sin límite?
5. ¿Qué hacer si el proveedor seleccionado no soporta el modelo preferido? ¿Usar un modelo default o mostrar error?

#### 3. DELETE `/api/settings/keys/{key_id}` - Eliminar API Key

**Objetivo:** Eliminar una API key específica con confirmación y validaciones.

**Implementación:**
- Validar que la key existe
- **Validar que no sea la última key activa** (o pedir confirmación)
- Eliminar de base de datos
- Confirmar que al menos una key permanece activa
- Retornar resultado

**Consideraciones críticas:**
- Si la key a eliminar es la única key activa → Requerir confirmación
- Si hay otras keys activas del mismo proveedor → Permitir eliminación sin confirmación
- Si es la única key del sistema → Pedir confirmación y ofertecer agregar nueva

**Flujo de confirmación:**
```python
# Pseudocódigo
key_to_delete = get_key_by_id(key_id)

if key_to_delete.is_active:
    # Verificar si es la única key activa del proveedor
    other_active_keys = query(ApiKey).filter(
        ApiKey.is_active == 1,
        ApiKey.provider == key_to_delete.provider
    ).count()
    
    if other_active_keys == 0:
        # Es la única key activa del sistema
        return {
            "requires_confirmation": True,
            "message": "Esta es tu única API key activa. ¿Estás seguro de eliminarla?"
        }
    
    # Hay otras keys activas
    return {
        "requires_confirmation": False,
        "message": "Confirma eliminación"
    }
```

**Validación post-eliminación:**
```python
# Después de eliminar, verificar que al menos una key esté activa
if count_active_keys() == 0:
    return {
        "status": "error",
        "message": "No puedes eliminar tu última API key. Debes agregar una nueva primero."
    }
```

**❓ Preguntas Clave:**

1. ¿Deseas que la confirmación se haga en el backend (requerir confirmación) o en el frontend (modal)?
2. Si el usuario confirma eliminar la última key y no agrega una nueva, ¿qué debería pasar? ¿Bloquear el sistema con mensaje instructivo?
3. ¿Deberíamos ofrecer la opción "Eliminar y Agregar Nueva" en el mismo flujo?
4. ¿Deberíamos guardar un log de eliminaciones (quién, cuándo, qué key) para auditoría?
5. ¿Deseas un período de "papelera" (por ejemplo, keys eliminadas pero recuperables por 24 horas)?

#### 4. PUT `/api/settings/keys/{key_id}/activate` - Activar API Key

**Objetivo:** Activar una key específica y desactivar las otras del mismo proveedor.

**Implementación:**
- Validar que la key existe
- Desactivar todas las keys del mismo proveedor
- Activar la key seleccionada
- Actualizar `updated_at`
- Retornar resultado

**Lógica de cambio activo:**
```python
# Pseudocódigo
provider = get_key_by_id(key_id).provider

# Desactivar todas las keys del proveedor
db.query(ApiKey).filter(
    ApiKey.provider == provider
).update({"is_active": 0})

# Activar la key seleccionada
db.query(ApiKey).filter(
    ApiKey.id == key_id
).update({"is_active": 1, "updated_at": current_timestamp()})
```

**Beneficio:** Garantiza que solo una key esté activa por proveedor.

**❓ Pregunta Clave:**
¿Deseas que al activar una key, se envíe una notificación o evento (para mostrar en el frontend que la key cambió)?

#### 5. GET `/api/settings/validate-active` - Validar Configuración

**Objetivo:** Validar que hay al menos una API key activa en el sistema.

**Implementación:**
- Consultar tabla `api_keys`
- Contar keys con `is_active == 1`
- Retornar estado y warning si aplica

**Response esperado (con keys activas):**
```json
{
  "has_active_key": true,
  "active_providers": ["openai", "anthropic"],
  "warning": null
}
```

**Response esperado (sin keys activas):**
```json
{
  "has_active_key": false,
  "active_providers": [],
  "warning": "No hay ninguna API key activa configurada. Por favor configura una para usar PromptForge."
}
```

**Uso:** Llamar al inicio de cada acción que requiera API key.

**❓ Pregunta Clave:**
¿Deseas incluir en la respuesta también la lista de providers que tienen keys (aunque estén inactivas) para mostrar en la UI?

---

### Tarea 6.5.4: Crear UI de Settings para Gestión de API Keys

**Archivo:** `frontend/src/components/api-keys-manager.tsx`

**Objetivo:** Componente completo para gestión visual de API keys.

**Pasos de Implementación:**

#### 1. Estado y Datos del Componente

**Implementación:**
```typescript
// Estados necesarios
const [apiKeys, setApiKeys] = useState<ApiKey[]>([]);
const [loading, setLoading] = useState(false);
const [error, setError] = useState<string | null>(null);
const [showAddModal, setShowAddModal] = useState(false);
const [showDeleteModal, setShowDeleteModal] = useState(false);
const [keyToDelete, setKeyToDelete] = useState<ApiKey | null>(null);
```

#### 2. Función de Carga de API Keys

**Objetivo:** Cargar la lista de API keys desde el backend.

**Implementación:**
- Llamar a `GET /api/settings/keys` al montar el componente
- Guardar respuesta en estado
- Manejar errores de carga
- Implementar refresh manual (botón de recargar)

**❓ Pregunta Clave:**
¿Deseas que la lista se cargue automáticamente al montar el componente o solo cuando el usuario hace clic en un botón de "Cargar"?

#### 3. Renderizado de Lista de API Keys

**Objetivo:** Mostrar lista visual de todas las API keys con su estado.

**Implementación:**
- Card o fila por cada API key
- Mostrar: Provider, Modelo Preferido, Estado (Activa/Inactiva), Fecha de creación
- Indicador visual de cuál está activa (badges, colores)
- Badges para proveedores (OpenAI = 🔵, Anthropic = 🟣, Ollama = 🟢)

**Ejemplo de estructura:**
```typescript
// Pseudocódigo
return (
  <div className="space-y-4">
    {apiKeys.map(key => (
      <div className="flex items-center justify-between p-4 border rounded-lg">
        <div className="flex items-center gap-4">
          <ProviderBadge provider={key.provider} />
          <div>
            <div className="font-semibold">{key.provider}</div>
            <div className="text-sm text-muted-foreground">
              {key.model_preference}
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {key.is_active && <span className="text-green-500">Activa</span>}
          {!key.is_active && <span className="text-gray-500">Inactiva</span>}
          <button onClick={() => activateKey(key.id)}>Activar</button>
          <button onClick={() => showDeleteConfirmation(key)}>Eliminar</button>
        </div>
      </div>
    ))}
  </div>
);
```

**❓ Preguntas Clave:**

1. ¿Deseas que la lista sea en formato de cards (vertical) o tabla (horizontal con columnas)?
2. ¿Deberíamos mostrar el modelo preferido en la lista o solo el provider y el estado?
3. ¿Deseas agregar información adicional como "Última vez usada" o "Cantidad de usos"?
4. ¿Deberíamos implementar búsqueda/filtro en la lista de API keys?

#### 4. Modal para Agregar Nueva API Key

**Objetivo:** Formulario modal para agregar una nueva API key con validación.

**Implementación:**
- Selector de Proveedor (OpenAI, Anthropic, Ollama)
- Campo de API Key (tipo password para ocultar caracteres)
- Selector de Modelo Preferido (según proveedor seleccionado)
- Botón "Validate & Save" con indicador de carga
- Validación en tiempo real (mostrar ✓ o ✗ mientras escribe)
- Cerrar modal al guardar exitosamente

**Campos del formulario:**
```typescript
// Pseudocódigo
<form onSubmit={handleAddKey}>
  <label>Proveedor</label>
  <select value={provider} onChange={setProvider}>
    <option value="openai">OpenAI</option>
    <option value="anthropic">Anthropic</option>
    <option value="ollama">Ollama</option>
  </select>

  <label>API Key</label>
  <input 
    type="password" 
    value={apiKey} 
    onChange={handleApiKeyChange}
    placeholder="sk-..."
  />
  <ValidationIndicator isValidating={isValidating} />

  <label>Modelo Preferido</label>
  <select value={modelPreference} onChange={setModelPreference}>
    {models.map(model => (
      <option value={model.id}>{model.name}</option>
    ))}
  </select>

  <button disabled={!isValidating || !apiKey}>
    Validate & Save
  </button>
</form>
```

**Validación en tiempo real:**
- Debounce para no validar cada keystroke
- Validar formato de API key mientras escribe
- Mostrar indicador visual: "✓ Key válida" o "✗ Key inválida"

**❓ Preguntas Clave:**

1. ¿Deseas que la validación se haga al perder foco del campo (onBlur) o mientras escribe (onChange con debounce)?
2. ¿Deberíamos mostrar mensajes de error específicos (ej: "Formato inválido para OpenAI")?
3. ¿Deseas agregar un botón de "Paste" para facilitar pegar la API key desde el portapapeles?

#### 5. Modal de Confirmación de Eliminación

**Objetivo:** Modal que requiere confirmación antes de eliminar una API key.

**Implementación:**
- Mostrar información de la key a eliminar
- Advertencia clara del impacto
- Opciones: "Cancelar", "Eliminar y Agregar Nueva", "Solo Eliminar"
- Validar que si es la última key activa, se oferteca agregar una nueva

**Ejemplo de estructura:**
```typescript
// Pseudocódigo
return (
  <Modal isOpen={showDeleteModal} onClose={cancelDelete}>
    <div className="p-6">
      <h3 className="text-xl font-bold">¿Estás seguro de eliminar esta API Key?</h3>
      
      <div className="text-muted-foreground mb-4">
        Esta acción no se puede deshacer.
      </div>

      {isLastActiveKey && (
        <div className="bg-orange-50 border border-orange-200 p-4 rounded mb-4">
          <p className="text-orange-800 font-medium">⚠️ Advertencia</p>
          <p className="text-orange-700 text-sm">
            Esta es tu única API key activa. Si la eliminas, 
            no podrás usar PromptForge hasta que agregues una nueva.
          </p>
        </div>
      )}

      <div className="flex gap-3">
        <button onClick={cancelDelete}>Cancelar</button>
        
        {isLastActiveKey && (
          <button onClick={deleteAndAddNew}>Eliminar y Agregar Nueva</button>
        )}
        
        <button onClick={deleteOnly}>Solo Eliminar</button>
      </div>
    </div>
  </Modal>
);
```

**❓ Pregunta Clave:**
¿Deseas agregar una opción de "Papelera" donde las keys eliminadas se guarden por 24 horas y puedan recuperarse?

---

### Tarea 6.5.5: Integración con UI Existente

**Archivos:** `frontend/src/app/page.tsx`, `frontend/src/components/ui/button.tsx`

**Objetivo:** Integrar el nuevo sistema de gestión de API keys con la UI existente.

**Pasos de Implementación:**

#### 1. Agregar Botón de Acceso a Settings

**Objetivo:** Botón en el header para acceder a settings desde cualquier vista.

**Implementación:**
- Botón con icono de configuración (⚙️)
- Colocado en el header de la aplicación
- Redirigir a vista de settings
- Visible en todas las páginas (usar layout principal)

**Ejemplo de estructura:**
```typescript
// En header de layout.tsx o page.tsx
<button onClick={() => router.push('/settings')}>
  <SettingsIcon className="w-5 h-5" />
  Configuración
</button>
```

**❓ Pregunta Clave:**
¿Deseas que el botón de settings esté siempre visible o solo cuando hay una API key configurada?

#### 2. Verificar Configuración al Iniciar

**Objetivo:** Validar que hay una API key activa antes de mostrar la interfaz principal.

**Implementación:**
- Al montar `page.tsx`, llamar a `GET /api/settings/validate-active`
- Si no hay key activa → Mostrar onboarding
- Si hay key activa → Mostrar interfaz principal
- Guardar resultado en estado para evitar validaciones repetidas

**Lógica de navegación:**
```typescript
// Pseudocódigo
useEffect(() => {
    validateConfiguration();
  }, []);

const validateConfiguration = async () => {
    const response = await fetch(`${API_BASE}/settings/validate-active`);
    const data = await response.json();
    
    if (!data.has_active_key) {
        setShowOnboarding(true);
    } else {
        setShowOnboarding(false);
    }
};
```

**❓ Preguntas Clave:**

1. ¿Deseas que esta validación se haga cada vez que se carga la página o solo una vez y guardar en estado?
2. ¿Qué debería pasar si la validación falla por error de red? ¿Mostrar mensaje o intentar de nuevo?
3. ¿Deseas agregar un indicador de "Conectando..." mientras se valida la configuración?
4. ¿Deberíamos permitir acceder a settings aunque no haya key activa (para agregar una)?

#### 3. Actualizar Store de Workflow

**Archivo:** `frontend/src/store/workflowStore.ts`

**Objetivo:** Integrar validación de configuración en las acciones del workflow.

**Implementación:**
- Agregar función `checkActiveKeys()` al store
- Llamar antes de cada acción que requiera API key
- Manejar caso de no hay key activa (redirigir a settings)
- Mostrar error apropiado si no hay key

**Ejemplo de función:**
```typescript
// Pseudocódigo
const checkActiveKeys = async () => {
    const response = await fetch(`${API_BASE}/settings/validate-active`);
    const data = await response.json();
    
    if (!data.has_active_key) {
        setError("No hay ninguna API key activa configurada");
        router.push('/settings');
        throw new Error("Configuración requerida");
    }
    
    return data; // Retornar configuración para uso en otras funciones
};
```

**Integración en acciones existentes:**
```typescript
const startWorkflow = async (input: string) => {
    await checkActiveKeys(); // Nueva validación
    
    // ... lógica existente de workflow
};
```

**❓ Pregunta Clave:**
¿Deseas que la validación se haga antes de cada acción (costoso en llamadas) o solo al inicio de la sesión y guardar en caché?

---

### Tarea 6.5.6: Testing y Validación

**Objetivo:** Probar todas las funcionalidades del sistema de gestión de API keys.

**Casos de prueba:**

1. **Agregar nueva API key**
   - Validar formato correcto
   - Validar con servicio (OpenAI/Anthropic)
   - Verificar que se guarda encriptada
   - Verificar que se marca como activa
   - Verificar que se desactivan las otras del mismo proveedor

2. **Listar API keys**
   - Verificar que todas las keys aparecen
   - Verificar que `api_key_encrypted` no se expone
   - Verificar que el estado se muestra correctamente

3. **Activar API key**
   - Activar key inactiva
   - Verificar que la anterior se desactiva
   - Verificar que solo una key por proveedor está activa

4. **Eliminar API key**
   - Eliminar key con confirmación
   - Verificar que se elimina de BD
   - Eliminar última key activa → Verificar mensaje de error
   - Eliminar y agregar nueva → Verificar flujo completo

5. **Validación de configuración**
   - Sin keys → Mostrar onboarding
   - Con keys → Mostrar interfaz principal
   - Eliminar todas → Error instructivo

**❓ Preguntas Clave:**

1. ¿Deseas que las pruebas sean manuales (usando la UI) o automatizadas (scripts de test)?
2. ¿Deseas incluir tests de integración que prueben la API directamente?
3. ¿Deberíamos probar también el límite de 3 keys por proveedor?

---

## 📊 Summary de Fase 6.5

### Archivos a Crear/Modificar

**Backend:**
1. `backend/app/db/models.py` - Nuevo modelo `ApiKey`
2. `backend/migrations/002_migrate_to_api_keys.py` - Script de migración
3. `backend/app/api/endpoints.py` - Endpoints CRUD (5 nuevos endpoints)

**Frontend:**
1. `frontend/src/components/api-keys-manager.tsx` - Componente nuevo
2. `frontend/src/components/settings-page.tsx` - Página nueva
3. `frontend/src/app/page.tsx` - Integración de botón settings
4. `frontend/src/store/workflowStore.ts` - Validación de configuración
5. `frontend/src/components/ui/button.tsx` - Posible nuevo botón de settings

### Tareas Totales: 6
1. [ ] 6.5.1: Rediseñar modelo de base de datos
2. [ ] 6.5.2: Crear script de migración
3. [ ] 6.5.3: Crear endpoints CRUD para API keys
4. [ ] 6.5.4: Crear UI de Settings
5. [ ] 6.5.5: Integración con UI existente
6. [ ] 6.5.6: Testing y validación

### Preguntas Clave Totales: 20
Estas preguntas están distribuidas en cada tarea para facilitar la implementación.

---

## 🎯 Criterios de Éxito de Fase 6.5

Al completar esta fase, el sistema deberá:

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

**Fase 6.5 - Planificación Creada Por:** OpenCode Assistant  
**Fecha:** 16 de febrero de 2026  
**Versión:** 1.0 - Lista para Implementación
