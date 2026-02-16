# 00. Visión Global: PromptForge

## 📋 Concepto del Proyecto
**PromptForge** es una herramienta profesional de ingeniería de prompts diseñada para elevar el estándar de interacción con LLMs. Transforma una idea vaga en un prompt de producción mediante un proceso estructurado de **clarificación, generación de variantes, validación automática, refinamiento experto y testing competitivo (Arena).**

### 🎯 Objetivos Principales
1.  **Calidad sobre Cantidad:** No generar un solo prompt, sino explorar el espacio de soluciones con 3 variantes competitivas.
2.  **Ciclo de Feedback Humano:** El usuario no es un espectador pasivo; es el juez final en la "Arena" y el director en la fase de refinamiento.
3.  **Agnosticismo de Modelo:** Diseñado para funcionar con cualquier proveedor (OpenAI, Anthropic, GLM, Local LLMs via Ollama) mediante una capa de abstracción.
4.  **Seguridad y Privacidad:** Gestión local y encriptada de credenciales.
5.  **Internacionalización:** Soporte completo para múltiples idiomas (English/Spanish).
6.  **Arquitectura Modular:** Soporte para múltiples tipos de prompt con workflows específicos.

## 🏗️ Arquitectura de Alto Nivel

### Stack Tecnológico
*   **Backend:** Python 3.11+
    *   **Framework API:** FastAPI.
    *   **Orquestación:** LangGraph (para flujos cíclicos y stateful).
    *   **LLM Interface:** LiteLLM (para estandarizar llamadas a APIs).
    *   **Base de Datos:** SQLite (ligera, archivo local) con SQLAlchemy.
    *   **Seguridad:** Librería `cryptography` (Fernet) para encriptación de API Keys en reposo.
*   **Frontend:**
    *   **Framework:** Next.js 16 (React).
    *   **UI Libs:** Tailwind CSS, Shadcn/UI, Lucide Icons.
    *   **Estado:** Zustand + React Query.
    *   **Internacionalización:** React Context + JSON files.

### Flujo de Usuario (The Happy Path)
1.  **Onboarding:** Usuario ingresa API Key → Validación (Ping) → Almacenamiento Seguro.
2.  **Definición:** Usuario selecciona tipo (Basic, System, Image, Additional) e ingresa idea base.
3.  **Clarificación:** Agente entrevista al usuario para llenar vacíos de información.
4.  **Generación:** 3 Agentes crean variantes en paralelo (Enfoques distintos).
5.  **Evaluación:** Agente crítico puntúa cada variante y sugiere mejoras.
6.  **Refinamiento:** Agente experto aplica mejoras.
7.  **Arena (Testing):**
    *   *Prompt Normal:* Ejecución automática.
    *   *System Prompt:* Usuario ingresa input de prueba → Ejecución.
    *   *Image Prompt:* Generación de texto para DALL-E, Midjourney, Stable Diffusion.
8.  **Decisión:** Usuario elige ganador o pide refinamiento (Loop).

## 🗺️ Estructura de Fases de Desarrollo

Esta documentación se divide en las siguientes fases operativas:

### Fase 1-5: Completadas (MVP Básico)
- [x] **Fase 1: Esqueleto y Seguridad** (`01_esqueleto_seguridad.md`)
    *   Setup del proyecto, BD y manejo seguro de credenciales.
- [x] **Fase 2: Cerebro de Prompts** (`02_cerebro_prompts.md`)
    *   Diseño y testeo de los prompts internos que usarán los agentes.
- [x] **Fase 3: Orquestación Core** (`03_orquestacion_core.md`)
    *   Implementación del grafo lineal (Clarificar -> Generar -> Evaluar).
- [x] **Fase 4: Interfaz Arena** (`04_interfaz_arena.md`)
    *   Frontend para visualizar y comparar resultados en tiempo real.
- [x] **Fase 5: Loops y System Prompts** (`05_loops_y_system.md`)
    *   Lógica compleja de feedback y testing manual de system prompts.

### Fase 6: Consolidación y Documentación (EN PROCESO)
- [x] **Planificación:** Documentos maestros creados
- [ ] **Dockerización:** Crear Dockerfiles y docker-compose.yml
- [ ] **Documentación Maestra (`README.md`):** Actualizar con nuevas funcionalidades

