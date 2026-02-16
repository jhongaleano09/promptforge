# 08. Fase: Tipos de Prompt Modulares (ACTUALIZADA)

**Estado:** 🆕 PLANIFICADA - Lista para Implementación  
**Prioridad:** 3 (MEDIA - Prepara para expansiones futuras)  
**Estimado:** 4-5 días

---

## 🎯 Objetivos

Implementar una arquitectura modular que soporte múltiples tipos de prompt con workflows específicos para cada uno:
1. **Basic** (ya funcional - ✅) - Prompt estándar para tareas generales
2. **System Prompt** (requiere input de prueba) - Para configurar comportamiento del modelo
3. **Image Prompt** - Para generación de imágenes (DALL-E, Midjourney, etc.)
4. **Additional Prompt** - Prompts complementarios o adicionales
5. Arquitectura escalable para habilitar nuevos tipos en el futuro
6. Workflows específicos para cada tipo de prompt
7. Factory Pattern para seleccionar el workflow correcto
8. UI intuitiva para seleccionar tipo de prompt

---

## 🗺 Desglose de Tareas

### Tarea 8.1: Crear Enumeración de Tipos de Prompt

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

**Pasos de Implementación:**

1. **Crear archivo `prompt_types.py`**
   - Ubicación: `backend/app/core/`
   - Importar `Enum` y `typing`

2. **Definir enumeración `PromptType`**
   - Crear valores para: `BASIC`, `SYSTEM`, `IMAGE`, `ADDITIONAL`
   - Documentar cada valor con docstrings

3. **Definir configuración de cada tipo**
   - Crear dict `PROMPT_TYPE_CONFIGS` con todos los metadatos
   - Campos por tipo: `name`, `description`, `requires_test_input`, `workflow_graph`, `enabled`, `icon`, `color`, `category`

4. **Implementar función `get_prompt_type_config()`**
   - Recibir `prompt_type` como parámetro
   - Retornar config específica
   - Validar que el tipo exista
   - Lanzar error si no existe

5. **Implementar función `get_enabled_prompt_types()`**
   - Filtrar tipos con `enabled == True`
   - Retornar lista de IDs
   - Usar en endpoints para listar tipos disponibles

6. **Implementar función `get_all_prompt_types()`**
   - Retornar información completa de todos los tipos
   - Usar para mostrar en UI con todos los detalles

7. **Implementar función `is_prompt_type_enabled()`**
   - Verificar si un tipo específico está habilitado
   - Usar para validaciones en backend

8. **Considerar extension futura**
   - ¿Deberíamos agregar un campo `version` para soportar múltiples versiones de un tipo?
   - ¿Deberíamos agregar `tags` para categorizar tipos?

**❓ Preguntas Clave:**

1. ¿Deseas mantener los valores de la enumeración en inglés (`BASIC`, `SYSTEM`) o usar español (`BASICO`, `SISTEMA`)?
2. ¿Deberíamos agregar más metadatos como `difficulty_level`, `estimated_tokens`, `examples`?
3. ¿Los `workflow_graph` deberían ser nombres de funciones o rutas de archivos?
4. ¿Deberíamos agregar validación en `get_prompt_type_config()` para verificar que el tipo sea uno de los valores del enum?
5. ¿Deseas que la función `get_enabled_prompt_types()` retorne solo los IDs o también las configuraciones completas?
6. ¿Deberíamos agregar un tipo `CUSTOM` para permitir workflows personalizados por el usuario?
7. ¿Los iconos y colores (`📝`, `blue`) deberían ser configurables o fijos?
8. ¿Deberíamos agregar un campo `display_order` para controlar el orden en que aparecen los tipos en la UI?

---

### Tarea 8.2: Crear Factory Pattern para Workflows

**Archivo:** `backend/app/agents/workflow_factory.py`

**Objetivo:** Implementar Factory Pattern para retornar el workflow (grafo) apropiado según el tipo de prompt seleccionado.

**Estado Actual:**
- Solo existe un workflow básico en `graph.py`
- No hay sistema para seleccionar workflows diferentes
- El workflow está hardcoded en `get_graph()`

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

**Pasos de Implementación:**

