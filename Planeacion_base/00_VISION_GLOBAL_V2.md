# 00. Visión Global: PromptForge V2.0

**Fecha de Creación:** 17 de Febrero de 2026  
**Versión del Documento:** 2.0  
**Estado:** ✅ ACTIVO  
**Última Actualización:** 17 de Febrero de 2026

---

## 📋 Concepto del Proyecto

**PromptForge** es una herramienta profesional de ingeniería de prompts diseñada para elevar el estándar de interacción con LLMs. Transforma una idea vaga en un prompt de producción mediante un proceso estructurado de **clarificación, generación de variantes, validación automática, refinamiento experto y testing competitivo (Arena).**

### 🎯 Misión

Democratizar la ingeniería de prompts de alta calidad, permitiendo que cualquier usuario—desde desarrolladores hasta profesionales no técnicos—pueda crear prompts profesionales y efectivos para sus casos de uso específicos.

---

## 🎯 Objetivos Principales

### 1. **Calidad sobre Cantidad**
No generar un solo prompt, sino explorar el espacio de soluciones con 3 variantes competitivas que ofrecen diferentes enfoques y estilos.

### 2. **Ciclo de Feedback Humano**
El usuario no es un espectador pasivo; es el juez final en la "Arena" y el director en la fase de refinamiento. La IA propone, el humano decide.

### 3. **Agnosticismo de Modelo**
Diseñado para funcionar con cualquier proveedor de LLM:
- **OpenAI** (GPT-4, GPT-3.5-turbo)
- **Anthropic** (Claude 3)
- **Ollama** (Modelos locales)
- Extensible a nuevos proveedores

### 4. **Seguridad y Privacidad**
- Gestión local de credenciales
- Encriptación de API keys en reposo (Fernet)
- Sin envío de datos a servidores externos
- Base de datos SQLite local

### 5. **Internacionalización**
Soporte completo para múltiples idiomas:
- **Español** (idioma por defecto)
- **English**
- Extensible a más idiomas

### 6. **Arquitectura Modular**
Soporte para múltiples tipos de prompt con workflows específicos:
- **Basic Prompts:** Prompts estándar para tareas generales
- **System Prompts:** Prompts que definen el comportamiento del sistema
- **Image Prompts:** Optimizados para generación de imágenes (DALL-E, Midjourney, Stable Diffusion)
- **Additional Prompts:** Templates y casos de uso específicos

---

## 🏗️ Stack Tecnológico

### Backend (Python 3.12+)

**Framework y Servicios:**
- **FastAPI 0.109.2** - Framework API REST con validación automática
- **Uvicorn 0.27.1** - Servidor ASGI de alto rendimiento
- **LangGraph 0.2.76** - Orquestación de flujos cíclicos y stateful con agentes
- **LangChain 0.2.17** - Abstracción de LLM y herramientas
- **LiteLLM 1.25.2** - Interfaz unificada para múltiples proveedores de LLM

**Base de Datos y Persistencia:**
- **SQLite** - Base de datos ligera y local
- **SQLAlchemy 2.0.27** - ORM para Python
- **aiosqlite 0.20.0** - Driver async para SQLite
- **AsyncSqliteSaver** - Checkpointer de LangGraph para persistencia de estado

**Seguridad:**
- **cryptography 42.0.2** - Librería Fernet para encriptación de API keys en reposo

**Arquitectura Backend:**
```
backend/
├── app/
│   ├── agents/              # Orquestación con LangGraph
│   │   ├── graph.py         # Definición del grafo de workflow
│   │   ├── nodes.py         # Nodos del workflow (clarify, generate, evaluate, judge, refine)
│   │   ├── state.py         # Esquema de estado (PromptState TypedDict)
│   │   └── workflow_factory.py  # Factory para workflows modulares
│   ├── api/                 # Endpoints REST
│   │   ├── endpoints.py     # Settings, API keys, arena
│   │   ├── workflow.py      # Workflow streaming con SSE
│   │   ├── user_preferences.py  # Preferencias de usuario
│   │   └── schemas.py       # Modelos Pydantic
│   ├── core/                # Lógica de negocio
│   │   ├── workflow_manager.py  # Singleton de gestión de workflows
│   │   ├── config_service.py    # Servicio de configuración
│   │   ├── security.py          # Encriptación/desencriptación
│   │   └── prompt_types.py      # Configuración de tipos de prompt
│   ├── db/                  # Capa de base de datos
│   │   ├── database.py      # Setup de SQLAlchemy
│   │   ├── models.py        # Modelos (Settings, ApiKey, UserPreferences)
│   │   └── migrations/      # Migraciones de esquema
│   ├── prompts/             # Templates de prompts
│   │   ├── templates.py     # Templates en español (legacy)
│   │   ├── i18n_templates.py    # Templates multi-idioma
│   │   └── helpers.py       # Helpers para templates
│   └── services/            # Servicios de negocio
│       ├── llm_engine.py    # Motor de ejecución de LLM
│       └── user_service.py  # Servicio de preferencias
└── main.py                  # Entry point de la aplicación
```

