# 📋 Planificación Maestra - PromptForge

**Fecha de Creación:** 16 de Febrero de 2026  
**Estado:** ✅ COMPLETA Y ORGANIZADA  
**Versión del Documento:** 1.0 (CONSOLIDADA)  

---

## 📋 Tabla de Contenido

- [1. Visión Global](#1-visión-global)
- [2. Estado Actual del Proyecto](#2-estado-actual-del-proyecto)
- [3. Hoja de Ruta (Roadmap) - Q1 2026](#3-hoja-de-ruta-roadmap---q1-2026)
- [4. Fase 1-5: MVP Básico (Completado)](#4-fase-1-5-mvp-básico-completado)
- [5. Fase 6: Consolidación y Documentación](#5-fase-6-consolidación-y-documentación)
- [6. Fase 6.5: Sistema de Gestión de API Keys](#6-fase-65-sistema-de-gestión-de-api-keys)
- [7. Fase 7.5: Internacionalización i18n](#7-fase-75-internacionalización-i18n)
- [8. Fase 8: Tipos de Prompt Modulares](#8-fase-8-tipos-de-prompt-modulares)
- [9. Fase 9: Validación de API Key de Test](#9-fase-9-validación-de-api-key-de-test)
- [10. Prioridades y Estrategia de Implementación](#10-prioridades-y-estrategia-de-implementación)
- [11. Resumen de Fases](#11-resumen-de-fases)

---

## 1. Visión Global

### 📋 Concepto del Proyecto
**PromptForge** es una herramienta profesional de ingeniería de prompts diseñada para elevar el estándar de interacción con LLMs. Transforma una idea vaga en un prompt de producción mediante un proceso estructurado de **clarificación, generación de variantes, validación automática, refinamiento experto y testing competitivo (Arena).**

### 🎯 Objetivos Principales

1. **Calidad sobre Cantidad:** No generar un solo prompt, sino explorar el espacio de soluciones con 3 variantes competitivas.
2. **Ciclo de Feedback Humano:** El usuario no es un espectador pasivo; es el juez final en la "Arena" y el director en la fase de refinamiento.
3. **Agnosticismo de Modelo:** Diseñado para funcionar con cualquier proveedor (OpenAI, Anthropic, GLM, Local LLMs via Ollama) mediante una capa de abstracción.
4. **Seguridad y Privacidad:** Gestión local y encriptada de credenciales.
5. **Internacionalización:** Soporte completo para múltiples idiomas (English/Spanish).
6. **Arquitectura Modular:** Soporte para múltiples tipos de prompt con workflows específicos.

### 🏗️ Stack Tecnológico

#### Backend (Python 3.11+)
- **Framework API:** FastAPI
- **Orquestación:** LangGraph (para flujos cíclicos y stateful)
- **LLM Interface:** LiteLLM (para estandarizar llamadas a APIs)
- **Base de Datos:** SQLite (ligera, archivo local) con SQLAlchemy
- **Seguridad:** Librería `cryptography` (Fernet) para encriptación de API Keys en reposo

#### Frontend (Next.js 16)
- **Framework:** Next.js 16 (React)
- **UI Libs:** Tailwind CSS, Shadcn/UI, Lucide Icons
- **Estado:** Zustand + React Query
- **Internacionalización:** React Context + JSON files

---

## 2. Estado Actual del Proyecto

### Diagnóstico (16/02/2026)

#### A. Backend (Python/FastAPI)
- **Estado:** ✅ Estable y funcional
- **Arquitectura:** Modular (`app/core`, `app/api`, `app/agents`)
- **Orquestación:** Implementación exitosa de **LangGraph** para el flujo `Clarify -> Generate -> Evaluate`
- **Streaming:** Server-Sent Events (SSE) implementado para generación
- **Seguridad:** Cifrado de API Keys en reposo utilizando `fernet`
- **Persistencia:** SQLite local funcional
- **Deuda Técnica:**
  - Falta de soporte para múltiples API keys (solo una key simple en DB)
  - Falta de internacionalización (i18n) completa
  - Arquitectura de tipos de prompt no modularizada

#### B. Frontend (Next.js 16)
- **Estado:** ✅ Funcional y estético
- **Tecnología:** React, Tailwind CSS, Zustand (State Management)
- **Componentes:**
  - `Onboarding`: Gestión de API key (simple, una key)
  - `ChatInterface`: Interfaz de chat para clarificación
  - `ArenaView`: Vista comparativa de variantes
  - `WorkflowStore`: Gestión de estado global
- **Conexión:** Configuración con variables de entorno implementada (`.env.local` con `NEXT_PUBLIC_API_URL`)
- **Deuda Técnica:**
  - Falta de sistema de gestión de API keys UI
  - Falta de internacionalización (i18n) en la UI
  - Falta de selector de tipos de prompt

#### C. Infraestructura y Despliegue
- **Estado:** ⚠️ Funcional pero requiere mejoras
- **Situación:** Backend en puerto 8001, Frontend en puerto 3000
- **Documentación:** README.md existe pero necesita actualización con nuevas funcionalidades

---

## 3. Hoja de Ruta (Roadmap) - Q1 2026

### Resumen de Fases

| Fase | Nombre | Estado | Prioridad | Estimado |
|------|--------|--------|-----------|----------|
| 1-5 | MVP Básico | ✅ Completado | N/A | - |
| 6 | Consolidación | 🔄 En Proceso | Media | 2-3 días |
| 6.5 | Gestión de API Keys | 🆕 Planificado | 1 CRÍTICA | 2-3 días |
| 7.5 | Internacionalización | 🆕 Planificado | 2 ALTA | 3-4 días |
| 8 | Tipos de Prompt | 🆕 Planificado | 3 MEDIA | 4-5 días |
| 9 | Validación API Key Test | 🆕 Planificado | 4 BAJA | 1-2 días |

### Estrategia de Desarrollo

Implementación incremental priorizando funcionalidades críticas:

1. **Sprint 1 (2-3 días):** Gestión de API Keys (FASE 6.5) - PRIORIDAD 1 CRÍTICA
2. **Sprint 2 (3-4 días):** Internacionalización i18n (FASE 7.5) - PRIORIDAD 2 ALTA
3. **Sprint 3 (4-5 días):** Tipos de Prompt Modulares (FASE 8) - PRIORIDAD 3 MEDIA
4. **Sprint 4 (1-2 días):** Validación de API Key de Test (FASE 9) - PRIORIDAD 4 BAJA
5. **Sprint 5 (2-3 días):** Integración y Testing

---

## 4. Fase 1-5: MVP Básico (Completado)

### Objetivos Logrados
- [x] Planificación de documentos maestros
- [x] Conexión API: Fix de puerto (frontend: 3000 → backend: 8001)
- [x] Variables de entorno: Implementación de `.env.local` con `NEXT_PUBLIC_API_URL`
- [x] Validación API Key: Backend corrigido para validar correctamente
- [x] Testing: API Key de usuario validada exitosamente
- [x] Orquestación con LangGraph: Flujo `Clarify -> Generate -> Evaluate` funcional
- [x] Streaming SSE: Generación en tiempo real implementada
- [x] Interfaz Arena: Vista comparativa de variantes funcional
- [x] Encriptación de API Keys: Cifrado en reposo con Fernet

### Componentes Implementados

#### Backend
- ✅ `app/api/endpoints.py` - Endpoints REST principales
- ✅ `app/agents/graph.py` - Grafo de workflow con LangGraph
- ✅ `app/agents/nodes.py` - Nodos del workflow (clarify, generate, evaluate)
- ✅ `app/db/models.py` - Modelo de base de datos (Settings)
- ✅ `app/core/security.py` - Servicio de encriptación/desencriptación
- ✅ `app/services/llm_engine.py` - Motor LLM con LiteLLM

#### Frontend
- ✅ `src/app/page.tsx` - Página principal
- ✅ `src/components/onboarding-form.tsx` - Formulario de configuración
- ✅ `src/components/arena/ArenaView.tsx` - Vista comparativa
- ✅ `src/store/workflowStore.ts` - Store de estado global
- ✅ `.env.local` - Variables de entorno

---

## 5. Fase 6: Consolidación y Documentación

### Objetivos
- [x] Planificación: Documentos maestros creados
- [ ] Dockerización: Crear Dockerfiles y docker-compose.yml
- [ ] Documentación Maestra (`README.md`): Actualizar con nuevas funcionalidades
  - Sección de API Keys (múltiples)
  - Sección de i18n (cambiar idioma)
  - Sección de tipos de prompt
  - Guías actualizadas

### Detalles de Implementación

#### Tarea 6.1: Dockerización
**Archivos a crear:**
- `backend/Dockerfile` - Imagen Docker para backend
- `frontend/Dockerfile` - Imagen Docker para frontend
- `docker-compose.yml` - Orquestación de servicios

**Pasos:**
1. Crear Dockerfile para backend Python
2. Crear Dockerfile para frontend Next.js
3. Crear docker-compose.yml para orquestar ambos servicios
4. Agregar `.dockerignore` en ambos proyectos
5. Probar construcción y ejecución de contenedores

#### Tarea 6.2: Actualización de README.md
**Secciones a agregar:**
- Descripción de nuevas funcionalidades
- Guía de uso de API Keys (múltiples proveedores)
- Guía de cambio de idioma
- Guía de tipos de prompt
- Ejemplos de uso actualizados
- Troubleshooting común

**Preguntas Clave:**
1. ¿Deseas que el README.md esté en inglés, español, o bilingüe?
2. ¿Deberíamos agregar screenshots o GIFs de la aplicación en funcionamiento?
3. ¿Deseas incluir una sección de "Roadmap Futuro" con funcionalidades planeadas?
4. ¿Deberíamos agregar una tabla de compatibilidad con modelos de diferentes proveedores?

---

## 6. Fase 6.5: Sistema de Gestión de API Keys

### 🎯 Objetivos

Implementar un sistema completo de gestión de API keys que permita:
1. Múltiples proveedores simultáneamente (OpenAI, Anthropic, Ollama)
2. Una API key por proveedor activa a la vez
3. Eliminar API keys de forma segura con confirmación
4. Ofrecer agregar nueva key al eliminar la última
5. Validar que al menos una key esté activa antes de usar el sistema
6. Reconfigurar API keys en cualquier momento desde settings

### 🗺 Desglose de Tareas

#### Tarea 6.5.1: Rediseñar Modelo de Base de Datos

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

**Preguntas Clave:**

1. ¿Deseas crear la nueva tabla `api_keys` y eliminar la vieja `settings` en el mismo script de migración, o prefieres hacerlo en pasos separados?
2. ¿Deberíamos agregar un campo `user_id` o `session_id` para soportar múltiples usuarios en el futuro?
3. ¿Deberíamos agregar campos adicionales como `last_used_at` o `usage_count` para estadísticas?
4. ¿Qué hacer con los datos existentes en `settings` cuando se realice la migración? ¿Migrarlos o solicitar al usuario que reingrese la API key?

---

#### Tarea 6.5.2: Crear Script de Migración de Datos

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

**Preguntas Clave:**

1. ¿Deseas que la migración se ejecute automáticamente al iniciar el backend si detecta que la tabla `settings` existe y `api_keys` no?
2. ¿O prefieres que la migración sea un comando manual que el usuario ejecute?
3. ¿Qué debería pasar si la migración falla? ¿Mostrar error y bloquear el sistema, o permitir continuar con configuración vacía?
4. ¿Deberíamos guardar un registro de la migración en un archivo `migration_log.txt` o solo en logs del backend?
5. ¿Deberíamos mantener la tabla `settings` por un tiempo por si el usuario quiere revertir la migración?

---

#### Tarea 6.5.3: Crear Endpoints CRUD para API Keys

**Archivo:** `backend/app/api/endpoints.py`

**Objetivo:** Implementar endpoints REST para gestionar completamente las API keys (CRUD completo).

##### 6.5.3.1: GET `/api/settings/keys` - Listar API Keys

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

**Pregunta Clave:**
¿Deberíamos incluir también el `model_preference` en la respuesta o solo el `provider` y el estado?

---

##### 6.5.3.2: POST `/api/settings/keys` - Agregar Nueva API Key

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

**Preguntas Clave:**

1. ¿Deseas que la validación con el servicio se haga de forma síncrona o asíncrona?
2. ¿Qué modelo usar para la validación? ¿Uno económico (`gpt-3.5-turbo`) o el que el usuario seleccionó como preferido?
3. ¿Deberíamos guardar un registro de intentos fallidos de validación para detectar posibles ataques?
4. ¿Cuál debería ser el límite de keys por proveedor? ¿3, 5, o sin límite?
5. ¿Qué hacer si el proveedor seleccionado no soporta el modelo preferido? ¿Usar un modelo default o mostrar error?

---

##### 6.5.3.3: DELETE `/api/settings/keys/{key_id}` - Eliminar API Key

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

**Preguntas Clave:**

1. ¿Deseas que la confirmación se haga en el backend (requerir confirmación) o en el frontend (modal)?
2. Si el usuario confirma eliminar la última key y no agrega una nueva, ¿qué debería pasar? ¿Bloquear el sistema con mensaje instructivo?
3. ¿Deberíamos ofrecer la opción "Eliminar y Agregar Nueva" en el mismo flujo?
4. ¿Deberíamos guardar un log de eliminaciones (quién, cuándo, qué key) para auditoría?
5. ¿Deseas un período de "papelera" (por ejemplo, keys eliminadas pero recuperables por 24 horas)?

---

##### 6.5.3.4: PUT `/api/settings/keys/{key_id}/activate` - Activar API Key

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

**Pregunta Clave:**
¿Deseas que al activar una key, se envíe una notificación o evento (para mostrar en el frontend que la key cambió)?

---

##### 6.5.3.5: GET `/api/settings/validate-active` - Validar Configuración

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

**Pregunta Clave:**
¿Deseas incluir en la respuesta también la lista de providers que tienen keys (aunque estén inactivas) para mostrar en la UI?

---

#### Tarea 6.5.4: Crear UI de Settings para Gestión de API Keys

**Archivo:** `frontend/src/components/api-keys-manager.tsx`

**Objetivo:** Componente completo para gestión visual de API keys.

##### 6.5.4.1: Estado y Datos del Componente

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

##### 6.5.4.2: Función de Carga de API Keys

**Objetivo:** Cargar la lista de API keys desde el backend.

**Implementación:**
- Llamar a `GET /api/settings/keys` al montar el componente
- Guardar respuesta en estado
- Manejar errores de carga
- Implementar refresh manual (botón de recargar)

**Pregunta Clave:**
¿Deseas que la lista se cargue automáticamente al montar el componente o solo cuando el usuario hace clic en un botón de "Cargar"?

##### 6.5.4.3: Renderizado de Lista de API Keys

**Objetivo:** Mostrar lista visual de todas las API keys con su estado.

**Implementación:**
- Card o fila por cada API key
- Mostrar: Provider, Modelo Preferido, Estado (Activa/Inactiva), Fecha de creación
- Indicador visual de cuál está activa (badges, colores)
- Badges para proveedores (OpenAI = 🔵, Anthropic = 🟣, Ollama = 🟢)

**Preguntas Clave:**

1. ¿Deseas que la lista sea en formato de cards (vertical) o tabla (horizontal con columnas)?
2. ¿Deberíamos mostrar el modelo preferido en la lista o solo el provider y el estado?
3. ¿Deseas agregar información adicional como "Última vez usada" o "Cantidad de usos"?
4. ¿Deberíamos implementar búsqueda/filtro en la lista de API keys?

##### 6.5.4.4: Modal para Agregar Nueva API Key

**Objetivo:** Formulario modal para agregar una nueva API key con validación.

**Implementación:**
- Selector de Proveedor (OpenAI, Anthropic, Ollama)
- Campo de API Key (tipo password para ocultar caracteres)
- Selector de Modelo Preferido (según proveedor seleccionado)
- Botón "Validate & Save" con indicador de carga
- Validación en tiempo real (mostrar ✓ o ✗ mientras escribe)
- Cerrar modal al guardar exitosamente

**Preguntas Clave:**

1. ¿Deseas que la validación se haga al perder foco del campo (onBlur) o mientras escribe (onChange con debounce)?
2. ¿Deberíamos mostrar mensajes de error específicos (ej: "Formato inválido para OpenAI")?
3. ¿Deseas agregar un botón de "Paste" para facilitar pegar la API key desde el portapapeles?

##### 6.5.4.5: Modal de Confirmación de Eliminación

**Objetivo:** Modal que requiere confirmación antes de eliminar una API key.

**Implementación:**
- Mostrar información de la key a eliminar
- Advertencia clara del impacto
- Opciones: "Cancelar", "Eliminar y Agregar Nueva", "Solo Eliminar"
- Validar que si es la última key activa, se oferteca agregar una nueva

**Pregunta Clave:**
¿Deseas agregar una opción de "Papelera" donde las keys eliminadas se guarden por 24 horas y puedan recuperarse?

---

#### Tarea 6.5.5: Integración con UI Existente

**Archivos:** `frontend/src/app/page.tsx`, `frontend/src/components/ui/button.tsx`

**Objetivo:** Integrar el nuevo sistema de gestión de API keys con la UI existente.

##### 6.5.5.1: Agregar Botón de Acceso a Settings

**Objetivo:** Botón en el header para acceder a settings desde cualquier vista.

**Implementación:**
- Botón con icono de configuración (⚙️)
- Colocado en el header de la aplicación
- Redirigir a vista de settings
- Visible en todas las páginas (usar layout principal)

**Pregunta Clave:**
¿Deseas que el botón de settings esté siempre visible o solo cuando hay una API key configurada?

##### 6.5.5.2: Verificar Configuración al Iniciar

**Objetivo:** Validar que hay una API key activa antes de mostrar la interfaz principal.

**Implementación:**
- Al montar `page.tsx`, llamar a `GET /api/settings/validate-active`
- Si no hay key activa → Mostrar onboarding
- Si hay key activa → Mostrar interfaz principal
- Guardar resultado en estado para evitar validaciones repetidas

**Preguntas Clave:**

1. ¿Deseas que esta validación se haga cada vez que se carga la página o solo una vez y guardar en estado?
2. ¿Qué debería pasar si la validación falla por error de red? ¿Mostrar mensaje o intentar de nuevo?
3. ¿Deseas agregar un indicador de "Conectando..." mientras se valida la configuración?
4. ¿Deberíamos permitir acceder a settings aunque no haya key activa (para agregar una)?

##### 6.5.5.3: Actualizar Store de Workflow

**Archivo:** `frontend/src/store/workflowStore.ts`

**Objetivo:** Integrar validación de configuración en las acciones del workflow.

**Implementación:**
- Agregar función `checkActiveKeys()` al store
- Llamar antes de cada acción que requiera API key
- Manejar caso de no hay key activa (redirigir a settings)
- Mostrar error apropiado si no hay key

**Pregunta Clave:**
¿Deseas que la validación se haga antes de cada acción (costoso en llamadas) o solo al inicio de la sesión y guardar en caché?

---

#### Tarea 6.5.6: Testing y Validación

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

**Preguntas Clave:**

1. ¿Deseas que las pruebas sean manuales (usando la UI) o automatizadas (scripts de test)?
2. ¿Deseas incluir tests de integración que prueben la API directamente?
3. ¿Deberíamos probar también el límite de 3 keys por proveedor?

---

### 📊 Summary de Fase 6.5

#### Archivos a Crear/Modificar

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

#### Tareas Totales: 6
1. [ ] 6.5.1: Rediseñar modelo de base de datos
2. [ ] 6.5.2: Crear script de migración
3. [ ] 6.5.3: Crear endpoints CRUD para API keys
4. [ ] 6.5.4: Crear UI de Settings
5. [ ] 6.5.5: Integración con UI existente
6. [ ] 6.5.6: Testing y validación

#### Preguntas Clave Totales: 20

---

### 🎯 Criterios de Éxito de Fase 6.5

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

## 7. Fase 7.5: Internacionalización i18n

### 🎯 Objetivos

Implementar soporte completo para dos idiomas (English/Spanish) que afecte tanto la UI como los prompts del agente:
1. Switcher de idioma funcional en la UI
2. Toda la UI en ambos idiomas
3. Templates de prompts del agente en ambos idiomas
4. Workflows adaptados según idioma seleccionado
5. Preferencia de idioma guardada y persistente

### 🗺 Desglose de Tareas

#### Tarea 7.5.1: Crear Templates de Prompts Bilingües

**Archivo:** `backend/app/prompts/i18n_templates.py`

**Objetivo:** Crear templates de prompts para el agente en ambos idiomas (Spanish e English).

**Estado Actual:**
- Templates existen en `backend/app/prompts/templates.py`
- Solo están en español (hardcoded)
- Se usan en `backend/app/agents/nodes.py`

**Estado Objetivo:**
- Crear nuevo archivo `i18n_templates.py` con todos los templates en ambos idiomas
- Implementar función selector de templates según idioma
- Migrar lógica de `nodes.py` para usar templates dinámicos

**Estructura del nuevo archivo:**
```python
# backend/app/prompts/i18n_templates.py

# Templates en Español
ES_CLARIFIER_TEMPLATE = """
Actúa como un agente de clarificación experto en **ESPAÑOL**.
Tu objetivo es analizar la solicitud del usuario y:
1. Identificar ambigüedades
2. Formular preguntas de aclaración
3. Extraer requerimientos finales

Contexto:
{user_input}

Respuesta en formato JSON:
{{
  "questions": [],
  "requirements": {{...}}
}}
"""

ES_GENERATOR_TEMPLATE = """
Eres un ingeniero de prompts experto que trabaja en **ESPAÑOL**.
Tu tarea es crear prompts de alta calidad basados en los requerimientos.

Requerimientos:
{clarified_requirements}

Persona: {persona_name}
Descripción: {persona_description}

Genera un prompt profesional en {target_language}.
"""

ES_EVALUATOR_TEMPLATE = """
Evalúa la calidad del siguiente prompt en **ESPAÑOL**.

Prompt candidato:
{candidate_prompt}

Criterios:
1. Claridad
2. Precisión
3. Eficacia

Calificación (1-10) para cada criterio.
"""

ES_JUDGE_TEMPLATE = """
Actúa como juez experto en **ESPAÑOL**.
Evalúa cuál respuesta es mejor.

Input del usuario:
{original_intent}

Respuestas:
A: {output_a}
B: {output_b}
C: {output_c}

Selecciona el ganador y explica por qué.
"""

ES_REFINER_TEMPLATE = """
Mejora el siguiente prompt basado en el feedback del usuario en **ESPAÑOL**.

Prompt original:
{seed_prompt}

Feedback del usuario:
{user_feedback}

Contexto original:
{original_context}

Genera 3 variaciones mejoradas del prompt.
"""

# Templates en Inglés
EN_CLARIFIER_TEMPLATE = """
Act as an expert clarification agent working in **ENGLISH**.
Your goal is to analyze the user request and:
1. Identify ambiguities
2. Formulate clarification questions
3. Extract final requirements

Context:
{user_input}

Response in JSON format:
{{
  "questions": [],
  "requirements": {{...}}
}}
"""

EN_GENERATOR_TEMPLATE = """
You are an expert prompt engineer working in **ENGLISH**.
Your task is to create high-quality prompts based on requirements.

Requirements:
{clarified_requirements}

Persona: {persona_name}
Description: {persona_description}

Generate a professional prompt in {target_language}.
"""

EN_EVALUATOR_TEMPLATE = """
Evaluate the quality of the following prompt in **ENGLISH**.

Candidate prompt:
{candidate_prompt}

Criteria:
1. Clarity
2. Precision
3. Effectiveness

Rate (1-10) for each criterion.
"""

EN_JUDGE_TEMPLATE = """
Act as an expert judge working in **ENGLISH**.
Evaluate which response is better.

User input:
{original_intent}

Responses:
A: {output_a}
B: {output_b}
C: {output_c}

Select the winner and explain why.
"""

EN_REFINER_TEMPLATE = """
Improve the following prompt based on user feedback in **ENGLISH**.

Original prompt:
{seed_prompt}

User feedback:
{user_feedback}

Original context:
{original_context}

Generate 3 improved variations of the prompt.
"""

# Selector de templates según idioma
def get_templates(language: str = "spanish"):
    """
    Retorna un diccionario con todos los templates según el idioma.
    
    Args:
        language: 'spanish' (default) o 'english'
    
    Returns:
        Dict con keys: 'clarifier', 'generator', 'evaluator', 'judge', 'refiner'
    """
    if language == "english":
        return {
            "clarifier": EN_CLARIFIER_TEMPLATE,
            "generator": EN_GENERATOR_TEMPLATE,
            "evaluator": EN_EVALUATOR_TEMPLATE,
            "judge": EN_JUDGE_TEMPLATE,
            "refiner": EN_REFINER_TEMPLATE
        }
    else:  # spanish (default)
        return {
            "clarifier": ES_CLARIFIER_TEMPLATE,
            "generator": ES_GENERATOR_TEMPLATE,
            "evaluator": ES_EVALUATOR_TEMPLATE,
            "judge": ES_JUDGE_TEMPLATE,
            "refiner": ES_REFINER_TEMPLATE
        }

# Función auxiliar para validar idioma
def is_valid_language(language: str) -> bool:
    """
    Valida que el idioma sea soportado.
    """
    return language.lower() in ["spanish", "english"]
```

**Pasos de Implementación:**

1. **Crear archivo `i18n_templates.py`**
   - Ubicación: `backend/app/prompts/`
   - Importar módulos necesarios (typing, etc.)

2. **Definir templates en español**
   - Traducir templates existentes de `templates.py`
   - Asegurar que toda la lógica esté presente
   - Mantener marcadores de formato: `{user_input}`, `{persona_name}`, etc.

3. **Crear traducciones en inglés**
   - Traducir todos los templates al inglés
   - Mantener estructura idéntica (mismos marcadores de formato)
   - Asegurar que la lógica sea equivalente
   - Considerar maticas culturales en la redacción

4. **Implementar función `get_templates()`**
   - Recibir parámetro `language` (default: "spanish")
   - Retornar diccionario con los 5 templates
   - Validar que el idioma sea soportado
   - Manejar idioma inválido (retornar default o lanzar error)

5. **Validar integridad de templates**
   - Verificar que todos los marcadores de formato estén presentes
   - Comparar estructura de templates ES vs EN
   - Probar formato en ambos idiomas

6. **Considerar idiomas adicionales (futuro)**
   - ¿Deberíamos preparar estructura para agregar portugués, francés, etc.?
   - ¿Cómo organizar templates por idioma (archivos separados o uno grande)?

**Preguntas Clave:**

1. ¿Deseas que los marcadores de formato sean idénticos en ambos idiomas (ej: `{user_input}` siempre, no `{input}` en inglés)?
2. ¿Deseas agregar notas o comentarios en los templates para explicar qué hace cada sección?
3. ¿Deberíamos mantener también los templates originales en `templates.py` o reemplazarlos completamente?
4. ¿Deseas que los nombres de variables sean los mismos en ambos idiomas (ej: `persona_name` en vez de `nombre_persona`)?
5. ¿Deseas que la función `get_templates()` valide el idioma o retorne el default sin advertencias?
6. ¿Hay alguna expresión idiomática o mática cultural que sea difícil de traducir literalmente?

---

#### Tarea 7.5.2: Actualizar Estado del Workflow para Incluir Idioma

**Archivo:** `backend/app/agents/state.py`

**Objetivo:** Agregar el campo `language` al estado del workflow para que los agentes sepan en qué idioma trabajar.

**Estado Actual:**
```python
class PromptState(TypedDict):
    user_input: str
    # ... otros campos
```

**Estado Objetivo:**
```python
class PromptState(TypedDict):
    user_input: str
    language: str  # NUEVO: 'spanish' o 'english'
    requirements: Dict[str, Any] = Field(default_factory=dict)
    # ... otros campos existentes
```

**Pasos de Implementación:**

1. **Agregar campo `language` a `PromptState`**
   - Tipo: `str`
   - Default: `"spanish"` (idioma predeterminado)
   - Descripción: "Idioma de interacción seleccionado por el usuario"

2. **Definir valores válidos**
   - Documentar que los valores válidos son: `"spanish"`, `"english"`
   - Considerar validación en getters/setters

3. **Actualizar inicialización del estado**
   - Modificar puntos donde se crea el estado inicial
   - Asegurar que `language` tenga el valor default

4. **Validar compatibilidad con LangGraph**
   - Verificar que agregar un campo no rompa el workflow
   - Probar que el campo se propaga correctamente entre nodos

**Preguntas Clave:**

1. ¿Deseas que `language` sea requerido o opcional (con default)?
2. ¿Deberíamos agregar validación para asegurar que solo se use "spanish" o "english"?
3. ¿Deseas agregar también un campo `ui_language` separado de `interaction_language`?
4. ¿Deberíamos mantener el nombre en inglés (`language`) o usar `idioma` en español?

---

#### Tarea 7.5.3: Integrar Templates i18n en Nodos del Workflow

**Archivo:** `backend/app/agents/nodes.py`

**Objetivo:** Actualizar todos los nodos para usar los templates dinámicos según el idioma del estado.

**Estado Actual:**
```python
from app.prompts.templates import CLARIFIER_TEMPLATE, GENERATOR_TEMPLATE, # ...

async def clarify_node(state: PromptState):
    # ...
    prompt = CLARIFIER_TEMPLATE.format(
        user_input=user_input,
        interaction_language="Spanish"
    )
    # ...
```

**Estado Objetivo:**
```python
from app.prompts.i18n_templates import get_templates

async def clarify_node(state: PromptState):
    # ...
    language = state.get("language", "spanish")
    templates = get_templates(language)
    
    prompt = templates["clarifier"].format(
        user_input=user_input,
        interaction_language="Spanish" if language == "spanish" else "English"
    )
    # ...
```

**Pasos de Implementación:**

1. **Actualizar imports en `nodes.py`**
   - Importar `get_templates` desde `i18n_templates.py`
   - Remover import de `templates.py` (mantener ambos por compatibilidad)

2. **Actualizar `clarify_node()`**
   - Obtener `language` del estado
   - Obtener templates según idioma
   - Usar template correspondiente al formatear prompt
   - Mantener toda la lógica existente

3. **Actualizar `generate_node()`**
   - Obtener `language` del estado
   - Obtener templates según idioma
   - Usar template `generator` correspondiente
   - Asegurar que `target_language` en el prompt sea el idioma correcto

4. **Actualizar `evaluate_node()`**
   - Obtener `language` del estado
   - Obtener templates según idioma
   - Usar template `evaluator` correspondiente
   - Mantener lógica de evaluación

5. **Actualizar `judge_node()`**
   - Obtener `language` del estado
   - Obtener templates según idioma
   - Usar template `judge` correspondiente

6. **Actualizar `refiner_node()`**
   - Obtener `language` del estado
   - Obtener templates según idioma
   - Usar template `refiner` correspondiente
   - Mantener lógica de refinamiento

7. **Pruebas de integración**
   - Probar cada nodo con idioma "spanish"
   - Probar cada nodo con idioma "english"
   - Verificar que los prompts se generan en el idioma correcto

**Preguntas Clave:**

1. ¿Deseas que mantengamos ambos imports (templates.py y i18n_templates.py) por compatibilidad o solo usar i18n?
2. ¿Deseas que la lógica de selección de idioma se centralice en una función auxiliar que usen todos los nodos?
3. ¿Qué debería pasar si el estado no tiene el campo `language`? ¿Usar default o lanzar error?
4. ¿Deseas agregar logging para rastrear qué idioma se está usando en cada ejecución?
5. ¿Deberíamos validar que el template seleccionado exista antes de usarlo (defensivo)?

---

#### Tarea 7.5.4: Crear Endpoint de Configuración de Idioma

**Archivo:** `backend/app/api/endpoints.py`

**Objetivo:** Implementar endpoints para guardar y obtener la preferencia de idioma del usuario.

##### 7.5.4.1: GET `/api/settings/language` - Obtener Idioma Actual

**Objetivo:** Retornar el idioma actual configurado por el usuario.

**Implementación:**
- Consultar base de datos para obtener preferencia de idioma
- Si no hay configuración, retornar default ("spanish")
- Retornar en formato JSON

**Request esperado:**
```http
GET /api/settings/language
```

**Response esperado:**
```json
{
  "status": "success",
  "language": "spanish",
  "supported_languages": ["spanish", "english"]
}
```

**Preguntas Clave:**

1. ¿Deseas almacenar la preferencia de idioma en la tabla `api_keys` o crear una tabla `user_preferences`?
2. ¿Deseas que la respuesta incluya también los metadatos del idioma (nombre, código, dirección del texto)?
3. ¿Deberíamos incluir en la respuesta también la fecha de la última vez que se cambió el idioma?

##### 7.5.4.2: POST `/api/settings/language` - Guardar Preferencia de Idioma

**Request esperado:**
```http
POST /api/settings/language
Content-Type: application/json

{
  "language": "spanish"
}
```

**Implementación:**
- Validar que el idioma sea soportado ("spanish" o "english")
- Guardar en base de datos
- Retornar confirmación
- Manejar errores de validación

**Validaciones requeridas:**
- `language` no debe estar vacío
- `language` debe ser uno de: "spanish", "english"
- Validación case-insensitive (aceptar "Spanish", "SPANISH", etc.)
- Retornar error 400 si el idioma no es válido

**Response exitoso:**
```json
{
  "status": "success",
  "message": "Language preference saved",
  "language": "spanish"
}
```

**Response con error:**
```json
{
  "status": "error",
  "message": "Invalid language. Supported languages: spanish, english",
  "supported_languages": ["spanish", "english"]
}
```

**Almacenamiento en base de datos:**
- **Opción A:** Agregar campo `language_preference` a la tabla `api_keys`
  - Pros: Simple, un solo lugar
  - Contras: ¿Qué pasa si el usuario elimina todas las keys?

- **Opción B:** Crear tabla `user_settings` independiente
  - Pros: Más flexible, soporta más configuraciones futuras
  - Contras: Más complejo

**Preguntas Clave:**

1. ¿Prefieres almacenar la preferencia de idioma en la tabla `api_keys` (Opción A) o crear una tabla `user_settings` (Opción B)?
2. ¿Deseas que al guardar el idioma, se actualice también el estado de cualquier workflow activo en memoria?
3. ¿Deberíamos enviar un evento o notificación cuando se cambia el idioma?
4. ¿Deseas agregar un campo `last_changed_at` para rastrear cuándo se modificó el idioma?
5. ¿Deseas que el endpoint valide si el usuario tiene permisos para cambiar configuraciones?

---

#### Tarea 7.5.5: Crear Provider de Idiomas (React Context)

**Archivo:** `frontend/src/contexts/LanguageContext.tsx`

**Objetivo:** Crear un React Context para gestionar el idioma de la aplicación y proporcionar funciones de traducción.

**Estructura del componente:**
```typescript
'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

// Tipos
type Language = 'english' | 'spanish';

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: string) => string; // Función de traducción
  isLoading: boolean;
}

// Crear el Context
const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

// Provider Component
export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguage] = useState<Language>('spanish'); // Default
  const [translations, setTranslations] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  // Cargar traducciones al cambiar idioma
  useEffect(() => {
    loadTranslations(language);
  }, [language]);

  // Cargar idioma inicial al montar
  useEffect(() => {
    const savedLanguage = localStorage.getItem('promptforge_language') as Language;
    if (savedLanguage) {
      setLanguage(savedLanguage);
    } else {
      // Cargar desde backend
      loadSavedLanguage();
    }
  }, []);

  const loadTranslations = async (lang: Language) => {
    setIsLoading(true);
    try {
      const res = await fetch(`/i18n/${lang}.json`);
      const data = await res.json();
      setTranslations(data);
      setIsLoading(false);
    } catch (error) {
      console.error('Error loading translations:', error);
      setIsLoading(false);
    }
  };

  const loadSavedLanguage = async () => {
    try {
      const res = await fetch(`${API_BASE}/settings/language`);
      const data = await res.json();
      if (data.status === 'success') {
        setLanguage(data.language);
      }
    } catch (error) {
      console.error('Error loading saved language:', error);
    }
  };

  const setLanguage = (lang: Language) => {
    setLanguage(lang);
    localStorage.setItem('promptforge_language', lang);
    loadTranslations(lang);
    
    // Guardar preferencia en backend
    fetch(`${API_BASE}/settings/language`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ language: lang }),
    });
  };

  const t = (key: string) => {
    return translations[key] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t, isLoading }}>
      {children}
    </LanguageContext.Provider>
  );
}

// Hook personalizado
export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}
```

**Pasos de Implementación:**

1. **Crear archivo `LanguageContext.tsx`**
   - Ubicación: `frontend/src/contexts/`
   - Crear directorio `contexts` si no existe

2. **Definir tipos**
   - `Language`: Union type con 'english' | 'spanish'
   - `LanguageContextType`: Interface con estado y funciones
   - Validar tipos con TypeScript

3. **Implementar `LanguageProvider`**
   - Estado inicial: `language = 'spanish'` (default)
   - Función `setLanguage`: Cambiar idioma
   - Función `t`: Obtener traducción
   - Función `loadTranslations`: Cargar archivo JSON
   - Manejo de errores de carga

4. **Implementar persistencia local**
   - Usar `localStorage` para guardar preferencia
   - Leer del localStorage al montar
   - Sincronizar con backend

5. **Implementar `useLanguage` hook**
   - Validar que el context exista
   - Lanzar error si se usa fuera del provider
   - Retornar contexto completo

6. **Agregar caché de traducciones**
   - Almacenar traducciones en estado
   - Evitar recargar el archivo JSON en cada render
   - Actualizar caché al cambiar idioma

**Preguntas Clave:**

1. ¿Deseas que el idioma se guarde automáticamente en localStorage, solo backend, o ambos?
2. ¿Deseas agregar un indicador de "cargando traducciones..." mientras se carga el archivo JSON?
3. ¿Deberíamos usar una biblioteca como `i18next` o implementar el sistema nosotros?
4. ¿Deseas que el contexto también exponga las listas de idiomas disponibles y sus metadatos?
5. ¿Cómo manejar el caso donde el archivo de traducción no tenga una key (fallback al key original)?

---

#### Tarea 7.5.6: Crear Archivos de Traducción (JSON)

**Archivos:** `frontend/public/i18n/spanish.json`, `frontend/public/i18n/english.json`

**Objetivo:** Crear archivos JSON con todas las traducciones de la UI en ambos idiomas.

**Estructura de los archivos:**
```json
{
  "welcome_title": "Bienvenido a PromptForge",
  "welcome_subtitle": "Herramienta Profesional de Ingeniería de Prompts",
  "configure_provider": "Configura tu proveedor de LLM",
  "provider": "Proveedor",
  "api_key": "API Key",
  "validate_save": "Validar y Guardar",
  "setup_complete": "¡Configuración Completa!",
  "api_key_secure": "Tu API key ha sido almacenada de forma segura.",
  "continue_app": "Continuar a la Aplicación",
  "settings": "Configuración",
  "api_keys": "API Keys",
  "add_key": "Agregar Nueva Key",
  "delete_key": "Eliminar Key",
  "activate_key": "Activar",
  "confirm_delete": "¿Estás seguro de eliminar esta API Key?",
  "no_active_key": "No hay ninguna API Key activa",
  "what_build": "¿Qué deseas construir?",
  "describe_task": "Describe tu tarea, y te ayudaré a crear el prompt perfecto.",
  "clarification": "Clarificación",
  "generation": "Generación",
  "evaluation": "Evaluación",
  "arena": "Arena",
  "language_spanish": "Español",
  "language_english": "English",
  "select_language": "Seleccionar Idioma",
  "provider_openai": "OpenAI",
  "provider_anthropic": "Anthropic",
  "provider_ollama": "Ollama (Local)",
  "model_gpt4": "GPT-4",
  "model_gpt35_turbo": "GPT-3.5 Turbo",
  "model_claude3": "Claude 3",
  "error_network": "Error de red",
  "error_api_key_invalid": "API Key inválida",
  "retry": "Reintentar"
}
```

**Pasos de Implementación:**

1. **Crear directorio `i18n` en `frontend/public/`**
   - Ruta: `frontend/public/i18n/`
   - Verificar que Next.js sirve archivos estáticos desde `public/`

2. **Crear archivo `spanish.json`**
   - Traducir TODOS los textos de la UI al español
   - Agrupar por funcionalidad (onboarding, settings, workflow, arena)
   - Usar keys consistentes (snake_case o camelCase)

3. **Crear archivo `english.json`**
   - Traducir TODOS los textos de la UI al inglés
   - Mantener las mismas keys que `spanish.json`
   - Asegurar traducciones naturales y contextuales

4. **Validar estructura de ambos archivos**
   - Verificar que tengan las mismas keys
   - Comparar cantidad de entradas
   - Verificar que no haya keys vacías

5. **Considerar anidación para organizacion**
   - ¿Deberíamos agrupar traducciones por sección?
   - Ejemplo: `{ "onboarding": { "title": "...", "subtitle": "..." } }`

**Textos a traducir (inventario preliminar):**

**Onboarding:**
- Títulos, subtítulos, descripciones
- Labels de formularios
- Botones y acciones
- Mensajes de error y éxito

**Settings:**
- Nombres de secciones
- Labels de campos
- Botones de acción
- Mensajes de confirmación

**Workflow (Chat/Clarificación):**
- Títulos de chat
- Labels de input
- Botones de envío
- Mensajes de estado

**Arena:**
- Títulos de variantes
- Labels de evaluación
- Botones de acción
- Mensajes de feedback

**General:**
- Navegación
- Mensajes de error
- Indicadores de carga

**Preguntas Clave:**

1. ¿Deseas usar snake_case para las keys (`welcome_title`) o camelCase (`welcomeTitle`)?
2. ¿Deseas que las keys sigan una convención de prefijos por funcionalidad (ej: `onboarding.title`)?
3. ¿Deseas agregar metadatos de contexto (ej: `context: "onboarding"`) para ayudarte a organizar?
4. ¿Cómo manejar textos que son iguales en ambos idiomas (ej: "OpenAI", "GPT-4")? ¿Duplicar o centralizar?
5. ¿Deseas agregar un campo `__metadata` en cada archivo JSON con información sobre la traducción (autor, fecha)?

---

#### Tarea 7.5.7: Crear Componente Switcher de Idioma

**Archivo:** `frontend/src/components/language-switcher.tsx`

**Objetivo:** Componente UI para permitir al usuario cambiar el idioma de la aplicación.

**Ejemplo de implementación:**
```typescript
'use client';

import { useLanguage } from '@/contexts/LanguageContext';
import { Globe, Languages } from 'lucide-react';

export function LanguageSwitcher() {
  const { language, setLanguage, t } = useLanguage();

  const handleLanguageChange = (lang: 'spanish' | 'english') => {
    setLanguage(lang);
  };

  return (
    <div className="flex items-center gap-2">
      <Globe className="w-4 h-4 text-muted-foreground" />
      <select
        value={language}
        onChange={(e) => handleLanguageChange(e.target.value as 'spanish' | 'english')}
        className="bg-transparent border-none text-sm font-medium cursor-pointer focus:outline-none"
        aria-label={t('select_language')}
      >
        <option value="spanish">🇪🇸 Español</option>
        <option value="english">🇬🇧 English</option>
      </select>
    </div>
  );
}
```

**Pasos de Implementación:**

1. **Crear archivo `language-switcher.tsx`**
   - Ubicación: `frontend/src/components/`
   - Importar `useLanguage` hook

2. **Implementar diseño visual**
   - Usar ícono de globo/lenguas
   - Dropdown con emojis de banderas
   - Estilo consistente con el resto de la UI

3. **Agregar accesibilidad**
   - Atributo `aria-label` para screen readers
   - Soporte para navegación por teclado
   - Contraste de colores adecuado

4. **Posicionamiento en la UI**
   - Colocar en el header principal
   - Visible en todas las páginas
   - Fácil acceso

5. **Considerar animaciones**
   - Transición suave al cambiar idioma
   - Feedback visual de cambio
   - Indicador de carga si las traducciones toman tiempo

**Preguntas Clave:**

1. ¿Deseas que el switcher use un dropdown (select) como en el ejemplo, o prefieres botones de toggle (dos botones)?
2. ¿Deseas incluir el nombre del idioma en texto además del emoji de bandera?
3. ¿Deseas agregar un indicador visual de qué idioma está activo (subrayado, background, etc.)?
4. ¿Deseas que el switcher tenga un tooltip explicando qué hace (para usuarios nuevos)?
5. ¿Deseas agregar un shortcut de teclado para cambiar idioma (ej: Ctrl+L)?

---

#### Tarea 7.5.8: Integrar LanguageContext en Layout Principal

**Archivo:** `frontend/src/app/layout.tsx`

**Objetivo:** Envolver toda la aplicación con el `LanguageProvider` para que todos los componentes tengan acceso a las traducciones.

**Pasos de Implementación:**

1. **Importar `LanguageProvider`**
   - Importar desde `@/contexts/LanguageContext`
   - Verificar ruta de import correcta

2. **Envolver `{children}` con `LanguageProvider`**
   - Modificar el return del componente
   - Asegurar que envuelve solo una vez

3. **Actualizar atributo `lang` del HTML**
   - Cambiar de estático `lang="en"` a dinámico según idioma seleccionado
   - Esto ayuda a screen readers y herramientas de accesibilidad

**Preguntas Clave:**

1. ¿Deseas que el atributo `lang` del HTML se actualice automáticamente cuando cambia el idioma o solo al recargar la página?
2. ¿Deberíamos cambiar también la dirección del texto del HTML (`dir="ltr"` o `dir="rtl"`) según el idioma?
3. ¿Deseas agregar también metadatos de SEO (`<title>`, `<meta>`) que cambien según el idioma?
4. ¿Deseas que el `LanguageProvider` esté dentro o fuera del `ThemeProvider`? ¿Qué orden es mejor?

---

#### Tarea 7.5.9: Migrar Componentes Existentes para Usar Traducciones

**Archivos:** Múltiples componentes en `frontend/src/components/` y `frontend/src/app/`

**Objetivo:** Reemplazar todos los textos fijos (hardcoded) por llamadas a la función `t()` del contexto de idioma.

**Componentes a migrar:**

1. **Onboarding Form** (`frontend/src/components/onboarding-form.tsx`)
   - Títulos y subtítulos
   - Labels de formularios
   - Mensajes de error y éxito
   - Botones

2. **Settings Page** (cuando se cree)
   - Nombres de secciones
   - Labels de campos
   - Botones de acción

3. **Main Page** (`frontend/src/app/page.tsx`)
   - "What do you want to build?"
   - "Describe your task..."
   - Botones de acción

4. **Chat Interface** (`frontend/src/components/arena/ChatInterface.tsx`)
   - Títulos de chat
   - Mensajes de estado
   - Botones

5. **Arena View** (`frontend/src/components/arena/ArenaView.tsx`)
   - Títulos de variantes
   - Labels de evaluación
   - Botones de acción

6. **API Keys Manager** (cuando se cree en fase 6.5)
   - Todos los textos relacionados con gestión de keys

**Proceso de migración:**

1. **Importar `useLanguage` hook**
   - `import { useLanguage } from '@/contexts/LanguageContext';`

2. **Usar hook en cada componente**
   - `const { t } = useLanguage();`

3. **Reemplazar textos fijos**
   - Antes: `<h1>Welcome to PromptForge</h1>`
   - Después: `<h1>{t('welcome_title')}</h1>`

4. **Validar que no queden textos sin traducir**
   - Buscar strings literales en inglés o español
   - Crear keys en los archivos JSON

5. **Pruebas de integración**
   - Cambiar idioma y verificar que todo se actualice
   - Verificar que no haya textos mezclados (algunos traducidos, otros no)

**Preguntas Clave:**

1. ¿Deseas que hagamos la migración componente por componente (más lento pero más controlado) o en un solo cambio masivo?
2. ¿Cómo manejar textos dinámicos que incluyen variables (ej: "Hola, {nombre}")? ¿Interpolación o pasar parámetros a `t()`?
3. ¿Deseas que agreguemos un script o herramienta que escanee todos los archivos buscando textos en inglés/español para no olvidar ninguno?
4. ¿Deberíamos agregar una función `t()` que acepte parámetros para interpolación (ej: `t('welcome', {name: 'Juan'})`)?
5. ¿Qué hacer con textos que son idénticos en ambos idiomas (ej: "OpenAI", "GPT-4")? ¿Traducir de todas formas o centralizar?

---

#### Tarea 7.5.10: Integrar LanguageSwitcher en el Header

**Archivos:** `frontend/src/app/layout.tsx` o componente de header dedicado

**Objetivo:** Agregar el componente `LanguageSwitcher` en una posición visible y accesible del header principal.

**Pasos de Implementación:**

1. **Importar `LanguageSwitcher`**
   - Importar componente desde `@/components/language-switcher`

2. **Posicionar en el header**
   - Colocar junto con el botón de tema (sol/luna)
   - O en el lado derecho del header
   - Visible en todas las páginas

3. **Estilo y diseño**
   - Consistente con el resto del header
   - Responsive (funciona en móvil)
   - Espaciado adecuado

**Preguntas Clave:**

1. ¿Deseas que el LanguageSwitcher esté a la izquierda (cerca del logo) o a la derecha (cerca del botón de tema)?
2. ¿Deseas agregar también un indicador en el footer (adicionalmente al header)?
3. ¿Deberíamos mostrar el idioma actual como texto además del switcher (ej: "Idioma: 🇪🇸")?
4. ¿Deseas que el switcher se colapse en una vista más compacta cuando hay poco espacio horizontal?
5. ¿Deberíamos agregar un atajo de teclado para abrir el switcher rápidamente?

---

#### Tarea 7.5.11: Testing y Validación de i18n

**Objetivo:** Probar completamente que la internacionalización funciona correctamente en toda la aplicación.

**Casos de prueba:**

1. **Cambio de idioma desde el switcher**
   - Cambiar a español → Verificar que toda la UI cambie
   - Cambiar a inglés → Verificar que toda la UI cambie
   - Verificar persistencia (al recargar página, mantener idioma seleccionado)

2. **Carga inicial de idioma**
   - Recargar página con idioma guardado
   - Verificar que carga correctamente
   - No debería mostrar idioma default si hay uno guardado

3. **Persistencia de idioma**
   - Cerrar y abrir navegador → Verificar idioma se mantiene
   - Limpiar localStorage → Verificar que carga desde backend

4. **Traducciones de prompts del agente**
   - Iniciar workflow en español → Verificar que prompts sean en español
   - Iniciar workflow en inglés → Verificar que prompts sean en inglés
   - Verificar que la respuesta del LLM se adapte al idioma

5. **Integración con otras funcionalidades**
   - Verificar que onboarding funcione en ambos idiomas
   - Verificar que settings funcionen en ambos idiomas
   - Verificar que workflow/arena funcionen en ambos idiomas

6. **Casos edge**
   - Cambiar idioma durante una ejecución de workflow
   - Cambiar idioma con errores de red
   - Cambiar idioma con API key inválida

**Preguntas Clave:**

1. ¿Deseas que creemos un checklist manual de pruebas o un script automatizado?
2. ¿Qué criterios de éxito considerar para cada caso de prueba?
3. ¿Deseas incluir screenshots en el checklist para documentación visual?
4. ¿Cómo manejar los casos edge mencionados? ¿Cancelar ejecución, bloquear cambio, o permitir?
5. ¿Deseas que creemos un reporte de pruebas con bugs encontrados y su severidad?

---

### 📊 Summary de Fase 7.5

#### Archivos a Crear

**Backend:**
1. `backend/app/prompts/i18n_templates.py` - Templates bilingües
2. `backend/app/api/endpoints.py` (actualizar) - Endpoint de idioma

**Frontend:**
1. `frontend/src/contexts/LanguageContext.tsx` - Context de idioma
2. `frontend/public/i18n/spanish.json` - Traducciones ES
3. `frontend/public/i18n/english.json` - Traducciones EN
4. `frontend/src/components/language-switcher.tsx` - Switcher UI

#### Archivos a Modificar:
1. `backend/app/agents/state.py` - Agregar campo `language`
2. `backend/app/agents/nodes.py` - Usar templates dinámicos
3. `frontend/src/app/layout.tsx` - Envolver con `LanguageProvider`
4. Múltiples componentes - Reemplazar textos fijos por `t()`

#### Tareas Totales: 11
1. [ ] 7.5.1: Crear templates bilingües
2. [ ] 7.5.2: Actualizar estado del workflow
3. [ ] 7.5.3: Integrar templates en nodos
4. [ ] 7.5.4: Crear endpoint de idioma
5. [ ] 7.5.5: Crear provider React Context
6. [ ] 7.5.6: Crear archivos de traducción
7. [ ] 7.5.7: Crear componente switcher
8. [ ] 7.5.8: Integrar en layout
9. [ ] 7.5.9: Migrar componentes existentes
10. [ ] 7.5.10: Integrar switcher en header
11. [ ] 7.5.11: Testing y validación

#### Preguntas Clave Totales: 42

---

### 🎯 Criterios de Éxito de Fase 7.5

Al completar esta fase, el sistema deberá:

1. ✅ Switcher de idioma funcional y visible en el header
2. ✅ Toda la UI traducida en inglés y español
3. ✅ Templates de prompts del agente en ambos idiomas
4. ✅ Workflows adaptados según idioma seleccionado
5. ✅ Preferencia de idioma guardada y persistente
6. ✅ Persistencia en localStorage y backend
7. ✅ Cambio de idioma fluido sin recargar la página
8. ✅ Integración correcta con todas las funcionalidades existentes
9. ✅ Testing completo en ambos idiomas
10. ✅ Documentación actualizada con i18n

---

## 8. Fase 8: Tipos de Prompt Modulares

### 🎯 Objetivos

Implementar una arquitectura modular que soporte múltiples tipos de prompt con workflows específicos para cada uno:
1. **Basic** (ya funcional - ✅) - Prompt estándar para tareas generales
2. **System Prompt** (requiere input de prueba) - Para configurar comportamiento del modelo
3. **Image Prompt** - Para generación de imágenes (DALL-E, Midjourney, etc.)
4. **Additional Prompt** - Prompts complementarios o adicionales
5. Arquitectura escalable para habilitar nuevos tipos en el futuro
6. Workflows específicos para cada tipo de prompt
7. Factory Pattern para seleccionar el workflow correcto
8. UI intuitiva para seleccionar tipo de prompt

### 🗺 Desglose de Tareas

#### Tarea 8.1: Crear Enumeración de Tipos de Prompt

**Archivo:** `backend/app/core/prompt_types.py`

**Objetivo:** Definir enumeración y configuraciones de todos los tipos de prompt que el sistema soportará.

**Estado Actual:**
- No existe ningún sistema de tipos de prompt
- Solo existe workflow básico (hardcoded)
- No hay distinción entre tipos de prompts

**Estado Objetivo:**
```python
# backend/app/core/prompt_types.py

from enum import Enum
from typing import Dict, Any, List

class PromptType(Enum):
    """Enumeración de tipos de prompt soportados."""
    BASIC = "basic"            # ✅ Habilitado (ya funcional)
    SYSTEM = "system"           # ⏳ Fase 8.6 habilitará esto
    IMAGE = "image"            # ⏳ Fase 8.7 habilitará esto
    ADDITIONAL = "additional"    # ⏳ Fase 8.8 habilitará esto

# Descripciones y configuraciones por tipo
PROMPT_TYPE_CONFIGS: Dict[str, Dict[str, Any]] = {
    PromptType.BASIC.value: {
        "name": "Basic Prompt",
        "description": "Prompt estándar para tareas generales de ingeniería de prompts",
        "requires_test_input": False,
        "workflow_graph": "basic_workflow",
        "enabled": True,  # Disponible para uso
        "icon": "📝",
        "color": "blue",
        "category": "general"
    },
    PromptType.SYSTEM.value: {
        "name": "System Prompt",
        "description": "Prompt de sistema para configurar el comportamiento y rol del modelo",
        "requires_test_input": True,  # Requiere input de usuario para probar
        "workflow_graph": "system_prompt_workflow",
        "enabled": False,  # Fase 8.6 habilitará esto
        "icon": "⚙️",
        "color": "purple",
        "category": "configuration"
    },
    PromptType.IMAGE.value: {
        "name": "Image Prompt",
        "description": "Prompt especializado para generación de imágenes (DALL-E, Midjourney, Stable Diffusion)",
        "requires_test_input": False,
        "workflow_graph": "image_prompt_workflow",
        "enabled": False,  # Fase 8.7 habilitará esto
        "icon": "🖼️",
        "color": "green",
        "category": "creative"
    },
    PromptType.ADDITIONAL.value: {
        "name": "Additional Prompt",
        "description": "Prompt complementario o adicional para tareas específicas",
        "requires_test_input": False,
        "workflow_graph": "additional_prompt_workflow",
        "enabled": False,  # Fase 8.8 habilitará esto
        "icon": "➕",
        "color": "orange",
        "category": "extension"
    }
}

# Funciones auxiliares
def get_prompt_type_config(prompt_type: str) -> Dict[str, Any]:
    """
    Retorna la configuración de un tipo de prompt específico.
    
    Args:
        prompt_type: String del tipo (ej: 'basic', 'system', 'image', 'additional')
    
    Returns:
        Dict con configuración del tipo o dict vacío si no existe.
    
    Raises:
        ValueError: Si el tipo de prompt no existe.
    """
    config = PROMPT_TYPE_CONFIGS.get(prompt_type)
    if not config:
        raise ValueError(f"Prompt type '{prompt_type}' not supported. Available types: {list(PROMPT_TYPE_CONFIGS.keys())}")
    return config

def get_enabled_prompt_types() -> List[str]:
    """
    Retorna lista de tipos de prompt habilitados (enabled = True).
    
    Returns:
        Lista de strings con los IDs de tipos habilitados.
    """
    return [
        ptype for ptype, config in PROMPT_TYPE_CONFIGS.items()
        if config.get("enabled", False)
    ]

def get_all_prompt_types() -> List[Dict[str, Any]]:
    """
    Retorna lista de todos los tipos de prompt con sus configuraciones.
    
    Returns:
        Lista de dicts con información completa de cada tipo.
    """
    return [
        {
            "id": ptype,
            **config
        }
        for ptype, config in PROMPT_TYPE_CONFIGS.items()
    ]

def is_prompt_type_enabled(prompt_type: str) -> bool:
    """
    Verifica si un tipo de prompt está habilitado.
    
    Args:
        prompt_type: String del tipo a verificar
    
    Returns:
        True si está habilitado, False en caso contrario.
    """
    config = PROMPT_TYPE_CONFIGS.get(prompt_type)
    return config.get("enabled", False) if config else False
```

**Preguntas Clave:**

1. ¿Deseas mantener los valores de la enumeración en inglés (`BASIC`, `SYSTEM`) o usar español (`BASICO`, `SISTEMA`)?
2. ¿Deberíamos agregar más metadatos como `difficulty_level`, `estimated_tokens`, `examples`?
3. ¿Los `workflow_graph` deberían ser nombres de funciones o rutas de archivos?
4. ¿Deberíamos agregar validación en `get_prompt_type_config()` para verificar que el tipo sea uno de los valores del enum?
5. ¿Deseas que la función `get_enabled_prompt_types()` retorne solo los IDs o también las configuraciones completas?
6. ¿Deberíamos agregar un tipo `CUSTOM` para permitir workflows personalizados por el usuario?
7. ¿Los iconos y colores (`📝`, `blue`) deberían ser configurables o fijos?
8. ¿Deberíamos agregar un campo `display_order` para controlar el orden en que aparecen los tipos en la UI?

---

#### Tarea 8.2: Crear Factory Pattern para Workflows

**Archivo:** `backend/app/agents/workflow_factory.py`

**Objetivo:** Implementar Factory Pattern para retornar el workflow (grafo) apropiado según el tipo de prompt seleccionado.

**Estado Objetivo:**
```python
# backend/app/agents/workflow_factory.py

from typing import Any
from app.core.prompt_types import PromptType, get_prompt_type_config, is_prompt_type_enabled
from app.agents.graph import get_graph as get_basic_graph
# Importar otros workflows cuando se implementen:
# from app.agents.system_prompt_graph import get_graph as get_system_prompt_graph
# from app.agents.image_prompt_graph import get_graph as get_image_prompt_graph
# from app.agents.additional_prompt_graph import get_graph as get_additional_prompt_graph

def get_workflow_graph(prompt_type: str, checkpointer=None) -> Any:
    """
    Factory Pattern: Retorna el workflow (grafo de LangGraph) apropiado
    según el tipo de prompt seleccionado.
    
    Args:
        prompt_type: String del tipo de prompt ('basic', 'system', 'image', 'additional')
        checkpointer: Checkpointer de LangGraph para persistencia de estado
    
    Returns:
        Objeto de workflow compilado de LangGraph.
    
    Raises:
        ValueError: Si el tipo de prompt no está habilitado.
        ValueError: Si el workflow para el tipo no existe.
    """
    # Obtener configuración del tipo de prompt
    config = get_prompt_type_config(prompt_type)
    
    # Validar que el tipo está habilitado
    if not config.get("enabled", False):
        raise ValueError(
            f"Prompt type '{prompt_type}' is not enabled. "
            f"Current enabled types: {get_enabled_prompt_types()}"
        )
    
    # Obtener nombre del workflow a usar
    workflow_name = config.get("workflow_graph")
    
    # Factory: Importar y retornar el workflow correspondiente
    # Esto permite extensión futura sin modificar código existente
    
    # Workflow básico (ya implementado)
    if workflow_name == "basic_workflow":
        return get_basic_graph(checkpointer)
    
    # Workflows específicos (se implementarán en fases 8.6, 8.7, 8.8)
    elif workflow_name == "system_prompt_workflow":
        # Se implementará en Fase 8.6
        try:
            from app.agents.system_prompt_graph import get_graph as get_system_prompt_graph
            return get_system_prompt_graph(checkpointer)
        except ImportError:
            raise ValueError(
                f"System prompt workflow is not yet implemented. "
                "Check Fase 8.6 for implementation details."
            )
    
    elif workflow_name == "image_prompt_workflow":
        # Se implementará en Fase 8.7
        try:
            from app.agents.image_prompt_graph import get_graph as get_image_prompt_graph
            return get_image_prompt_graph(checkpointer)
        except ImportError:
            raise ValueError(
                f"Image prompt workflow is not yet implemented. "
                "Check Fase 8.7 for implementation details."
            )
    
    elif workflow_name == "additional_prompt_workflow":
        # Se implementará en Fase 8.8
        try:
            from app.agents.additional_prompt_graph import get_graph as get_additional_prompt_graph
            return get_additional_prompt_graph(checkpointer)
        except ImportError:
            raise ValueError(
                f"Additional prompt workflow is not yet implemented. "
                "Check Fase 8.8 for implementation details."
            )
    
    else:
        # Fallback: Workflow no reconocido
        # Usar workflow básico por defecto
        return get_basic_graph(checkpointer)

def get_available_workflows() -> list:
    """
    Retorna lista de workflows disponibles con sus tipos.
    
    Returns:
        Lista de dicts con información de cada workflow disponible.
    """
    available = []
    
    for ptype in get_enabled_prompt_types():
        config = get_prompt_type_config(ptype)
        workflow_name = config.get("workflow_graph")
        
        # Verificar si el workflow está implementado
        implemented = True
        if workflow_name in ["system_prompt_workflow", "image_prompt_workflow", "additional_prompt_workflow"]:
            # A estos workflows se les verificará implementación cuando se usen
            # Por ahora asumimos que no están implementados
            implemented = workflow_name == "basic_workflow"
        
        available.append({
            "prompt_type": ptype,
            "workflow_name": workflow_name,
            "implemented": implemented,
            "config": config
        })
    
    return available
```

**Preguntas Clave:**

1. ¿Deseas que el manejo de errores de importación dinámica sea con try/except o usar una estructura de registro de workflows?
2. ¿Deberíamos agregar un parámetro opcional `fallback_to_basic=True` para decidir qué hacer si el workflow no está implementado?
3. ¿El `checkpointer` debería ser opcional o requerido en todos los workflows?
4. ¿Deseas que el factory valide también que el `checkpointer` sea del tipo correcto antes de usarlo?
5. ¿Deberíamos agregar logging al factory para rastrear qué workflow se está seleccionando?
6. ¿Deseas implementar un caché de workflows para no recrearlos en cada llamada?
7. ¿Qué hacer si múltiples workflows solicitan el mismo checkpointer? ¿Compartir o crear instancias separadas?
8. ¿Deberíamos agregar un método `get_workflow_graph_sync()` para workflows síncronos (si los hubiera)?

---

#### Tarea 8.3: Crear Endpoint de Tipos de Prompt

**Archivo:** `backend/app/api/endpoints.py`

**Objetivo:** Implementar endpoints para listar tipos de prompt disponibles y su estado de habilitación.

##### 8.3.1: GET `/api/prompts/types` - Listar Tipos Disponibles

**Response exitoso:**
```json
{
  "types": [
    {
      "id": "basic",
      "name": "Basic Prompt",
      "description": "Prompt estándar para tareas generales de ingeniería de prompts",
      "enabled": true,
      "requires_test_input": false,
      "workflow_graph": "basic_workflow",
      "icon": "📝",
      "color": "blue",
      "category": "general"
    },
    {
      "id": "system",
      "name": "System Prompt",
      "description": "Prompt de sistema para configurar el comportamiento y rol del modelo",
      "enabled": false,
      "requires_test_input": true,
      "workflow_graph": "system_prompt_workflow",
      "icon": "⚙️",
      "color": "purple",
      "category": "configuration"
    },
    {
      "id": "image",
      "name": "Image Prompt",
      "description": "Prompt especializado para generación de imágenes (DALL-E, Midjourney, Stable Diffusion)",
      "enabled": false,
      "requires_test_input": false,
      "workflow_graph": "image_prompt_workflow",
      "icon": "🖼️",
      "color": "green",
      "category": "creative"
    },
    {
      "id": "additional",
      "name": "Additional Prompt",
      "description": "Prompt complementario o adicional para tareas específicas",
      "enabled": false,
      "requires_test_input": false,
      "workflow_graph": "additional_prompt_workflow",
      "icon": "➕",
      "color": "orange",
      "category": "extension"
    }
  ],
  "total": 4,
  "enabled_count": 1
}
```

##### 8.3.2: GET `/api/prompts/types/available` - Solo Tipos Habilitados

**Response exitoso:**
```json
{
  "types": [
    {
      "id": "basic",
      "name": "Basic Prompt",
      "description": "Prompt estándar para tareas generales",
      "enabled": true,
      "icon": "📝",
      "color": "blue"
    }
  ],
  "total": 1
}
```

**Preguntas Clave:**

1. ¿Deseas mantener ambos endpoints (`/types` y `/types/available`) o solo uno con parámetro para filtrar?
2. ¿Deseas agregar un parámetro de query para ordenar por (`?order=enabled`, `?order=name`)?
3. ¿Deberíamos incluir en la respuesta también información sobre la fecha de habilitación de cada tipo?
4. ¿Deseas agregar un endpoint `GET /api/prompts/types/{id}` para obtener detalles de un tipo específico?
5. ¿Deseas que el endpoint incluya información sobre qué modelos son recomendados para cada tipo de prompt?

---

#### Tarea 8.4: Crear UI de Selector de Tipo de Prompt

**Archivo:** `frontend/src/components/prompt-type-selector.tsx`

**Objetivo:** Componente visual para que el usuario seleccione el tipo de prompt que desea usar.

**Preguntas Clave:**

1. ¿Deseas que el grid sea de 2 columnas como en el ejemplo, o 3 columnas, o responsivo según tamaño de pantalla?
2. ¿Deberíamos agregar un tooltip o descripción emergente al hacer hover en el card de tipo?
3. ¿Deseas mostrar el badge de estado (enabled/coming_soon) como en el ejemplo, o usar estilos diferentes?
4. ¿Qué debería pasar cuando el usuario hace clic en un tipo no habilitado? ¿Mostrar un alert (como en el ejemplo) o un modal más elegante?
5. ¿Deseas agregar un campo "Más información" con enlace a documentación sobre cada tipo de prompt?
6. ¿Deberíamos mostrar también el icono de color (`color`) o solo usar el icono emoji?
7. ¿Deseas agregar animación al seleccionar un tipo (fade, scale, etc.)?
8. ¿Deseas que el selector tenga un valor por defecto (auto-selección según último uso) o siempre en 'basic'?

---

#### Tarea 8.5: Integrar Selector de Tipo en UI Principal

**Archivo:** `frontend/src/app/page.tsx`

**Objetivo:** Integrar el componente `PromptTypeSelector` en la página principal y pasar el tipo seleccionado al workflow.

**Preguntas Clave:**

1. ¿Deseas que el tipo por defecto sea 'basic' siempre, o debería recuperarse de localStorage/prefencia guardada?
2. ¿Deseas agregar un efecto para cargar el tipo preferido del usuario al iniciar la aplicación?
3. ¿Deberíamos guardar el tipo seleccionado en localStorage para recordarlo entre sesiones?
4. ¿Deseas mostrar el selector de tipo siempre (cuando status === 'idle') o solo cuando no hay un workflow activo?
5. ¿Deseas que el selector esté visible también cuando el usuario está en medio de un workflow (para cambiar tipo)?
6. ¿Deberíamos agregar un indicador visual de qué tipo se está usando actualmente en otras partes de la UI?
7. ¿Qué mensaje mostrar para los tipos no habilitados? ¿El genérico "próximamente" o algo más específico?
8. ¿Deseas que el `prompt_type` sea requerido o opcional (con default a 'basic')?
9. ¿Deberíamos validar que el `prompt_type` sea un valor válido antes de iniciar el workflow?
10. ¿Qué debería pasar si el usuario envía un `prompt_type` no habilitado? ¿Error 400 o usar el tipo 'basic' por defecto con un warning?
11. ¿Deseas que el tipo de prompt se pueda cambiar mientras un workflow está en progreso? ¿Bloquear o permitir?

---

#### Tarea 8.6-8.8: Habilitar Workflows Específicos

**Tarea 8.6: Habilitar System Prompts (Fase 8.6)**
- **Archivo:** `backend/app/agents/system_prompt_graph.py`
- **Objetivo:** Implementar workflow específico para System Prompts que requiere input de prueba del usuario.
- **Resumen:**
  - Crear grafo de workflow específico para system prompts
  - Reutilizar nodos existentes donde sea posible
  - Implementar lógica específica para system prompts
  - Adaptar templates de prompts para system prompts

**Tarea 8.7: Habilitar Image Prompts (Fase 8.7)**
- **Archivo:** `backend/app/agents/image_prompt_graph.py`
- **Objetivo:** Implementar workflow específico para Image Prompts enfocado en generar prompts para DALL-E, Midjourney, etc.
- **Resumen:**
  - Crear grafo de workflow específico para image prompts
  - Implementar templates específicos para image prompts
  - Posiblemente usar un modelo diferente (más económico para generar texto, no imágenes)
  - Adaptar Arena para mostrar prompts generados (no ejecutar, solo texto)

**Tarea 8.8: Habilitar Additional Prompts (Fase 8.8)**
- **Archivo:** `backend/app/agents/additional_prompt_graph.py`
- **Objetivo:** Implementar workflow específico para Additional Prompts.
- **Resumen:**
  - Crear grafo de workflow específico para additional prompts
  - Implementar lógica específica para additional prompts
  - Posible reutilización del workflow básico con adaptaciones menores

**Preguntas Clave:**

1. ¿Deseas que describa los detalles de implementación de estas tareas en este documento (planificación) o en documentos separados (implementación específica)?
2. ¿Deseas que los system prompts usen el mismo modelo configurado o un modelo específico (ej: más rápido para pruebas)?
3. ¿Deseas que el workflow de system prompts tenga un nodo adicional para "refinar system prompt" diferente del refinador de prompts normales?
4. ¿Deseas que los image prompts realmente generen imágenes (usar API de imagen) o solo generar el texto del prompt?
5. ¿Deseas que incluyamos una opción para seleccionar el servicio de imagen objetivo (DALL-E, Midjourney, Stable Diffusion)?
6. ¿Deseas que el workflow de image prompts tenga una etapa de "prueba del prompt" diferente a la de system prompts?
7. ¿Deseas agregar un campo de "estilo de imagen" que el usuario pueda seleccionar (realista, artístico, cartoon, etc.)?
8. ¿Deseas que los additional prompts usen el workflow básico con solo adaptaciones menores o un workflow completamente diferente?
9. ¿Deseas agregar una opción para que el usuario defina qué hace que el prompt sea "adicional"?
10. ¿Deseas que los additional prompts puedan contener variables o placeholders para que el usuario los rellene?
11. ¿Deberíamos agregar una categoría de "plantillas" donde los additional prompts sean plantillas reutilizables?

---

### 📊 Summary de Fase 8

#### Archivos a Crear

**Backend:**
1. `backend/app/core/prompt_types.py` - Enumeración y configuraciones
2. `backend/app/agents/workflow_factory.py` - Factory Pattern para workflows
3. `backend/app/api/endpoints.py` (actualizar) - Endpoint de tipos de prompt
4. `backend/app/agents/system_prompt_graph.py` - Workflow para system prompts
5. `backend/app/agents/image_prompt_graph.py` - Workflow para image prompts
6. `backend/app/agents/additional_prompt_graph.py` - Workflow para additional prompts

**Frontend:**
1. `frontend/src/components/prompt-type-selector.tsx` - Selector visual de tipos
2. `frontend/src/app/page.tsx` (actualizar) - Integrar selector en UI principal

#### Tareas Totales: 8
1. [ ] 8.1: Crear enumeración de tipos de prompt
2. [ ] 8.2: Crear Factory Pattern para workflows
3. [ ] 8.3: Crear endpoint de tipos de prompt
4. [ ] 8.4: Crear UI de selector de tipo
5. [ ] 8.5: Integrar selector en UI principal
6. [ ] 8.6: Habilitar System Prompts (workflow específico)
7. [ ] 8.7: Habilitar Image Prompts (workflow específico)
8. [ ] 8.8: Habilitar Additional Prompts (workflow específico)

#### Preguntas Clave Totales: 34

---

### 🎯 Criterios de Éxito de Fase 8

Al completar esta fase, el sistema deberá:

1. ✅ Arquitectura modular implementada (fácil agregar nuevos tipos)
2. ✅ Factory Pattern funcionando (selección dinámica de workflows)
3. ✅ Selector de tipo de prompt visible en la UI
4. ✅ Tipo 'basic' habilitado y funcional (ya lo está)
5. ✅ Tipos 'system', 'image', 'additional' preparados para habilitarse
6. ✅ Workflows específicos definidos para cada tipo
7. ✅ Endpoints funcionando para listar tipos
8. ✅ Integración fluida con UI existente
9. ✅ Documentación de cómo agregar nuevos tipos

---

## 9. Fase 9: Validación de API Key de Test

### 🎯 Objetivos

Implementar un sistema de validación de API key exclusiva para pruebas que:
1. Solo el propietario (desarrollador) pueda usar la API key de test
2. La API key de test NO se guarde en la base de datos
3. La API key de test NO aparezca en la UI de usuarios normales
4. Validación temporal sin persistencia (solo para pruebas)
5. Seguridad para evitar uso no autorizado

### 🗺 Desglose de Tareas

#### Tarea 9.1: Crear Endpoint de Validación Especial

**Archivo:** `backend/app/api/endpoints.py`

**Objetivo:** Implementar endpoint `/api/settings/validate-test` que valide API key sin guardarla en base de datos.

**Diferencias con `/api/settings/validate`:**

| Aspecto | `/api/settings/validate` | `/api/settings/validate-test` |
|---------|-------------------------------|--------------------------------|
| **Guarda en BD** | ✅ Sí | ❌ NO |
| **Aparece en UI normal** | ✅ Sí | ❌ NO |
| **Uso** | Producción (usuarios finales) | Solo pruebas del propietario |
| **Persistencia** | Permanente | Temporal (sin guardar) |
| **Accesibilidad** | Pública (requiere autenticación) | Restringida (modo especial) |

**Preguntas Clave:**

1. ¿Deseas implementar rate limiting ahora (recomendado) o dejarlo para una fase posterior?
2. ¿Deberíamos usar 10 validaciones por hora o un número diferente?
3. ¿Deseas implementar el rate limiting con un decorador de Python o con middleware de FastAPI?
4. ¿Qué debería pasar si se excede el límite? ¿Error HTTP 429 o permitir con un warning?

---

#### Tarea 9.2: Modo de Test para Propietario

**Opción A: Variable de Entorno (RECOMENDADA)**

**Objetivo:** Permitir habilitar un "modo de test" mediante variable de entorno.

**Implementación en backend:**

```python
import os

@router.post("/settings/validate-test")
async def validate_test_key(request: ValidationRequest):
    # Verificar si estamos en modo de test
    test_mode = os.getenv("PROMPTFORGE_TEST_MODE", "false").lower() == "true"
    
    if not test_mode:
        raise HTTPException(
            status_code=403,
            detail="Test validation endpoint is only available in test mode. Set PROMPTFORGE_TEST_MODE=true to enable."
        )
    
    # ... lógica de validación
    pass
```

**Ventajas:**
- Simple de implementar
- Fácil de deshabilitar en producción
- No requiere cambios en el frontend

**Opción B: Parámetro de URL (Alternativa)**

**Opción C: Token de Validación de Un Solo Uso (MÁS SEGURO)**

**Preguntas Clave:**

1. ¿Deseas que el mensaje de error sea específico sobre que este endpoint es solo para desarrolladores o genérico?
2. ¿Deberíamos agregar una lista blanca de IPs que pueden usar el modo de test (solo tu IP, etc.)?
3. ¿Deseas que el modo de test también habilite otros endpoints de debugging o solo el de validación?
4. ¿Deseas implementar Opción A (variable de entorno), Opción B (parámetro de URL), Opción C (tokens), o una combinación?
5. ¿Si implementamos múltiples opciones, cuál debería tener prioridad (variable de entorno vs parámetro)?
6. ¿Deseas que la validación de la test_key en Opción B sea opcional o requerida?
7. ¿Deseas implementar Opción C (tokens) o prefieres Opción A o B?
8. ¿Deseas que los tokens expiren en 1 hora o prefieres un tiempo diferente?
9. ¿Deberíamos guardar un registro de tokens generados con qué IP los usó (para auditoría)?
10. ¿Deseas agregar un endpoint para revocar tokens manualmente?

---

#### Tarea 9.3: Implementación en Frontend - Modo de Test

**Preguntas Clave:**

1. ¿Deseas implementar Opción A (variable de entorno), Opción B (parámetro de URL), Opción C (tokens), o una combinación?
2. ¿Si implementamos múltiples opciones, ¿deseas que el frontend soporte cambiar entre ellas fácilmente?
3. ¿Deseas que el modo de test esté siempre visible en el frontend (para desarrollador) o solo con una variable especial?

---

#### Tarea 9.4: Testing y Validación

**Casos de Prueba:**

1. **Validación exitosa**
   - Enviar API key válida
   - Verificar que retorne status "success"
   - Verificar que NO se guarde en BD
   - Verificar logs de validación

2. **Validación fallida - API Key inválida**
   - Enviar API key inválida
   - Verificar que retorne error 401
   - Verificar mensaje de error claro
   - Verificar que NO se guarde en BD

3. **Validación fallida - Rate limit**
   - Enviar múltiples validaciones rápidamente (más del límite)
   - Verificar que retorne error 429
   - Verificar mensaje de rate limit
   - Esperar a que expire la ventana de tiempo
   - Verificar que permita nuevamente

4. **Validación fallida - Proveedor no soportado**
   - Enviar proveedor inválido
   - Verificar que retorne error 400
   - Verificar lista de proveedores soportados

5. **Validación con modo de test deshabilitado**
   - Llamar al endpoint sin variable de entorno activada
   - Verificar que retorne error 403
   - Verificar mensaje de error específico

**Preguntas Clave:**

1. ¿Deseas crear un script automatizado de pruebas (con pytest o unittest) o pruebas manuales?
2. ¿Qué criterios de éxito considerar para que esta fase esté completa?
3. ¿Deseas que incluyamos pruebas de integración que prueben el flujo completo (validación + uso en workflow)?
4. ¿Deseas agregar tests de carga para verificar que el endpoint responda correctamente bajo presión (múltiples peticiones simultáneas)?

---

### 📊 Summary de Fase 9

#### Archivos a Crear

**Backend:**
1. `backend/app/api/endpoints.py` (actualizar) - Endpoint `/api/settings/validate-test`
2. `backend/app/core/test_token_manager.py` - Gestión de tokens (si usa Opción C)

**Frontend (si aplica):**
1. `frontend/src/components/test-mode-panel.tsx` - Panel de modo de test (Opción B)
2. `frontend/src/components/test-token-manager.tsx` - Gestor de tokens (Opción C)

#### Tareas Totales: 4
1. [ ] 9.1: Crear endpoint de validación especial
2. [ ] 9.2: Implementar modo de test para propietario
3. [ ] 9.3: Implementación en frontend (si aplica)
4. [ ] 9.4: Testing y validación

#### Preguntas Clave Totales: 19

---

### 🎯 Criterios de Éxito de Fase 9

Al completar esta fase, el sistema deberá:

1. ✅ Endpoint de validación de test implementado (`/api/settings/validate-test`)
2. ✅ API key de test NO se guarda en base de datos
3. ✅ API key de test NO aparece en UI normal
4. ✅ Solo el propietario puede usar la API key de test
5. ✅ Validación real con el servicio (OpenAI, Anthropic, etc.)
6. ✅ Rate limiting implementado (opcional pero recomendado)
7. ✅ Logging de validaciones para auditoría
8. ✅ Modo de test fácil de habilitar/deshabilitar
9. ✅ Documentación clara para desarrollador/propietario
10. ✅ Testing completo de todas las funcionalidades

---

## 10. Prioridades y Estrategia de Implementación

### Prioridades de Fases

| Prioridad | Fase | Nombre | Motivo |
|-----------|------|--------|--------|
| 1 (CRÍTICA) | 6.5 | Gestión de API Keys | Bloquea otras funcionalidades, esencial para UX |
| 2 (ALTA) | 7.5 | Internacionalización | Afecta toda la aplicación, mejora accesibilidad |
| 3 (MEDIA) | 8 | Tipos de Prompt | Prepara para expansiones futuras, arquitectura modular |
| 4 (BAJA) | 9 | Validación API Key Test | Solo para desarrollador, no afecta usuarios finales |

### Estrategia de Sprints

#### Sprint 1: Gestión de API Keys (2-3 días)
- Objetivo: Implementar sistema completo de gestión de API keys
- Tareas:
  - Rediseñar modelo de base de datos
  - Crear script de migración
  - Implementar endpoints CRUD
  - Crear UI de settings
  - Integrar con UI existente
  - Testing completo

#### Sprint 2: Internacionalización (3-4 días)
- Objetivo: Implementar soporte completo para English/Spanish
- Tareas:
  - Crear templates bilingües
  - Actualizar estado del workflow
  - Integrar templates en nodos
  - Crear endpoint de idioma
  - Crear provider React Context
  - Crear archivos de traducción
  - Crear switcher de idioma
  - Migrar componentes existentes
  - Testing completo

#### Sprint 3: Tipos de Prompt Modulares (4-5 días)
- Objetivo: Implementar arquitectura modular para múltiples tipos de prompt
- Tareas:
  - Crear enumeración de tipos
  - Crear Factory Pattern
  - Crear endpoint de tipos
  - Crear UI de selector
  - Integrar en UI principal
  - Preparar workflows específicos (8.6, 8.7, 8.8)

#### Sprint 4: Validación API Key Test (1-2 días)
- Objetivo: Implementar sistema de validación para desarrollador
- Tareas:
  - Crear endpoint de validación especial
  - Implementar modo de test
  - Crear UI (si aplica)
  - Testing completo

#### Sprint 5: Integración y Testing (2-3 días)
- Objetivo: Integrar todas las funcionalidades y probar end-to-end
- Tareas:
  - Integración de todas las fases
  - Testing end-to-end
  - Corrección de bugs
  - Documentación actualizada

---

## 11. Resumen de Fases

### Resumen Ejecutivo

| Fase | Tareas | Archivos Backend | Archivos Frontend | Preguntas Clave | Estimado |
|------|--------|------------------|-------------------|-----------------|----------|
| 6 | 2 | 2 | 0 | 4 | 2-3 días |
| 6.5 | 6 | 3 | 5 | 20 | 2-3 días |
| 7.5 | 11 | 2 | 4 | 42 | 3-4 días |
| 8 | 8 | 6 | 2 | 34 | 4-5 días |
| 9 | 4 | 2 | 2 | 19 | 1-2 días |
| **Total** | **31** | **15** | **13** | **119** | **12-17 días** |

### Documentos de Detalle

Todos los detalles técnicos están disponibles en los siguientes documentos:

1. **`00_vision_global.md`** - Visión global y contexto del proyecto
2. **`06_5_fase_api_keys_manager.md`** - Detalle de Fase 6.5 (Gestión de API Keys)
3. **`07_5_fase_internacionalizacion.md`** - Detalle de Fase 7.5 (Internacionalización)
4. **`08_fase_tipos_prompt_modulares_ACTUALIZADA.md`** - Detalle de Fase 8 (Tipos de Prompt)
5. **`09_fase_validacion_test_api_key.md`** - Detalle de Fase 9 (Validación de API Key de Test)

Cada documento contiene:
- Objetivos claros de la fase
- Desglose detallado de tareas
- Pasos de implementación para cada tarea
- Preguntas clave para facilitar la ejecución
- Criterios de éxito

---

## ✅ Estado de Planificación

**ESTADO:** ✅ **COMPLETA**

Todos los requerimientos del usuario han sido incorporados en la planificación:
- ✅ Gestión de API Keys (múltiples proveedores)
- ✅ Internacionalización (i18n) con prompts bilingües
- ✅ Tipos de Prompt (Basic, System, Image, Additional) con arquitectura modular
- ✅ Validación de API Key de Test (exclusiva para propietario)
- ✅ Mejoras de UX (re-acceso a onboarding, validación de configuración)

**Documentos creados:** 1 documento maestro consolidado + 4 documentos de detalle
**Preguntas clave totales:** 119+ preguntas distribuidas en todas las tareas
**Arquitectura modular:** Preparada para expansiones futuras

---

## 🚀 Próximos Pasos

### Para el Usuario:

1. **Revisar los documentos de planificación**
   - Leer `PLANIFICACION_MAESTRA.md` (este documento)
   - Revisar los documentos de detalle de cada fase
   - Familiarizarse con la estructura del proyecto

2. **Responder las preguntas clave**
   - Las preguntas están diseñadas para facilitar la implementación
   - Tus respuestas guiarán las decisiones técnicas
   - Puedes responder por fases o en su totalidad

3. **Priorizar la implementación**
   - Recomendado: Empezar con Sprint 1 (Gestión de API Keys)
   - Es la funcionalidad más crítica y bloquea otras

4. **Comenzar la implementación**
   - Usar los documentos como guía paso a paso
   - Seguir el orden de tareas en cada fase
   - Consultar las preguntas clave cuando surjan dudas

### Para el Desarrollador:

1. **Comenzar con Sprint 1**
   - Implementar Fase 6.5: Gestión de API Keys
   - Seguir el documento de planificación detallado
   - Preguntar dudas a medida que avanzas

2. **Documentar decisiones**
   - Registrar respuestas a las preguntas clave
   - Actualizar la planificación si hay cambios

3. **Testing continuo**
   - Probar cada funcionalidad a medida que se implementa
   - No dejar el testing para el final

4. **Comunicación**
   - Mantener al usuario informado del progreso
   - Reportar bloqueos o problemas técnicos
   - Sugerir mejoras o optimizaciones

---

**Planificación Creada Por:** OpenCode Assistant  
**Fecha:** 16 de febrero de 2026  
**Versión:** 1.0 (CONSOLIDADA) - Todos los requerimientos integrados  
**Estado:** ✅ LISTA PARA IMPLEMENTACIÓN Y EJECUCIÓN

**Archivos Modificados/Creados:**
- ✅ `Planeacion_base/00_vision_global.md` - Actualizado con nuevas fases
- ✅ `Planeacion_base/PLANIFICACION_MAESTRA.md` - Documento maestro consolidado (NUEVO)