1. **Crear archivo `workflow_factory.py`**
   - Ubicación: `backend/app/agents/`
   - Importar `PromptType` y funciones auxiliares

2. **Implementar función principal `get_workflow_graph()`**
   - Recibir `prompt_type` y `checkpointer`
   - Retornar workflow compilado
   - Implementar validaciones y manejo de errores

3. **Implementar lógica de factory**
   - Usar sentencias if/elif/else para seleccionar workflow
   - Importar dinámicamente workflows cuando se implementen
   - Manejar caso de workflow no implementado con error claro

4. **Agregar validación de tipos habilitados**
   - Verificar `config.get("enabled")`
   - Lanzar error si el tipo no está habilitado
   - Listar tipos disponibles en el mensaje de error

5. **Implementar fallback a workflow básico**
   - Si el workflow solicitado no existe o no está implementado
   - Usar workflow básico por seguridad
   - Evitar que el sistema falle completamente

6. **Implementar función `get_available_workflows()`**
   - Retornar información de workflows disponibles
   - Incluir indicador de `implemented`
   - Usar para debugging y documentación

7. **Considerar errores de importación dinámica**
   - Los imports dinámicos (`from app.agents...`) pueden fallar
   - Manejar con try/except
   - Dar mensajes de error específicos

8. **Preparar para extensión futura**
   - El factory facilita agregar nuevos tipos sin modificar esta función
   - Solo agregar nuevo workflow y actualizar `PROMPT_TYPE_CONFIGS`

**❓ Preguntas Clave:**

1. ¿Deseas que el manejo de errores de importación dinámica sea con try/except o usar una estructura de registro de workflows?
2. ¿Deberíamos agregar un parámetro opcional `fallback_to_basic=True` para decidir qué hacer si el workflow no está implementado?
3. ¿El `checkpointer` debería ser opcional o requerido en todos los workflows?
4. ¿Deseas que el factory valide también que el `checkpointer` sea del tipo correcto antes de usarlo?
5. ¿Deberíamos agregar logging al factory para rastrear qué workflow se está seleccionando?
6. ¿Deseas implementar un caché de workflows para no recrearlos en cada llamada?
7. ¿Qué hacer si múltiples workflows solicitan el mismo checkpointer? ¿Compartir o crear instancias separadas?
8. ¿Deberíamos agregar un método `get_workflow_graph_sync()` para workflows síncronos (si los hubiera)?

---

### Tarea 8.3: Crear Endpoint de Tipos de Prompt

**Archivo:** `backend/app/api/endpoints.py`

**Objetivo:** Implementar endpoints para listar tipos de prompt disponibles y su estado de habilitación.

**Pasos de Implementación:**

#### 8.3.1: GET `/api/prompts/types` - Listar Tipos Disponibles

**Objetivo:** Retornar lista de todos los tipos de prompt con su configuración y estado.

**Implementación:**
- Importar funciones desde `prompt_types.py`
- Llamar a `get_all_prompt_types()` o `get_enabled_prompt_types()`
- Retornar en formato JSON
- Incluir información completa para el frontend

**Request esperado:**
```http
GET /api/prompts/types
```

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

**Consideraciones:**
- Ordenar tipos por `enabled` (habilitados primero)
- Incluir metadatos para UI (icono, color)
- Incluir campo `requires_test_input` para UI específica

#### 8.3.2: GET `/api/prompts/types/available` - Solo Tipos Habilitados

**Objetivo:** Retornar solo los tipos de prompt que están habilitados (ready to use).

**Request esperado:**
```http
GET /api/prompts/types/available
```

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

**Uso:** Este endpoint se usa para mostrar solo las opciones disponibles en el selector de tipo de prompt.

**❓ Preguntas Clave:**

1. ¿Deseas mantener ambos endpoints (`/types` y `/types/available`) o solo uno con parámetro para filtrar?
2. ¿Deseas agregar un parámetro de query para ordenar por (`?order=enabled`, `?order=name`)?
3. ¿Deberíamos incluir en la respuesta también información sobre la fecha de habilitación de cada tipo?
4. ¿Deseas agregar un endpoint `GET /api/prompts/types/{id}` para obtener detalles de un tipo específico?
5. ¿Deseas que el endpoint incluya información sobre qué modelos son recomendados para cada tipo de prompt?

