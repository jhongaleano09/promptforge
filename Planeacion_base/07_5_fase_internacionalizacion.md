# 07.5. Fase: Internacionalización (i18n)

**Estado:** 🆕 PLANIFICADA - Lista para Implementación  
**Prioridad:** 2 (ALTA - Afecta toda la aplicación)  
**Estimado:** 3-4 días

---

## 🎯 Objetivos

Implementar soporte completo para dos idiomas (English/Spanish) que afecte tanto la UI como los prompts del agente:
1. Switcher de idioma funcional en la UI
2. Toda la UI en ambos idiomas
3. Templates de prompts del agente en ambos idiomas
4. Workflows adaptados según idioma seleccionado
5. Preferencia de idioma guardada y persistente

---

## 🗺 Desglose de Tareas

### Tarea 7.5.1: Crear Templates de Prompts Bilingües

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

**❓ Preguntas Clave:**

1. ¿Deseas que los marcadores de formato sean idénticos en ambos idiomas (ej: `{user_input}` siempre, no `{input}` en inglés)? RTA/ si los marcadores se deben conservar, lo relevante es la interfaz de usuario.
2. ¿Deseas agregar notas o comentarios en los templates para explicar qué hace cada sección? RTA? si.
3. ¿Deberíamos mantener también los templates originales en `templates.py` o reemplazarlos completamente? RTA/ Mantenerlos seran la base que posteriores iteraciones se traduciran a otros idiomas.
4. ¿Deseas que los nombres de variables sean los mismos en ambos idiomas (ej: `persona_name` en vez de `nombre_persona`)? RTA/ si las variables debe ser las mismos no hay necesidad de ajustarlas.
5. ¿Deseas que la función `get_templates()` valide el idioma o retorne el default sin advertencias? RTA/ correcto.
6. ¿Hay alguna expresión idiomática o mática cultural que sea difícil de traducir literalmente? RTA/ por el momento realiza la traduccion directa, en pruebas y usos se realizaran las correcciones inlcuidas las de los prompts iniciales que aun debo trabajarlos de forma directa.

---

### Tarea 7.5.2: Actualizar Estado del Workflow para Incluir Idioma

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

**❓ Preguntas Clave:**

1. ¿Deseas que `language` sea requerido o opcional (con default)? RTA/ definelo
2. ¿Deberíamos agregar validación para asegurar que solo se use "spanish" o "english"? RTA/ Correcto.
3. ¿Deseas agregar también un campo `ui_language` separado de `interaction_language`? RTA/ Si van a ser el mismo valor no seria necesario.
4. ¿Deberíamos mantener el nombre en inglés (`language`) o usar `idioma` en español? RTA/ usar idioma cuando este en español y en ingles usar language.
 
---

### Tarea 7.5.3: Integrar Templates i18n en Nodos del Workflow

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

**❓ Preguntas Clave:**

1. ¿Deseas que mantengamos ambos imports (templates.py y i18n_templates.py) por compatibilidad o solo usar i18n? RTA/ si mantener.
2. ¿Deseas que la lógica de selección de idioma se centralice en una función auxiliar que usen todos los nodos? RTA/ no comprendi la pregunta, realiza una sugerencia sobre este punto.
3. ¿Qué debería pasar si el estado no tiene el campo `language`? ¿Usar default o lanzar error? RTA/ usar default.
4. ¿Deseas agregar logging para rastrear qué idioma se está usando en cada ejecución? RTA/ no es necesario realizar logging, sin embargo, si sera necesario tener un espacio para el usuario. (nombre, pais, etc)
5. ¿Deberíamos validar que el template seleccionado exista antes de usarlo (defensivo)? RTA/ Si, pero solo para los test, a nivel general no deberiamos validar ya que siempre deben estar disponibles.

---

### Tarea 7.5.4: Crear Endpoint de Configuración de Idioma

**Archivo:** `backend/app/api/endpoints.py`

**Objetivo:** Implementar endpoints para guardar y obtener la preferencia de idioma del usuario.

**Pasos de Implementación:**

#### 4.1: GET `/api/settings/language` - Obtener Idioma Actual

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

**❓ Preguntas Clave:**

1. ¿Deseas almacenar la preferencia de idioma en la tabla `api_keys` o crear una tabla `user_preferences`? RTA/ crear nueva tabla 'user_perfil_preferences'
2. ¿Deseas que la respuesta incluya también los metadatos del idioma (nombre, código, dirección del texto)? RTA/ no, la respuesta debe ser pensada en funcion del usuario. no requiere esa parte.
3. ¿Deberíamos incluir en la respuesta también la fecha de la última vez que se cambió el idioma? RTA/ no, enfocarnos en que realicamos refinamiento de prompts.

#### 4.2: POST `/api/settings/language` - Guardar Preferencia de Idioma

**Objetivo:** Guardar la preferencia de idioma del usuario en la base de datos.

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

**❓ Preguntas Clave:**

