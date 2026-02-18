# 📅 Plan de Desarrollo y Bitácora - PromptForge (ACTUALIZADO)

**Fecha de Validación:** 16 de Febrero de 2026  
**Estado:** Planificación Completa con Nuevos Requerimientos Integrados  
**Versión del Documento:** 2.0 (ACTUALIZADA)  

---

## 🔍 Diagnóstico del Estado Actual (16/02/2026 - Actualizado)

El sistema se encuentra en un estado de **MVP Avanzado**. Se han identificado y planificado nuevas funcionalidades críticas para mejorar la usabilidad.

### A. Backend (Python/FastAPI)
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

### B. Frontend (Next.js 16)
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

### C. Infraestructura y Despliegue
- **Estado:** ⚠️ Funcional pero requiere mejoras
- **Situación:** Backend en puerto 8001, Frontend en puerto 3000 (o 3000 según config)
- **Documentación:** README.md existe pero necesita actualización con nuevas funcionalidades

---

## 🎯 Objetivos del Ciclo Actual

El objetivo principal es **profesionalizar y expandir el repositorio** incorporando nuevos requerimientos críticos del usuario:

1. ✅ **Gestión de API Keys** - Múltiples proveedores, eliminar, reconfigurar
2. ✅ **Internacionalización (i18n)** - Switcher de idioma (English/Spanish), prompts bilingües
3. ✅ **Tipos de Prompt** - Basic (ya funcional), System Prompt, Image, Additional con workflows modulares
4. ✅ **Validación de API Key de Test** - Solo para propietario, no persistente
5. ✅ **Mejoras de UX** - Re-acceso a onboarding desde settings, validación de API keys activas

### Estrategia de Desarrollo

Implementación incremental priorizando funcionalidades críticas:

1. **Sprint 1 (2-3 días):** Gestión de API Keys (FASE 6.5) - PRIORIDAD 1 CRÍTICA
2. **Sprint 2 (3-4 días):** Internacionalización i18n (FASE 7.5) - PRIORIDAD 2 ALTA
3. **Sprint 3 (4-5 días):** Tipos de Prompt Modulares (FASE 8) - PRIORIDAD 3 MEDIA
4. **Sprint 4 (1-2 días):** Validación de API Key de Test (FASE 9) - PRIORIDAD 4 BAJA
5. **Sprint 5 (2-3 días):** Integración y Testing

---

## 📝 Hoja de Ruta (Roadmap) - Q1 2026 (ACTUALIZADA)

### Fase 1-5: Completadas
- [x] **Planificación:** Creación de documentos maestros
- [x] **Conexión API:** Fix de puerto (frontend: 3000 → backend: 8001)
- [x] **Variables de entorno:** Implementación de `.env.local` con `NEXT_PUBLIC_API_URL`
- [x] **Validación API Key:** Backend corrigido para validar correctamente
- [x] **Testing:** API Key de usuario validada exitosamente

### Fase 6: Consolidación y Documentación
- [x] **Planificación:** Documentos creados
- [ ] **Dockerización:** Crear Dockerfiles y docker-compose.yml
- [ ] **Documentación Maestra (`README.md`):** Actualizar con nuevas funcionalidades
  - Sección de API Keys (múltiples)
  - Sección de i18n (cambiar idioma)
  - Sección de tipos de prompt
  - Guías actualizadas

### Fase 6.5: Gestión de API Keys (NUEVA - PRIORIDAD 1)
**Archivo:** `Planeacion_base/06_5_fase_api_keys_manager.md`

- [ ] 6.5.1: Rediseñar modelo de base de datos
  - Crear tabla `api_keys` con soporte para múltiples proveedores
  - Implementar campos: `provider`, `api_key_encrypted`, `model_preference`, `is_active`, timestamps
  - Constraint único: solo una key activa por proveedor

- [ ] 6.5.2: Crear script de migración de datos
  - Migrar datos de `settings` a `api_keys`
  - Manejar datos existentes correctamente
  - Verificar integridad de migración

- [ ] 6.5.3: Crear endpoints CRUD para API keys
  - GET `/api/settings/keys` - Listar keys
  - POST `/api/settings/keys` - Agregar nueva key
  - DELETE `/api/settings/keys/{id}` - Eliminar key
  - PUT `/api/settings/keys/{id}/activate` - Activar key
  - GET `/api/settings/validate-active` - Validar configuración

- [ ] 6.5.4: Crear UI de Settings
  - Componente `api-keys-manager.tsx` - Lista visual de keys
  - Componente `settings-page.tsx` - Página completa de settings
  - Modal de agregar nueva key
  - Modal de confirmación de eliminación
  - Validación que no sea la última key activa

- [ ] 6.5.5: Integrar con UI existente
  - Agregar botón de acceso a settings en header
  - Verificar configuración al iniciar (mostrar onboarding si no hay key)
  - Actualizar workflowStore con validación de configuración

- [ ] 6.5.6: Testing y validación
  - Probar agregar/eliminar/activar keys
  - Probar validación de configuración al inicio
  - Testing end-to-end de funcionalidad completa

