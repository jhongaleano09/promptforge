# Fase 2: El Cerebro (Definición de Prompts de Agentes)

**Objetivo:** Diseñar la "personalidad" y las instrucciones base de los agentes. Antes de codificar flujos, debemos asegurar que los agentes saben hacer su trabajo individualmente.

## 🛠️ Tareas Técnicas

### 2.1 Estructura de Prompts
- [ ] Crear directorio `backend/app/prompts/`.
- [ ] Definir sistema de plantillas (usando Jinja2 o f-strings) para inyectar variables en los prompts.

### 2.2 Agente Clasificador & Clarificador
*Responsable de entender qué quiere el usuario.*
- [ ] **Prompt "Analista de Requisitos":**
  - Input: Intención vaga del usuario.
  - Output Esperado (JSON):
    - `ambiguities`: Lista de cosas no claras.
    - `questions`: 3-5 preguntas estratégicas para resolver las ambigüedades.
    - `detected_type`: system_prompt | normal | image | deep_research.

### 2.3 Agente Generador (Arquitecto de Variantes)
*Responsable de la creatividad divergente.*
- [ ] **Prompt "Generador Multi-Enfoque":**
  - Input: Requisitos clarificados + Tipo de Prompt.
  - Tarea: Generar 3 variantes distintas.
  - Estrategia variante A: **Conciso/Directo** (Optimizado para tokens).
  - Estrategia variante B: **Chain-of-Thought** (Razonamiento paso a paso).
  - Estrategia variante C: **Rico en Contexto/Few-Shot** (Ejemplos incluidos).
  - Output Esperado (JSON): Lista de objetos `{ id: "A", name: "Directo", content: "..." }`.

### 2.4 Agente Evaluador (El Crítico)
*Responsable del control de calidad.*
- [ ] **Prompt "Juez Imparcial":**
  - Input: Un prompt candidato + Requisitos originales.
  - Tarea: Evaluar del 1 al 10 en: Claridad, Seguridad, Adherencia a Requisitos.
  - Identificar posibles alucinaciones o loopholes.
  - Output Esperado (JSON): `{ score: 8.5, feedback: "...", suggestions: ["..."] }`.

### 2.5 Agente Refinador (El Editor)
*Responsable de pulir.*
- [ ] **Prompt "Editor Senior":**
  - Input: Prompt original + Feedback del Evaluador.
  - Tarea: Reescribir el prompt aplicando las sugerencias sin perder la esencia original.

## ✅ Criterios de Aceptación (DoD)
1.  Tener un script de prueba (`test_agents.py`) que ejecute cada prompt con un input fijo y valide que el LLM devuelve JSON válido.
2.  Los prompts son robustos contra inyección básica (el sistema no se rompe si el usuario pide "ignora tus instrucciones anteriores").

## ❓ Preguntas Clave para el Usuario
1.  **Idioma:** ¿Los agentes deben "pensar" y preguntar en Español siempre, o deben adaptarse al idioma en que escriba el usuario? (Recomendación: Forzar Español para la interfaz/preguntas, pero permitir generar prompts en inglés si el usuario lo pide). RTA/ en la interfaz de usuario debemos considerar un selector de idiomas y para eficiencia tanto de los prompts tanto como delos resultados, se debe tener las respectivas variaciones para cada idioma. iniciar con Ingles/Español.
2.  **Nivel de "Maldad" del Evaluador:** ¿Qué tan estricto quieres que sea el Agente Evaluador? RTA/ **Estricto** debe penaliza fuertemente ambigüedades, simula ser un usuario "tonto" que malinterpreta instrucciones). realizar las notas de lo que considere.
3.  **Variantes Fijas:** ¿Estás de acuerdo con los 3 arquetipos de variantes propuestos (Directo, CoT, Few-Shot) o prefieres otros (ej: uno creativo, uno formal, uno técnico)? RTA/ los propuestos estan bien.