---

### Tarea 8.4: Crear UI de Selector de Tipo de Prompt

**Archivo:** `frontend/src/components/prompt-type-selector.tsx`

**Objetivo:** Componente visual para que el usuario seleccione el tipo de prompt que desea usar.

**Pasos de Implementación:**

#### 8.4.1: Estructura del Componente

**Implementación:**
```typescript
'use client';

import { useState, useEffect } from 'react';
import { useLanguage } from '@/contexts/LanguageContext';
import { fetchEventSource } from '@microsoft/fetch-event-source';

type PromptType = 'basic' | 'system' | 'image' | 'additional';

interface PromptTypeOption {
  id: PromptType;
  name: string;
  description: string;
  enabled: boolean;
  requires_test_input: boolean;
  icon: string;
  color: string;
  category: string;
}

interface PromptTypeSelectorProps {
  selectedType: PromptType;
  onTypeChange: (type: PromptType) => void;
  disabled?: boolean;
}

export function PromptTypeSelector({ selectedType, onTypeChange, disabled = false }: PromptTypeSelectorProps) {
  const { t } = useLanguage();
  const [availableTypes, setAvailableTypes] = useState<PromptTypeOption[]>([]);
  const [loading, setLoading] = useState(true);

  // Cargar tipos de prompt al montar
  useEffect(() => {
    const fetchTypes = async () => {
      try {
        const res = await fetch(`${API_BASE}/prompts/types`);
        const data = await res.json();
        setAvailableTypes(data.types);
      } catch (error) {
        console.error('Error loading prompt types:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTypes();
  }, []);

  const handleTypeChange = (typeId: PromptType) => {
    // Validar que el tipo esté habilitado
    const selectedConfig = availableTypes.find(t => t.id === typeId);
    
    if (!selectedConfig?.enabled) {
      alert(t('type_not_enabled')); // O mostrar un toast/modal
      return;
    }
    
    onTypeChange(typeId);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-200"></div>
        <p className="ml-4">{t('loading_types')}</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <label className="text-sm font-medium">
        {t('prompt_type_label')}
      </label>
      
      <div className="grid grid-cols-2 gap-4">
        {availableTypes.map(type => (
          <button
            key={type.id}
            disabled={disabled || !type.enabled}
            onClick={() => handleTypeChange(type.id)}
            className={`
              p-4 border rounded-lg text-left transition-all
              ${selectedType === type.id 
                ? 'border-primary bg-primary/5 ring-2 ring-primary' 
                : 'border-border hover:border-primary/50'}
              ${!type.enabled ? 'opacity-50 cursor-not-allowed' : ''}
              ${disabled ? 'opacity-40 cursor-not-allowed' : ''}
            `}
          >
            <div className="flex items-start gap-3">
              {/* Icono */}
              <div className="text-2xl">{type.icon}</div>
              
              <div className="flex-1">
                <div className="font-semibold text-base">
                  {type.name}
                </div>
                <div className="text-sm text-muted-foreground mt-1">
                  {type.description}
                </div>
                
                {/* Badge de estado */}
                <div className="mt-2">
                  {type.enabled ? (
                    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      ✓ {t('enabled')}
                    </span>
                  ) : (
                    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                      🕐 {t('coming_soon')}
                    </span>
                  )}
                </div>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
```

**❓ Preguntas Clave:**

1. ¿Deseas que el grid sea de 2 columnas como en el ejemplo, o 3 columnas, o responsivo según tamaño de pantalla?
2. ¿Deberíamos agregar un tooltip o descripción emergente al hacer hover en el card de tipo?
3. ¿Deseas mostrar el badge de estado (enabled/coming_soon) como en el ejemplo, o usar estilos diferentes?
4. ¿Qué debería pasar cuando el usuario hace clic en un tipo no habilitado? ¿Mostrar un alert (como en el ejemplo) o un modal más elegante?
5. ¿Deseas agregar un campo "Más información" con enlace a documentación sobre cada tipo de prompt?
6. ¿Deberíamos mostrar también el icono de color (`color`) o solo usar el icono emoji?
7. ¿Deseas agregar animación al seleccionar un tipo (fade, scale, etc.)?
8. ¿Deseas que el selector tenga un valor por defecto (auto-selección según último uso) o siempre en 'basic'?