1. ¿Prefieres almacenar la preferencia de idioma en la tabla `api_keys` (Opción A) o crear una tabla `user_settings` (Opción B)? RTA/ en la tabla nueva creada, se menciono antes.
2. ¿Deseas que al guardar el idioma, se actualice también el estado de cualquier workflow activo en memoria? RTA/ si actualizarlos 
3. ¿Deberíamos enviar un evento o notificación cuando se cambia el idioma? RTA/ no es necesario.
4. ¿Deseas agregar un campo `last_changed_at` para rastrear cuándo se modificó el idioma? RTA/ no es relevante.
5. ¿Deseas que el endpoint valide si el usuario tiene permisos para cambiar configuraciones? RTA/ no es relevante.

---

### Tarea 7.5.5: Crear Provider de Idiomas (React Context)

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

**❓ Preguntas Clave:**

1. ¿Deseas que el idioma se guarde automáticamente en localStorage, solo backend, o ambos? RTA/ en la tabla del usuario comentado antes.
2. ¿Deseas agregar un indicador de "cargando traducciones..." mientras se carga el archivo JSON? RTA/ No deberia tomar tanto tiempo, si toma mas de 1 segundo, si.
3. ¿Deberíamos usar una biblioteca como `i18next` o implementar el sistema nosotros? RTA/ la que sea mas sencilla y cumpla.
4. ¿Deseas que el contexto también exponga las listas de idiomas disponibles y sus metadatos? RTA/ considero que si.
5. ¿Cómo manejar el caso donde el archivo de traducción no tenga una key (fallback al key original)? RTA/ el traductor sabra, por ello se crearan plantillas base, esto se valida manualmente.

---

### Tarea 7.5.6: Crear Archivos de Traducción (JSON)

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

**❓ Preguntas Clave:**

1. ¿Deseas usar snake_case para las keys (`welcome_title`) o camelCase (`welcomeTitle`)? RTA/ no se enque consiste, comenta y aplica la mejor opcion.
2. ¿Deseas que las keys sigan una convención de prefijos por funcionalidad (ej: `onboarding.title`)? no tengo presente en que consista.
3. ¿Deseas agregar metadatos de contexto (ej: `context: "onboarding"`) para ayudarte a organizar?
4. ¿Cómo manejar textos que son iguales en ambos idiomas (ej: "OpenAI", "GPT-4")? ¿Duplicar o centralizar? Son nombres propios, se deben mantener. (centralizar)
5. ¿Deseas agregar un campo `__metadata` en cada archivo JSON con información sobre la traducción (autor, fecha)? RTA/ no lo veo relevante.

---

### Tarea 7.5.7: Crear Componente Switcher de Idioma

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

**Variantes de diseño a considerar:**

**Variante A: Dropdown (select)**
- ✅ Simple de implementar
- ✅ Nativo del navegador
- ❌ Menos personalizable

**Variante B: Botones de Toggle**
- ✅ Más visualmente atractivo
- ✅ Acceso rápido
- ❌ No escala bien con muchos idiomas

**Variante C: Menú desplegable**
- ✅ Muy personalizable
- ✅ Puede incluir más información
- ❌ Más complejo de implementar

**❓ Preguntas Clave:**

1. ¿Deseas que el switcher use un dropdown (select) como en el ejemplo, o prefieres botones de toggle (dos botones)? RTA/ usar un swicher.
2. ¿Deseas incluir el nombre del idioma en texto además del emoji de bandera? RTA/ si.    agregarlos.
3. ¿Deseas agregar un indicador visual de qué idioma está activo (subrayado, background, etc.)? con el swhicher mas negrilla para resaltar el seleccioando actualemnte.
4. ¿Deseas que el switcher tenga un tooltip explicando qué hace (para usuarios nuevos)? RTA/ No.
5. ¿Deseas agregar un shortcut de teclado para cambiar idioma (ej: Ctrl+L)? RTA/ No, ir a configuracion y hacerlo manualmente.

---

### Tarea 7.5.8: Integrar LanguageContext en Layout Principal

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

**Ejemplo de código:**
```typescript
import { LanguageProvider } from '@/contexts/LanguageContext';

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <LanguageProvider>
      <html lang="en" suppressHydrationWarning>
        <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
          {/* ... contenido existente */}
          <ThemeProvider>
            {/* ... */}
          </ThemeProvider>
        </body>
      </html>
    </LanguageProvider>
  );
}
```

**Consideraciones:**
- El atributo `lang` debería ser dinámico
- Puede venir del estado del `LanguageProvider`
- O leer directamente del localStorage

**❓ Preguntas Clave:**

1. ¿Deseas que el atributo `lang` del HTML se actualice automáticamente cuando cambia el idioma o solo al recargar la página? RTA/ si,
2. ¿Deberíamos cambiar también la dirección del texto del HTML (`dir="ltr"` o `dir="rtl"`) según el idioma? RTA/ Evalua y toma la mejor opcion en terminos de miplementacion. 
3. ¿Deseas agregar también metadatos de SEO (`<title>`, `<meta>`) que cambien según el idioma? RTA/ no
4. ¿Deseas que el `LanguageProvider` esté dentro o fuera del `ThemeProvider`? ¿Qué orden es mejor? RTA/ evalua y toma la decision.

