# 📅 Plan de Desarrollo y Bitácora - PromptForge

**Fecha de Validación:** 16 de Febrero de 2026  
**Estado:** Validación de Prototipo / Inicio de Fase de Consolidación  
**Versión del Documento:** 1.0  

## 1. 🔍 Diagnóstico del Estado Actual (16/02/2026)

El sistema se encuentra en un estado de **MVP Avanzado (Minimum Viable Product)**. Se ha superado la fase de "Prueba de Concepto" y se dispone de una arquitectura funcional.

### A. Backend (Python/FastAPI)
- **Estado:** ✅ Estable
- **Arquitectura:** Modular (`app/core`, `app/api`, `app/agents`).
- **Orquestación:** Implementación exitosa de **LangGraph** para el flujo `Clarify -> Generate -> Evaluate`.
- **Streaming:** Se ha implementado **Server-Sent Events (SSE)** para la generación de variantes, proporcionando una UX moderna.
- **Seguridad:** Cifrado de API Keys en reposo utilizando `fernet` (cryptography).
- **Persistencia:** SQLite local funcional.
- **Deuda Técnica:** 
    - Falta de unificación en la UX de refinamiento (actualmente HTTP estándar, debería ser Streaming).
    - Validación de integración con Ollama pendiente de pruebas exhaustivas.

### B. Frontend (Next.js 14)
- **Estado:** ✅ Funcional y Estético
- **Tecnología:** React, Tailwind CSS, Zustand (State Management).
- **Componentes:** 
    - `Onboarding`: Gestión de API Keys.
    - `ChatInterface`: Interfaz de chat para clarificación de requisitos.
    - `ArenaView`: Vista comparativa de variantes de prompts.
- **Integración:** Conectado correctamente a los endpoints de FastAPI.

### C. Infraestructura y Despliegue
- **Estado:** ⚠️ Pendiente de Estandarización
- **Situación:** Actualmente requiere ejecución manual de dos terminales (Backend/Frontend).
- **Acción:** Se ha decidido implementar **Docker** como método principal de despliegue para garantizar consistencia entre entornos de desarrollo y producción.

---

## 2. 🎯 Objetivos del Ciclo Actual

El objetivo principal es **profesionalizar el repositorio** para facilitar su adopción, despliegue y colaboración, preparando el terreno para las siguientes fases de lógica compleja (Bucles de Refinamiento y System Prompts).

### Estrategia de Despliegue Definida
Tras evaluar las opciones "Ejecución Local" vs "Docker", se ha optado por un **Enfoque Híbrido**:
1.  **Principal (Usuarios/Demos):** Docker Compose. "Funciona a la primera".
2.  **Secundario (Contribuidores):** Guía detallada de instalación local (Python venv + Node npm).

---

## 3. 📝 Hoja de Ruta (Roadmap) - Q1 2026

### Fase 1: Consolidación y Documentación (Prioridad Alta - Inmediato)
- [x] **Planificación:** Creación de este documento maestro.
- [ ] **Dockerización:**
    - Crear `backend/Dockerfile` (Python 3.11 slim).
    - Crear `frontend/Dockerfile` (Node 18/20 Alpine).
    - Orquestar con `docker-compose.yml`.
- [ ] **Documentación Maestra (`README.md`):**
    - Estructura Bilingüe (Inglés / Español).
    - Diagramas de arquitectura (texto/mermaid).
    - Guías de "Quick Start" y "Developer Setup".

### Fase 2: Experiencia de Usuario (UX) - Refinamiento (Prioridad Media)
- [ ] **Migración a Streaming:**
    - Refactorizar el endpoint de "Refinamiento" (`/workflow/{id}/run`) para utilizar SSE.
    - Actualizar el store de Zustand en el frontend para manejar el streaming de refinamiento igual que la generación inicial.
    - *Impacto:* Elimina la espera "ciega" durante la mejora de prompts.

### Fase 3: Lógica Avanzada - System Prompts (Prioridad Baja)
- [ ] **Soporte de System Prompts:**
    - Habilitar la lógica condicional en `llm_engine.py` para inyectar inputs de prueba de usuario.
    - Adaptar la UI de la Arena para permitir input de usuario dinámico al probar System Prompts.

---

## 4. 📓 Bitácora de Decisiones y Notas

| Fecha | Tipo | Descripción |
| :--- | :--- | :--- |
| **2026-02-16** | 🟢 Decisión | Se aprueba la **Dockerización** completa del proyecto para facilitar el onboarding de nuevos desarrolladores y usuarios. |
| **2026-02-16** | 🟢 Decisión | Se establece que la documentación pública (`README.md`) será **Bilingüe (EN/ES)** para maximizar el alcance del proyecto. |
| **2026-02-16** | ℹ️ Nota | Se identifica la necesidad de migrar el Refinamiento a Streaming para mantener consistencia en la UX. Se agendará para la Fase 2. |
