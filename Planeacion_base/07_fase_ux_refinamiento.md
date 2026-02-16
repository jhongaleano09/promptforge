# 07. Fase de UX: Refinamiento via Streaming

**Objetivo:** Unificar la experiencia de usuario (UX) haciendo que el proceso de "Refinamiento" (mejorar un prompt existente) sea tan fluido y visualmente reactivo como la generación inicial, eliminando esperas estáticas.

## 🧠 Estrategia Técnica
Actualmente, la generación inicial usa **Server-Sent Events (SSE)** para mostrar el texto token a token. Sin embargo, el refinamiento usa una petición HTTP estándar (`POST`) que bloquea la UI hasta que termina.
La estrategia es migrar el endpoint de refinamiento para reutilizar la lógica de streaming del motor de workflow.

---

## 🛠️ Tareas Técnicas Detalladas

### 7.1 Backend: Endpoint de Refinamiento Streaming
Adaptar el API para soportar SSE en la acción de refinamiento.

- [ ] **Nuevo Endpoint Streaming:**
    - Crear `POST /api/workflow/stream/{thread_id}/refine`.
    - Debe aceptar: `selected_variant_id`, `user_feedback`.
    - Debe invocar el grafo de LangGraph pero usando `astream_events` en lugar de `ainvoke`.
    - Debe emitir eventos compatibles con el frontend: `token`, `status`, `update`, `error`.
- [ ] **Lógica de Grafo (LangGraph):**
    - Asegurar que el nodo `refine` (Refinador) sea compatible con streaming de tokens (ya debería serlo si usa `ChatOpenAI` con `streaming=True`).

### 7.2 Frontend: Store Update (Zustand)
Actualizar el gestor de estado para consumir el nuevo endpoint.

- [ ] **Función `refineVariant`:**
    - Reemplazar `fetch` estándar por `fetchEventSource` (Microsoft library).
    - Manejar los eventos de `token` para actualizar la UI en tiempo real (efecto "escribiendo").
    - Manejar eventos de `status` para mostrar "Refinando..." -> "Evaluando...".
- [ ] **Manejo de Estado:**
    - Asegurar que `currentStreamingMessage` se use correctamente para mostrar el progreso del refinamiento, o si son múltiples variantes, cómo se visualiza el streaming de 3 variantes (probablemente secuencial o solo indicador de progreso). *Nota: Si refina 3 variantes, el streaming de texto completo puede ser caótico. Quizás streaming de "pasos" es mejor, o streaming de la "variante principal".*

### 7.3 Frontend: Indicadores Visuales
- [ ] **Feedback de Progreso:**
    - Mostrar qué está haciendo el agente ("Analizando feedback...", "Generando variantes...", "Evaluando...").
    - Deshabilitar controles durante el streaming.

---

## ❓ Preguntas Clave para la Implementación
1.  **Streaming Múltiple:** Al refinar, se generan 3 variantes. ¿Podemos streamear las 3 a la vez?
    *   *Respuesta técnica:* Difícil con una sola conexión SSE estándar sin complicar el protocolo.
    *   *Alternativa:* Streamear solo el *status* ("Generando Variante A...", "Generando Variante B...") y luego enviar el texto completo al final de cada una, O streamear tokens de una en una secuencialmente.
    *   *Decisión:* Para esta fase, priorizar streaming de **Status y Eventos de Progreso**, y actualización final del texto, para evitar complejidad excesiva en el parser del frontend. O si el backend lo soporta, streaming secuencial.
2.  **Persistencia del Feedback:** ¿Dónde se guarda el historial de refinamientos? (En el `PromptState` de LangGraph, ya cubierto por la arquitectura).

---

## ✅ Buenas Prácticas a Seguir
-   **Consistencia:** El formato de los eventos SSE (`data:JSON`) debe ser idéntico al del flujo de inicio.
-   **Error Handling:** Si el stream se corta a la mitad, el frontend debe poder recuperar el último estado válido o mostrar un error claro, no quedarse colgado.
-   **UX:** Siempre permitir al usuario cancelar el refinamiento si tarda demasiado.