### Fase 6.5: Sistema de Gestión de API Keys (PRIORIDAD 1 - CRÍTICA)
- [ ] **Rediseñar modelo de base de datos:** Tabla `api_keys` con soporte para múltiples proveedores
- [ ] **Script de migración:** Migrar datos de `settings` a `api_keys`
- [ ] **Endpoints CRUD:** Gestión completa de API keys (GET, POST, DELETE, PUT)
- [ ] **UI de Settings:** Componente visual para gestión de API keys
- [ ] **Integración con UI existente:** Acceso desde settings y validación al inicio
- [ ] **Testing:** Pruebas completas de funcionalidad

**Detalles completos:** `Planeacion_base/06_5_fase_api_keys_manager.md`

### Fase 7.5: Internacionalización i18n (PRIORIDAD 2 - ALTA)
- [ ] **Templates bilingües:** Crear templates de prompts en español e inglés
- [ ] **Actualizar estado del workflow:** Agregar campo `language` a `PromptState`
- [ ] **Integrar templates en nodos:** Actualizar todos los nodos para usar templates dinámicos
- [ ] **Endpoint de idioma:** Guardar y obtener preferencia de idioma del usuario
- [ ] **Provider React Context:** Crear contexto de idioma para el frontend
- [ ] **Archivos de traducción:** JSON con todas las traducciones de la UI
- [ ] **Switcher de idioma:** Componente UI para cambiar idioma
- [ ] **Integrar en layout:** Envolver app con LanguageProvider
- [ ] **Migrar componentes:** Reemplazar textos fijos por llamadas a `t()`
- [ ] **Testing:** Validar internacionalización completa

**Detalles completos:** `Planeacion_base/07_5_fase_internacionalizacion.md`

### Fase 8: Tipos de Prompt Modulares (PRIORIDAD 3 - MEDIA)
- [ ] **Enumeración de tipos:** Definir PromptType (BASIC, SYSTEM, IMAGE, ADDITIONAL)
- [ ] **Factory Pattern:** Crear factory para seleccionar workflow según tipo
- [ ] **Endpoint de tipos:** Listar todos los tipos de prompt disponibles
- [ ] **UI de selector:** Componente visual para seleccionar tipo de prompt
- [ ] **Integración en UI principal:** Pasar tipo seleccionado al workflow
- [ ] **Habilitar System Prompts:** Workflow específico para system prompts
- [ ] **Habilitar Image Prompts:** Workflow específico para image prompts
- [ ] **Habilitar Additional Prompts:** Workflow específico para additional prompts

**Detalles completos:** `Planeacion_base/08_fase_tipos_prompt_modulares_ACTUALIZADA.md`

### Fase 9: Validación de API Key de Test (PRIORIDAD 4 - BAJA)
- [ ] **Endpoint de validación especial:** Validar API key sin guardar en BD
- [ ] **Modo de test para propietario:** Sistema para validación exclusiva del desarrollador
- [ ] **Implementación en frontend:** Panel de modo de test (si aplica)
- [ ] **Testing:** Validar funcionalidad completa

**Detalles completos:** `Planeacion_base/09_fase_validacion_test_api_key.md`

## 📊 Estado del Proyecto (16/02/2026)

### Completado
- ✅ MVP funcional con workflow básico
- ✅ Validación de API keys básica
- ✅ Interfaz de chat y arena
- ✅ Orquestación con LangGraph
- ✅ Streaming SSE para generación
- ✅ Encriptación de API keys en reposo

### En Proceso
- 🔄 Planificación de nuevas funcionalidades
- 🔄 Documentación maestra consolidada

### Pendiente
- ⏳ Gestión de múltiples API keys
- ⏳ Internacionalización completa
- ⏳ Tipos de prompt modulares
- ⏳ Validación de API key de test
- ⏳ Dockerización
- ⏳ Documentación README actualizada

---

> **Nota de Arquitectura:** Este documento sirve como "Norte Geográfico". Si en algún momento una feature contradice estos objetivos (ej: sacrificar seguridad por velocidad, o eliminar el loop humano), debemos detenernos y re-evaluar.

**Última actualización:** 16 de febrero de 2026  
**Versión:** 2.0 (Actualizada con nuevas fases)