### Frontend (Next.js 16)

**Framework y Librerías:**
- **Next.js 16.1.6** - Framework React con Turbopack
- **React 19.2.3** - Librería UI
- **TypeScript 5** - Tipado estático

**UI y Estilos:**
- **Tailwind CSS 4** - Framework CSS utility-first
- **Radix UI** - Componentes accesibles (Dialog, etc.)
- **Lucide React 0.564.0** - Iconos
- **Framer Motion 12.34.0** - Animaciones

**Estado y Data Fetching:**
- **Zustand 5.0.11** - State management minimalista
- **TanStack Query 5.90.21** - Data fetching y caching
- **@microsoft/fetch-event-source 2.0.1** - SSE para streaming

**Visualización:**
- **Recharts 3.7.0** - Gráficos y visualizaciones
- **react-markdown 10.1.0** - Renderizado de markdown

**Internacionalización:**
- **React Context** - Provider de idioma
- **JSON files** - Archivos de traducciones

**Arquitectura Frontend:**
```
frontend/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── page.tsx         # Página principal (workflow)
│   │   ├── layout.tsx       # Layout raíz con providers
│   │   ├── settings/        # Página de configuración
│   │   └── globals.css      # Estilos globales
│   ├── components/          # Componentes React
│   │   ├── arena/           # Componentes de Arena
│   │   │   ├── ArenaView.tsx        # Vista comparativa
│   │   │   ├── ChatInterface.tsx    # Chat de clarificación
│   │   │   ├── PromptCard.tsx       # Card de variante
│   │   │   └── EvaluationChart.tsx  # Gráficos de evaluación
│   │   ├── ui/              # Componentes base UI
│   │   ├── onboarding-form.tsx      # Formulario inicial
│   │   ├── api-keys-manager.tsx     # Gestión de API keys
│   │   ├── language-switcher.tsx    # Selector de idioma
│   │   ├── provider-selector.tsx    # Selector de proveedor
│   │   └── prompt-type-selector.tsx # Selector de tipo de prompt
│   ├── contexts/            # React Contexts
│   │   └── LanguageContext.tsx      # Contexto i18n
│   ├── store/               # Zustand stores
│   │   └── workflowStore.ts         # Estado global del workflow
│   ├── config/              # Configuración
│   │   └── api.ts           # Base URL de API
│   └── lib/                 # Utilidades
└── public/
    └── i18n/                # Archivos de traducción
        ├── spanish.json
        └── english.json
```

---

## 🔄 Flujo de Usuario (The Happy Path)

### 1. **Onboarding Inicial**
- Usuario ingresa su primera API Key
- Sistema valida la key con el proveedor (ping test)
- Almacenamiento seguro con encriptación Fernet
- Configuración de preferencias básicas (idioma, nombre)

### 2. **Configuración de Preferencias**
- Selección de idioma (Español/English)
- Selección de tipo de prompt (Basic/System/Image/Additional)
- Gestión de múltiples API keys (OpenAI, Anthropic, Ollama)
- Una key activa por proveedor a la vez

### 3. **Inicio del Workflow**
- Usuario ingresa su idea o necesidad base
- Sistema selecciona el workflow según tipo de prompt
- Inicialización del estado con LangGraph

### 4. **Fase de Clarificación**
- **Agente Clarificador** analiza la entrada del usuario
- Identifica ambigüedades y vacíos de información
- Formula preguntas de clarificación específicas
- Usuario responde en modo conversacional
- Proceso iterativo hasta tener todos los requerimientos

### 5. **Fase de Generación**
- **3 Agentes Generadores** trabajan en paralelo
- Cada agente usa una "persona" diferente (enfoque distinto)
- Generación de 3 variantes competitivas del prompt
- Variantes optimizadas según el tipo de prompt seleccionado

