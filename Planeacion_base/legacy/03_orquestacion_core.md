# Fase 3: Orquestación Core (LangGraph)

**Objetivo:** Conectar las piezas sueltas (Agentes) en una línea de producción coherente. Aquí es donde "PromptForge" cobra vida como sistema.

## 🛠️ Tareas Técnicas

### 3.1 Estado del Grafo (State Management)
- [ ] Definir `PromptState` (TypedDict):
  ```python
  class PromptState(TypedDict):
      user_input: str
      requirements: dict
      clarification_history: list[BaseMessage]
      generated_variants: list[dict] # [ {id: 'A', content: '...'}, ... ]
      evaluations: dict # { 'A': {score: 9, ...} }
      selected_variant: str
  ```

### 3.2 Implementación de Nodos
- [ ] **Nodo Clarificación:**
  - Lógica: ¿Faltan datos? -> Generar Pregunta -> Pausar (Esperar input humano).
  - Si datos completos -> Pasar a Generación.
- [ ] **Nodo Generación (Fan-Out):**
  - Ejecutar 3 llamadas al LLM en paralelo (asyncio.gather) para velocidad.
  - Cada llamada usa una "persona" distinta (Directo, CoT, Few-Shot).
- [ ] **Nodo Evaluación:**
  - Recibe las 3 variantes.
  - Ejecuta el Agente Evaluador para cada una.
  - Agrega scores al estado.

### 3.3 API Endpoints para el Grafo
- [ ] `POST /api/workflow/start`: Inicia un nuevo hilo. Retorna `thread_id`.
- [ ] `POST /api/workflow/{thread_id}/answer`: Para responder a las preguntas de clarificación.
- [ ] `GET /api/workflow/{thread_id}/state`: Polling para ver si ya terminó la generación.

## ✅ Criterios de Aceptación (DoD)
1.  Poder iniciar un flujo con "Ayúdame a crear un prompt para un chatbot de soporte".
2.  Que el sistema pause y pregunte "¿Para qué industria?".
3.  Al responder "Zapatos", el sistema reanude y genere 3 variantes JSON.
4.  Tiempos de respuesta aceptables (Generación paralela funcionando).

## ❓ Preguntas Clave para el Usuario
1.  **Persistencia del Chat:** Si el usuario cierra el navegador a mitad de la entrevista de clarificación, ¿queremos recuperar esa sesión al volver (persistencia de threads en BD) o empezamos de cero? RTA/ Mantener las repuestas, ser persistentes en este nivel.
2.  **Límite de Preguntas:** Para evitar que el Agente Clarificador entre en un bucle infinito de preguntas, ¿ponemos un límite duro (ej: máximo 5 rondas de preguntas) antes de forzar la generación? RTA/ El mismo agente tiene que realizar sugerencias a las respuestas de tipo multiple para que el seleccione la mas apropiada para el, adicional tener una opcion para que escriba una respuesta difernete por el o donde incorpore parte de las respuestas que el considere. incluyendo hacer combinaciones sobre posibles respuestas preestablecidas por parte del agente, es decir que pueda hacer referncia a A y B