---

### Tarea 8.5: Integrar Selector de Tipo en UI Principal

**Archivo:** `frontend/src/app/page.tsx`

**Objetivo:** Integrar el componente `PromptTypeSelector` en la página principal y pasar el tipo seleccionado al workflow.

**Pasos de Implementación:**

#### 8.5.1: Agregar Estado de Tipo de Prompt

**Implementación:**
```typescript
// En el componente Home
const [promptType, setPromptType] = useState<PromptType>('basic'); // Default
```

**❓ Preguntas Clave:**

1. ¿Deseas que el tipo por defecto sea 'basic' siempre, o debería recuperarse de localStorage/prefencia guardada?
2. ¿Deseas agregar un efecto para cargar el tipo preferido del usuario al iniciar la aplicación?
3. ¿Deberíamos guardar el tipo seleccionado en localStorage para recordarlo entre sesiones?

#### 8.5.2: Renderizar PromptTypeSelector

**Implementación:**
```typescript
// En el JSX de Home
{status === 'idle' && (
  <div className="space-y-6">
    <PromptTypeSelector 
      selectedType={promptType}
      onTypeChange={setPromptType}
    />
    
    {promptType === 'basic' && (
      <InitialPromptInput 
        onSubmit={startWorkflow}
        promptType={promptType}  // Pasar tipo al workflow
      />
    )}
    
    {/* Para otros tipos, mostrar mensajes de "próximamente" */}
    {promptType !== 'basic' && (
      <div className="text-center p-8 border rounded-lg">
        <div className="text-4xl mb-4">🕐</div>
        <h2 className="text-xl font-semibold mb-2">
          {t('coming_soon')}
        </h2>
        <p className="text-muted-foreground">
          {t(`${promptType}_coming_soon_description`)}
        </p>
      </div>
    )}
  </div>
)}
```

**❓ Preguntas Clave:**

1. ¿Deseas mostrar el selector de tipo siempre (cuando status === 'idle') o solo cuando no hay un workflow activo?
2. ¿Deseas que el selector esté visible también cuando el usuario está en medio de un workflow (para cambiar tipo)?
3. ¿Deberíamos agregar un indicador visual de qué tipo se está usando actualmente en otras partes de la UI?
4. ¿Qué mensaje mostrar para los tipos no habilitados? ¿El genérico "próximamente" o algo más específico?

#### 8.5.3: Pasar Tipo de Prompt al Workflow

**Objetivo:** Asegurar que el workflow seleccione y use el workflow correcto según el tipo de prompt.

**Implementación en backend:**
- Actualizar endpoint `/api/workflow/stream/start` para recibir `prompt_type`
- Pasar `prompt_type` al estado inicial del workflow
- Usar `get_workflow_graph(prompt_type, checkpointer)` en lugar de `get_graph()`

**Implementación en frontend:**
- Al hacer clic en "Start Forging", enviar `prompt_type` en el payload
- Actualizar el store de workflow con el tipo seleccionado

**Request esperado:**
```json
{
  "user_input": "Describe your task...",
  "prompt_type": "basic",  // Nuevo campo
  "language": "spanish"  // Opcional, desde el contexto
}
```

**❓ Preguntas Clave:**

1. ¿Deseas que el `prompt_type` sea requerido o opcional (con default a 'basic')?
2. ¿Deberíamos validar que el `prompt_type` sea un valor válido antes de iniciar el workflow?
3. ¿Qué debería pasar si el usuario envía un `prompt_type` no habilitado? ¿Error 400 o usar el tipo 'basic' por defecto con un warning?
4. ¿Deseas que el tipo de prompt se pueda cambiar mientras un workflow está en progreso? ¿Bloquear o permitir?

---

### Tarea 8.6: Habilitar System Prompts (Fase 8.6)

**Archivo:** `backend/app/agents/system_prompt_graph.py`

