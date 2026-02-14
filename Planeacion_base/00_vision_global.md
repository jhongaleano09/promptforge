# 00. Visión Global: PromptForge

## 📋 Concepto del Proyecto
**PromptForge** es una herramienta profesional de ingeniería de prompts diseñada para elevar el estándar de interacción con LLMs. Transforma una idea vaga en un prompt de producción mediante un proceso estructurado de **clarificación, generación de variantes, validación automática, refinamiento experto y testing competitivo (Arena).**

### 🎯 Objetivos Principales
1.  **Calidad sobre Cantidad:** No generar un solo prompt, sino explorar el espacio de soluciones con 3 variantes competitivas.
2.  **Ciclo de Feedback Humano:** El usuario no es un espectador pasivo; es el juez final en la "Arena" y el director en la fase de refinamiento.
3.  **Agnosticismo de Modelo:** Diseñado para funcionar con cualquier proveedor (OpenAI, Anthropic, GLM, Local LLMs via Ollama) mediante una capa de abstracción.
4.  **Seguridad y Privacidad:** Gestión local y encriptada de credenciales.

## 🏗️ Arquitectura de Alto Nivel

### Stack Tecnológico
*   **Backend:** Python 3.11+
    *   **Framework API:** FastAPI.
    *   **Orquestación:** LangGraph (para flujos cíclicos y stateful).
    *   **LLM Interface:** LiteLLM (para estandarizar llamadas a APIs).
    *   **Base de Datos:** SQLite (ligera, archivo local) con SQLAlchemy.
    *   **Seguridad:** Librería `cryptography` (Fernet) para encriptación de API Keys en reposo.
*   **Frontend:**
    *   **Framework:** Next.js 14 (React).
    *   **UI Libs:** Tailwind CSS, Shadcn/UI, Lucide Icons.
    *   **Estado:** Zustand + React Query.

### Flujo de Usuario (The Happy Path)
1.  **Onboarding:** Usuario ingresa API Key -> Validación (Ping) -> Almacenamiento Seguro.
2.  **Definición:** Usuario selecciona tipo (Prompt Normal, System Prompt, etc.) e ingresa idea base.
3.  **Clarificación:** Agente entrevista al usuario para llenar vacíos de información.
4.  **Generación:** 3 Agentes crean variantes en paralelo (Enfoques distintos).
5.  **Evaluación:** Agente crítico puntúa cada variante y sugiere mejoras.
6.  **Refinamiento:** Agente experto aplica mejoras.
7.  **Arena (Testing):**
    *   *Prompt Normal:* Ejecución automática.
    *   *System Prompt:* Usuario ingresa input de prueba -> Ejecución.
8.  **Decisión:** Usuario elige ganador o pide refinamiento (Loop).

## 🗺️ Estructura de Fases de Desarrollo
Esta documentación se divide en las siguientes fases operativas:

1.  **Fase 1: Esqueleto y Seguridad** (`01_esqueleto_seguridad.md`)
    *   Setup del proyecto, BD y manejo seguro de credenciales.
2.  **Fase 2: Cerebro de Prompts** (`02_cerebro_prompts.md`)
    *   Diseño y testeo de los prompts internos que usarán los agentes.
3.  **Fase 3: Orquestación Core** (`03_orquestacion_core.md`)
    *   Implementación del grafo lineal (Clarificar -> Generar -> Evaluar).
4.  **Fase 4: Interfaz Arena** (`04_interfaz_arena.md`)
    *   Frontend para visualizar y comparar resultados en tiempo real.
5.  **Fase 5: Loops y System Prompts** (`05_loops_y_system.md`)
    *   Lógica compleja de feedback y testing manual de system prompts.

---
> **Nota de Arquitectura:** Este documento sirve como "Norte Geográfico". Si en algún momento una feature contradice estos objetivos (ej: sacrificar seguridad por velocidad, o eliminar el loop humano), debemos detenernos y re-evaluar.
