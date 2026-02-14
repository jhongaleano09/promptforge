# Fase 5: Loops de Refinamiento y System Prompts

**Objetivo:** Cerrar el ciclo. Implementar la capacidad de probar realmente los prompts y mejorarlos basándose en resultados reales, no solo teóricos.

## 🛠️ Tareas Técnicas

### 5.1 Testing de Prompts Normales
- [ ] Botón "Ejecutar Test" en cada tarjeta de variante.
- [ ] Al hacer click, el backend ejecuta ese prompt contra el LLM configurado.
- [ ] Mostrar el Output generado debajo del Prompt.

### 5.2 Lógica Especial: System Prompts
- [ ] Detectar si estamos trabajando en un System Prompt.
- [ ] UI: Mostrar campo "Input de Prueba del Usuario" (Global para las 3 variantes).
- [ ] Ejecución: Enviar `Messages = [{role: system, content: variante_X}, {role: user, content: input_prueba}]`.
- [ ] Mostrar las 3 respuestas del asistente en paralelo.

### 5.3 El Ciclo de Refinamiento (The Loop)
- [ ] UI de Feedback:
  - Input de texto: "¿Qué no te gustó de estos resultados?".
  - Selección: El usuario puede marcar una variante como "La mejor base".
- [ ] **Re-roll del Grafo:**
  - Enviar el feedback + el prompt seleccionado de vuelta al nodo **Refinador**.
  - Generar nuevas versiones (V2.A, V2.B, V2.C).
  - Historial de versiones (Poder volver atrás).

## ✅ Criterios de Aceptación (DoD)
1.  El usuario puede probar sus System Prompts con inputs reales.
2.  Si el usuario dice "La respuesta es muy larga", el sistema genera nuevas versiones más cortas.
3.  Se puede ver el historial de cambios (Iteración 1 -> Iteración 2).

## ❓ Preguntas Clave para el Usuario
1.  **Costos en Testing:** Ejecutar 3 variantes con inputs largos consume tokens. ¿Ponemos una advertencia/confirmación antes de ejecutar los tests, o asumimos que el usuario sabe lo que hace?
2.  **Límite de Iteraciones:** ¿Guardamos todo el historial de versiones (infinito) o solo las últimas X para no saturar la memoria/BD?
3.  **Comparación de Outputs:** En System Prompts, ¿queremos usar un "LLM Juez" que nos diga cuál respuesta fue mejor (Auto-Eval), o dejamos que solo el humano decida? (Auto-Eval aumenta costos pero ayuda a decidir).