**Objetivo:** Implementar workflow específico para System Prompts que requiere input de prueba del usuario.

**Estado:** Esta tarea se describirá en DETALLE cuando se implemente en la Fase 8.6.

**Resumen:**
- Crear grafo de workflow específico para system prompts
- Reutilizar nodos existentes donde sea posible
- Implementar lógica específica para system prompts
- Adaptar templates de prompts para system prompts

**❓ Preguntas Clave:**

1. ¿Deseas que describa los detalles de implementación de esta tarea en este documento (planificación) o en un documento separado (implementación específica)?
2. ¿Deseas que los system prompts usen el mismo modelo configurado o un modelo específico (ej: más rápido para pruebas)?
3. ¿Deseas que el workflow de system prompts tenga un nodo adicional para "refinar system prompt" diferente del refinador de prompts normales?

---

### Tarea 8.7: Habilitar Image Prompts (Fase 8.7)

**Archivo:** `backend/app/agents/image_prompt_graph.py`

**Objetivo:** Implementar workflow específico para Image Prompts enfocado en generar prompts para DALL-E, Midjourney, etc.

**Estado:** Esta tarea se describirá en DETALLE cuando se implemente en la Fase 8.7.

**Resumen:**
- Crear grafo de workflow específico para image prompts
- Implementar templates específicos para image prompts
- Posiblemente usar un modelo diferente (más económico para generar texto, no imágenes)
- Adaptar Arena para mostrar prompts generados (no ejecutar, solo texto)

**❓ Preguntas Clave:**

1. ¿Deseas que los image prompts realmente generen imágenes (usar API de imagen) o solo generen el texto del prompt?
2. ¿Deseas que incluyamos una opción para seleccionar el servicio de imagen objetivo (DALL-E, Midjourney, Stable Diffusion)?
3. ¿Deseas que el workflow de image prompts tenga una etapa de "prueba del prompt" diferente a la de system prompts?
4. ¿Deseas agregar un campo de "estilo de imagen" que el usuario pueda seleccionar (realista, artístico, cartoon, etc.)?

---

### Tarea 8.8: Habilitar Additional Prompts (Fase 8.8)

**Archivo:** `backend/app/agents/additional_prompt_graph.py`

**Objetivo:** Implementar workflow específico para Additional Prompts.

**Estado:** Esta tarea se describirá en DETALLE cuando se implemente en la Fase 8.8.

**Resumen:**
- Crear grafo de workflow específico para additional prompts
- Implementar lógica específica para additional prompts
- Posible reutilización del workflow básico con adaptaciones menores

**❓ Preguntas Clave:**

1. ¿Deseas que los additional prompts usen el workflow básico con solo adaptaciones menores o un workflow completamente diferente?
2. ¿Deseas agregar una opción para que el usuario defina qué hace que el prompt sea "adicional"?
3. ¿Deseas que los additional prompts puedan contener variables o placeholders para que el usuario los rellene?
4. ¿Deseas agregar una categoría de "plantillas" donde los additional prompts sean plantillas reutilizables?

---

## 📊 Summary de Fase 8

### Archivos a Crear

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

### Tareas Totales: 8
1. [ ] 8.1: Crear enumeración de tipos de prompt
2. [ ] 8.2: Crear Factory Pattern para workflows
3. [ ] 8.3: Crear endpoint de tipos de prompt
4. [ ] 8.4: Crear UI de selector de tipo
5. [ ] 8.5: Integrar selector en UI principal
6. [ ] 8.6: Habilitar System Prompts (workflow específico)
7. [ ] 8.7: Habilitar Image Prompts (workflow específico)
8. [ ] 8.8: Habilitar Additional Prompts (workflow específico)

### Preguntas Clave Totales: 34
Distribuidas en cada tarea para facilitar la implementación.

---

## 🎯 Criterios de Éxito de Fase 8

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

**Fase 8 - Planificación Creada Por:** OpenCode Assistant  
**Fecha:** 16 de febrero de 2026  
**Versión:** 2.0 - Actualizada con tipos de prompt modulares  
**Estado:** ✅ LISTA PARA IMPLEMENTACIÓN