### 6. **Fase de Evaluación**
- **Agente Evaluador** analiza cada variante
- Criterios: Claridad, Precisión, Completitud, Seguridad, Eficacia
- Puntuación de 1-10 para cada criterio
- Sugerencias de mejora específicas

### 7. **Fase de Refinamiento**
- **Agente Refinador** aplica mejoras automáticas
- Incorpora feedback del evaluador
- Optimización de estructura y formato
- Genera versiones refinadas de las variantes

### 8. **Arena: Testing y Comparación**

**Para Prompts Normales:**
- Ejecución automática de las 3 variantes
- Comparación lado a lado de resultados
- Visualización de evaluaciones con gráficos

**Para System Prompts:**
- Usuario ingresa un input de prueba
- Sistema ejecuta las 3 variantes con el mismo input
- Comparación de comportamientos

**Para Image Prompts:**
- Generación de textos optimizados para diferentes generadores de imágenes
- Comparación de estructura y keywords
- Testing opcional con DALL-E (si configurado)

### 9. **Decisión Final**
- Usuario elige la variante ganadora
- Opción de copiar al portapapeles
- Opción de pedir refinamiento adicional (loop)
- Opción de iniciar un nuevo workflow

---

## 🎨 Principios de Diseño

### 1. **Transparencia**
El usuario siempre sabe en qué fase del proceso está y qué está haciendo el sistema.

### 2. **Control Humano**
La IA propone, el humano decide. Cada decisión importante requiere aprobación del usuario.

### 3. **Iteración Rápida**
Ciclos cortos de feedback para llegar rápidamente al resultado deseado.

### 4. **Progreso Visible**
Indicadores visuales claros de progreso, estado y próximos pasos.

### 5. **Recuperación de Errores**
Manejo gracioso de errores con mensajes claros y opciones de recuperación.

### 6. **Accesibilidad**
UI intuitiva que funciona para usuarios técnicos y no técnicos.

---

## 🌍 Internacionalización

### Alcance i18n

**UI Completa:**
- Todos los textos de la interfaz
- Mensajes de error y confirmación
- Tooltips y ayudas
- Documentación en la app

**Agentes:**
- Templates de prompts en español e inglés
- Respuestas del sistema en el idioma seleccionado
- Preguntas de clarificación
- Evaluaciones y feedback

**Persistencia:**
- Preferencia de idioma guardada en base de datos
- Sincronización entre frontend y backend
- Soporte para cambio de idioma en tiempo real

---

## 🔐 Seguridad y Privacidad

### Principios de Seguridad

**1. Local-First:**
- Toda la data se almacena localmente
- No hay servidores externos involucrados
- Base de datos SQLite en el filesystem

**2. Encriptación en Reposo:**
- API keys encriptadas con Fernet (symmetric encryption)
- Clave de encriptación en variable de entorno
- Desencriptación solo en memoria durante uso

**3. Sin Logs Sensibles:**
- API keys nunca se escriben en logs
- Prompts del usuario no se persisten (solo en workflow state temporal)
- Limpieza de estado al finalizar workflow

**4. Validación Estricta:**
- Validación de API keys con proveedores antes de guardar
- Sanitización de inputs del usuario
- Validación de tipos y esquemas con Pydantic

---

## 🧩 Arquitectura Modular: Tipos de Prompt

### 1. **Basic Prompts (Completado)**
**Casos de uso:**
- Prompts para tareas generales
- Conversaciones
- Análisis de texto
- Generación de contenido

**Workflow:**
- Clarificación estándar
- Generación con 3 personas
- Evaluación completa
- Refinamiento iterativo

### 2. **System Prompts (Planificado - Sprint 4)**
**Casos de uso:**
- Definir comportamiento de chatbots
- Configurar asistentes especializados
- Establecer reglas de interacción

**Workflow:**
- Clarificación enfocada en comportamiento deseado
- Generación con énfasis en consistencia
- Testing manual con inputs de prueba del usuario
- Evaluación de adherencia a reglas

### 3. **Image Prompts (Planificado - Sprint 4)**
**Casos de uso:**
- DALL-E 3
- Midjourney
- Stable Diffusion
- Generadores de imágenes

**Workflow:**
- Clarificación visual (estilo, composición, detalles)
- Generación optimizada para cada plataforma
- Evaluación de keywords y estructura
- Testing opcional con DALL-E