### Fase 7: UX: Refinamiento via Streaming
- [ ] **Backend: Endpoint de Refinamiento Streaming**
  - Crear `POST /api/workflow/stream/{thread_id}/refine`
  - Implementar SSE para refinamiento
  - Emitir eventos compatibles con frontend

- [ ] **Frontend: Store Update (Zustand)**
  - Actualizar función `refineVariant` para usar `fetchEventSource`
  - Manejar eventos de streaming (`token`, `status`, `update`)
  - Mostrar progreso en tiempo real

- [ ] **Frontend: Indicadores Visuales**
  - Mostrar estado actual del refinamiento
  - Deshabilitar controles durante streaming
  - Mensajes claros de progreso

### Fase 7.5: Internacionalización i18n (NUEVA - PRIORIDAD 2)
**Archivo:** `Planeacion_base/07_5_fase_internacionalizacion.md`

- [ ] 7.5.1: Crear templates de prompts bilingües
  - Archivo `backend/app/prompts/i18n_templates.py`
  - Templates en español para todos los agentes
  - Templates en inglés para todos los agentes
  - Función `get_templates(language)` para selección

- [ ] 7.5.2: Actualizar estado del workflow para incluir idioma
  - Agregar campo `language` a `PromptState`
  - Default: `"spanish"`
  - Valores válidos: `"spanish"`, `"english"`

- [ ] 7.5.3: Integrar templates i18n en nodos del workflow
  - Actualizar `clarify_node()` para usar templates dinámicos
  - Actualizar `generate_node()` para usar templates dinámicos
  - Actualizar `evaluate_node()` para usar templates dinámicos
  - Actualizar `judge_node()` para usar templates dinámicos
  - Actualizar `refiner_node()` para usar templates dinámicos

- [ ] 7.5.4: Crear endpoint de configuración de idioma
  - GET `/api/settings/language` - Obtener idioma actual
  - POST `/api/settings/language` - Guardar preferencia de idioma
  - Validar idioma soportado

- [ ] 7.5.5: Crear provider de idiomas (React Context)
  - Archivo `frontend/src/contexts/LanguageContext.tsx`
  - Estado `language` y función `setLanguage`
  - Función `t()` para traducciones
  - Cargar traducciones desde archivos JSON

- [ ] 7.5.6: Crear archivos de traducción (JSON)
  - `frontend/public/i18n/spanish.json` - Traducciones ES
  - `frontend/public/i18n/english.json` - Traducciones EN
  - Todas las keys de la UI en ambos idiomas

- [ ] 7.5.7: Crear componente switcher de idioma
  - `frontend/src/components/language-switcher.tsx`
  - Dropdown con emojis de banderas
  - Función para cambiar idioma

- [ ] 7.5.8: Integrar LanguageProvider en layout principal
  - `frontend/src/app/layout.tsx` - Envolver app con provider
  - Actualizar atributo `lang` del HTML dinámicamente

- [ ] 7.5.9: Migrar componentes existentes para usar traducciones
  - Onboarding form
  - Settings page (cuando se cree)
  - Main page
  - Chat interface
  - Arena view
  - Reemplazar textos fijos por `t('key')`

- [ ] 7.5.10: Integrar language-switcher en el header
  - Agregar switcher en posición visible
  - Accesible en todas las páginas

- [ ] 7.5.11: Testing y validación de i18n
  - Probar cambio de idioma en toda la UI
  - Probar que los prompts del agente se generen en el idioma correcto
  - Verificar persistencia de idioma

### Fase 8: Tipos de Prompt Modulares (ACTUALIZADA)
**Archivo:** `Planeacion_base/08_fase_tipos_prompt_modulares_ACTUALIZADA.md`

- [ ] 8.1: Crear enumeración de tipos de prompt
  - Archivo `backend/app/core/prompt_types.py`
  - Enum `PromptType`: BASIC, SYSTEM, IMAGE, ADDITIONAL
  - `PROMPT_TYPE_CONFIGS` con metadatos de cada tipo
  - Funciones auxiliares: `get_prompt_type_config()`, `get_enabled_prompt_types()`

- [ ] 8.2: Crear Factory Pattern para workflows
  - Archivo `backend/app/agents/workflow_factory.py`
  - Función `get_workflow_graph(prompt_type, checkpointer)`
  - Selección dinámica de workflow según tipo
  - Importar workflows específicos cuando se implementen

- [ ] 8.3: Crear endpoint de tipos de prompt
  - GET `/api/prompts/types` - Listar todos los tipos
  - GET `/api/prompts/types/available` - Solo tipos habilitados
  - Incluir metadatos para UI (icono, color, descripción)

- [ ] 8.4: Crear UI de selector de tipo de prompt
  - `frontend/src/components/prompt-type-selector.tsx`
  - Grid de cards mostrando tipos disponibles
  - Indicadores de estado (enabled/coming soon)
  - Deshabilitar tipos no habilitados

- [ ] 8.5: Integrar selector en UI principal
  - `frontend/src/app/page.tsx` - Agregar estado `promptType`
  - Renderizar `PromptTypeSelector` antes del input
  - Pasar tipo seleccionado al workflow