---

### Tarea 7.5.9: Migrar Componentes Existentes para Usar Traducciones

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

**Ejemplos de migración:**

**Antes:**
```typescript
<h1>Welcome to PromptForge</h1>
<p>Configure your LLM provider</p>
<button>Validate & Save</button>
```

**Después:**
```typescript
const { t } = useLanguage();

<h1>{t('welcome_title')}</h1>
<p>{t('configure_provider')}</p>
<button>{t('validate_save')}</button>
```

**❓ Preguntas Clave:**

1. ¿Deseas que hagamos la migración componente por componente (más lento pero más controlado) o en un solo cambio masivo? RTA/ En un solo cambio masivo.
2. ¿Cómo manejar textos dinámicos que incluyen variables (ej: "Hola, {nombre}")? ¿Interpolación o pasar parámetros a `t()`?
3. ¿Deseas que agreguemos un script o herramienta que escanee todos los archivos buscando textos en inglés/español para no olvidar ninguno?
4. ¿Deberíamos agregar una función `t()` que acepte parámetros para interpolación (ej: `t('welcome', {name: 'Juan'})`)?
5. ¿Qué hacer con textos que son idénticos en ambos idiomas (ej: "OpenAI", "GPT-4")? ¿Traducir de todas formas o centralizar?

---

### Tarea 7.5.10: Integrar LanguageSwitcher en el Header

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

**Ejemplo de estructura del header:**
```typescript
<header className="w-full max-w-7xl mb-8 flex justify-between items-center border-b pb-4">
  <div className="flex items-center gap-2">
    {/* Logo existente */}
  </div>

  <div className="flex items-center gap-4">
    <LanguageSwitcher />
    
    {mounted && (
      <button
        onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        title={t('toggle_theme')}
      >
        {theme === "dark" ? <Sun /> : <Moon />}
      </button>
    )}
  </div>
</header>
```

**Consideraciones de diseño:**

**Móvil:**
- El switcher de idioma debe ser fácil de tocar
- Considerar usar iconos más grandes en pantallas pequeñas
- No debe obstaculizar otros elementos del header

**Desktop:**
- El switcher puede ser más compacto
- Espacio disponible en el header
- Posición clara y visible

**Accesibilidad:**
- Soporte para navegación por teclado
- Labels apropiados para screen readers
- Contraste de colores suficiente

**❓ Preguntas Clave:**

1. ¿Deseas que el LanguageSwitcher esté a la izquierda (cerca del logo) o a la derecha (cerca del botón de tema)?
2. ¿Deseas agregar también un indicador en el footer (adicionalmente al header)?
3. ¿Deberíamos mostrar el idioma actual como texto además del switcher (ej: "Idioma: 🇪🇸")?
4. ¿Deseas que el switcher se colapse en una vista más compacta cuando hay poco espacio horizontal?
5. ¿Deberíamos agregar un atajo de teclado para abrir el switcher rápidamente?

---

### Tarea 7.5.11: Testing y Validación de i18n

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

**❓ Preguntas Clave:**

1. ¿Deseas que creemos un checklist manual de pruebas o un script automatizado?
2. ¿Qué criterios de éxito considerar para cada caso de prueba?
3. ¿Deseas incluir screenshots en el checklist para documentación visual?
4. ¿Cómo manejar los casos edge mencionados? ¿Cancelar ejecución, bloquear cambio, o permitir?
5. ¿Deseas que creemos un reporte de pruebas con bugs encontrados y su severidad?

---

## 📊 Summary de Fase 7.5

### Archivos a Crear

**Backend:**
1. `backend/app/prompts/i18n_templates.py` - Templates bilingües
2. `backend/app/api/endpoints.py` (actualizar) - Endpoint de idioma

**Frontend:**
1. `frontend/src/contexts/LanguageContext.tsx` - Context de idioma
2. `frontend/public/i18n/spanish.json` - Traducciones ES
3. `frontend/public/i18n/english.json` - Traducciones EN
4. `frontend/src/components/language-switcher.tsx` - Switcher UI

**Archivos a Modificar:**
1. `backend/app/agents/state.py` - Agregar campo `language`
2. `backend/app/agents/nodes.py` - Usar templates dinámicos
3. `frontend/src/app/layout.tsx` - Envolver con `LanguageProvider`
4. Múltiples componentes - Reemplazar textos fijos por `t()`

### Tareas Totales: 11
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

### Preguntas Clave Totales: 42
Distribuidas en cada tarea para facilitar la implementación.

---

## 🎯 Criterios de Éxito de Fase 7.5

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

**Fase 7.5 - Planificación Creada Por:** OpenCode Assistant  
**Fecha:** 16 de febrero de 2026  
**Versión:** 1.0 - Lista para Implementación