### 4. **Additional Prompts (Planificado - Sprint 4)**
**Casos de uso:**
- Templates pre-construidos
- Casos de uso específicos de industrias
- Prompts para tareas técnicas

**Workflow:**
- Selección de template base
- Personalización con variables
- Validación de completitud
- Testing con datos de ejemplo

---

## 📊 Estado del Proyecto (17/02/2026)

### ✅ Completado (MVP Básico - Fases 1-5)

**Backend:**
- ✅ Framework FastAPI configurado y funcionando
- ✅ Orquestación con LangGraph implementada
- ✅ Workflow básico: Clarify → Generate → Evaluate
- ✅ Streaming SSE para generación en tiempo real
- ✅ Encriptación de API keys con Fernet
- ✅ Base de datos SQLite con modelos definidos
- ✅ Endpoints REST para configuración y workflow
- ✅ Sistema de gestión de API keys multi-proveedor

**Frontend:**
- ✅ Next.js 16 con TypeScript configurado
- ✅ Componentes UI con Tailwind CSS
- ✅ ChatInterface para clarificación
- ✅ ArenaView para comparación de variantes
- ✅ WorkflowStore con Zustand
- ✅ Integración SSE para streaming
- ✅ Sistema de gestión de API keys UI

**Integración:**
- ✅ Conexión frontend-backend funcional
- ✅ Variables de entorno correctamente configuradas
- ✅ Flujo completo de workflow testeado

### 🔄 En Proceso (Sprint 1)

**Corrección de Bugs:**
- 🔄 Bug crítico: Respuesta vacía del asistente en primera clarificación
- 🔄 Análisis de logs y corrección de errores menores
- 🔄 Mejoras de UX básico

**Navegación:**
- 🔄 Implementación de botón "Volver al Inicio"
- 🔄 Navegación consistente entre vistas

### ⏳ Pendiente (Sprints 2-5)

**Sprint 2 - Gestión de Configuración:**
- ⏳ Tabla `user_preferences` en base de datos
- ⏳ Sistema completo de gestión de API keys UI
- ⏳ Validación de configuración antes de usar workflow
- ⏳ Integración completa de settings

**Sprint 3 - Internacionalización:**
- ⏳ Templates de prompts bilingües (ES/EN)
- ⏳ Backend i18n con campo `language` en estado
- ⏳ Frontend Context i18n con React
- ⏳ Archivos de traducción JSON
- ⏳ Language switcher UI

**Sprint 4 - Tipos de Prompt Modulares:**
- ⏳ Factory pattern para workflows
- ⏳ Workflows específicos para cada tipo
- ⏳ UI selector de tipos de prompt
- ⏳ Testing de workflows modulares

**Sprint 5 - Optimización:**
- ⏳ Tarjeta de contexto (tokens, modelo)
- ⏳ Dockerización completa
- ⏳ Documentación README actualizada
- ⏳ Testing E2E
- ⏳ Optimizaciones de performance

---

## 🎯 Visión a Futuro (Post-Sprint 5)

### Funcionalidades Potenciales

**1. Colaboración:**
- Compartir prompts entre usuarios
- Galería de prompts comunitarios
- Exportación a formatos estándar

**2. Analytics:**
- Métricas de uso de tokens
- Estadísticas de proveedores
- Historial de prompts generados

**3. Integraciones:**
- Exportación directa a plataformas LLM
- Integración con APIs de terceros
- Plugins para IDEs

**4. Más Proveedores:**
- Google PaLM
- Cohere
- HuggingFace Inference API
- Azure OpenAI

**5. Más Tipos de Prompt:**
- Code Generation Prompts
- Data Analysis Prompts
- Creative Writing Prompts
- Educational Prompts

---

## 📚 Referencias

- **LangGraph Docs:** https://langchain-ai.github.io/langgraph/
- **LiteLLM Docs:** https://docs.litellm.ai/
- **Next.js 16 Docs:** https://nextjs.org/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com/

---

> **Nota de Arquitectura:** Este documento representa el "Norte Geográfico" del proyecto. Si en algún momento una feature contradice estos objetivos (ej: sacrificar seguridad por velocidad, o eliminar el loop humano), debemos detenernos y re-evaluar.

**Última Actualización:** 17 de Febrero de 2026  
**Versión:** 2.0  
**Autor:** Equipo PromptForge