- [ ] 8.6: Habilitar System Prompts (Fase 8.6 - PREPARACIÓN)
  - Crear workflow específico para system prompts
  - Implementar lógica específica para system prompts
  - Requiere input de prueba del usuario

- [ ] 8.7: Habilitar Image Prompts (Fase 8.7 - PREPARACIÓN)
  - Crear workflow específico para image prompts
  - Templates especializados para generación de imágenes
  - Solo generar texto del prompt (no la imagen)

- [ ] 8.8: Habilitar Additional Prompts (Fase 8.8 - PREPARACIÓN)
  - Crear workflow específico para additional prompts
  - Posible reutilización de workflow básico con adaptaciones

### Fase 9: Validación de API Key de Test (NUEVA)
**Archivo:** `Planeacion_base/09_fase_validacion_test_api_key.md`

- [ ] 9.1: Crear endpoint de validación especial
  - POST `/api/settings/validate-test` - Valida sin guardar en BD
  - Validación real con el servicio LLM
  - Diferente de `/api/settings/validate` (que sí guarda)

- [ ] 9.2: Modo de test para propietario
  - **Opción A (Variable de entorno):** `PROMPTFORGE_TEST_MODE=true`
  - **Opción B (Parámetro de URL):** `?test_mode=true&test_key=...`
  - **Opción C (Token de validación):** Tokens temporales que expiran

- [ ] 9.3: Implementación en frontend (si aplica)
  - Panel de modo de test (si usa opción B o C)
  - Gestor de tokens (si usa opción C)
  - Oculto en producción normal

- [ ] 9.4: Testing y validación
  - Probar validación exitosa
  - Probar validación fallida
  - Probar rate limiting
  - Verificar que NO se guarde en BD
  - Verificar que NO aparezca en UI normal

### Fases de Integración (Continuación de Fases Existentes)

- [ ] **Integración completa:** Unificar todas las nuevas funcionalidades
- [ ] **Testing end-to-end:** Flujos completos probados
- [ ] **Corrección de bugs:** Issues identificados y resueltos
- [ ] **Documentación actualizada:** README.md con todas las nuevas funcionalidades

---

## 📊 Resumen de Nuevas Funcionalidades

### 1. ✅ Gestión de API Keys
- Múltiples proveedores simultáneamente
- Una API key por proveedor activa
- Eliminar API keys con confirmación
- Reconfigurar API keys en cualquier momento

### 2. ✅ Internacionalización (i18n)
- Switcher de idioma funcional (English/Spanish)
- UI completa en ambos idiomas
- Prompts del agente bilingües
- Workflows adaptados según idioma

### 3. ✅ Tipos de Prompt
- Basic (ya funcional)
- System Prompt (requiere input de prueba)
- Image Prompt (generar texto para DALL-E, Midjourney)
- Additional Prompt (complementarios)
- Arquitectura modular

### 4. ✅ Validación de API Key de Test
- Solo el propietario puede usarla
- No guardar en base de datos
- No aparecer en UI normal
- Validación temporal sin persistencia

### 5. ✅ Mejoras de UX
- Acceso a onboarding desde settings
- Reconfigurar API keys fácilmente
- Validación de API keys activas al inicio

---

## 📚 Documentos de Planificación

Todos los detalles técnicos están disponibles en los siguientes documentos:

1. **`06_5_fase_api_keys_manager.md`** - Detalle de Fase 6.5 (Gestión de API Keys)
2. **`07_5_fase_internacionalizacion.md`** - Detalle de Fase 7.5 (Internacionalización)
3. **`08_fase_tipos_prompt_modulares_ACTUALIZADA.md`** - Detalle de Fase 8 (Tipos de Prompt)
4. **`09_fase_validacion_test_api_key.md`** - Detalle de Fase 9 (Validación de API Key de Test)

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

**Documentos creados:** 4 documentos de detalle (60-80 páginas cada uno)
**Preguntas clave totales:** 115+ preguntas distribuidas en todas las tareas
**Arquitectura modular:** Preparada para expansiones futuras

---

## 🚀 Próximos Pasos

### Para el Usuario:

1. **Revisar los documentos de planificación**
   - Leer `06_5_fase_api_keys_manager.md`
   - Leer `07_5_fase_internacionalizacion.md`
   - Leer `08_fase_tipos_prompt_modulares_ACTUALIZADA.md`
   - Leer `09_fase_validacion_test_api_key.md`

2. **Responder las preguntas clave**
   - Las preguntas están diseñadas para facilitar la implementación
   - Tus respuestas guiarán las decisiones técnicas

3. **Priorizar la implementación**
   - Recomendado: Empezar con Sprint 1 (Gestión de API Keys)
   - Es la funcionalidad más crítica y bloquea otras

4. **Comenzar la implementación**
   - Usar los documentos como guía paso a paso
   - Seguir el orden de tareas en cada fase

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

---

**Planificación Creada Por:** OpenCode Assistant  
**Fecha:** 16 de febrero de 2026  
**Versión:** 2.0 (ACTUALIZADA) - Todos los requerimientos integrados  
**Estado:** ✅ LISTA PARA IMPLEMENTACIÓN Y EJECUCIÓN
