# 05. Loops de Refinamiento y System Prompts

**Objetivo:** Cerrar el ciclo de producción. Transformar la herramienta de un generador lineal a un sistema de **mejora continua**. Implementar la capacidad de probar los prompts con inputs reales (Testing), evaluar sus respuestas mediante el mismo modelo (Juez LLM) y refinarlos iterativamente.

## 🧠 Estrategia Técnica

Esta fase introduce la **circularidad** en el flujo de trabajo:
1.  **Testing Real (LiteLLM):** Ejecución de variantes contra modelos reales (APIs compatibles con OpenAI).
2.  **Juez Automático (Self-Correction):** El mismo modelo configurado actúa como crítico de sus propias variantes, recomendando la mejor opción.
3.  **Memoria Cíclica:** LangGraph mantiene un historial de iteraciones para permitir refinamiento y "undo".

---

## 🛠️ Tareas Técnicas Detalladas

### 5.1 Motor de Ejecución (Testing Engine)
Implementar la capa que permite "disparar" los prompts generados.

- [ ] **Servicio de Ejecución (Backend):**
    - Función `run_prompt_variant(variant_id, input_data, llm_config)` usando `LiteLLM`.
    - **Soporte de APIs:** Priorizar OpenAI, OpenRouter, DeepSeek, Z.AI, MiniMax. (Ollama queda preparado arquitectónicamente pero no es la prioridad inmediata).
    - **Inyección de Variables:** Detectar variables (ej: `{{ input_usuario }}`) y solicitar valores antes de ejecutar.
- [ ] **Control de Costos (UI):**
    - **Advertencia:** Mostrar notificación/modal antes de ejecutar: *"Esta acción ejecutará X llamadas al modelo. Consumo estimado de tokens."*
    - Confirmación explícita del usuario requerida.

### 5.2 Lógica Especial: System Prompts
Tratamiento diferenciado cuando `prompt_type == 'system'`.

- [ ] **UI de Input de Prueba:**
    - Agregar campo de texto global "User Input (Prueba)" en la Arena.
    - Este input se aplica simultáneamente a las 3 variantes.
- [ ] **Construcción del Payload:**
    - Payload: `messages = [{role: "system", content: variante_X}, {role: "user", content: input_prueba}]`.
- [ ] **Visualización Paralela:**
    - Mostrar las 3 respuestas del modelo (Output A, B, C) en columnas adyacentes para comparación directa.

### 5.3 El Agente Juez (Auto-Eval)
Un agente que analiza los outputs y ofrece un veredicto.

- [ ] **Configuración del Juez:**
    - Utilizar el **mismo modelo y API Key** configurados por el usuario (sin coste extra de modelos externos).
- [ ] **Prompt del Juez:**
    - *Rol:* Crítico experto.
    - *Input:* Intención original + Test Input + 3 Outputs generados.
    - *Output:* JSON con `{ winner: "A", reason: "Más concisa y segura", highlights: ["Creativo", "Formal"] }`.
- [ ] **Integración en Arena:**
    - Badge "Recomendado por la IA" sobre la variante ganadora.
    - Notas cortas: "Destaca en: X, Y".

### 5.4 Ciclo de Refinamiento (LangGraph Loop)
Modificar el grafo para permitir volver atrás y mejorar.

- [ ] **Actualización de `PromptState`:**
    - Agregar campo `history: List[PromptStateSnapshot]`.
    - **Límite:** Mantener las últimas **100 iteraciones** (FIFO). Las más antiguas se eliminan.
- [ ] **Nodo Refinador:**
    - *Input:* Variante seleccionada + Feedback del usuario (ej: "Hazlo más corto").
    - *Acción:* Generar 3 nuevas versiones (V2.A, V2.B, V2.C) basadas en la ganadora y el feedback.
    - *Combinación:* Permitir al usuario seleccionar partes de A y B (manual) o pedir al modelo que las fusione.

---

## 💾 Modelo de Datos (Actualizaciones)

Se expande el esquema de `PromptState` para soportar ejecuciones e historia.

```python
class PromptState(TypedDict):
    # ... campos existentes ...
    iteration: int
    history: List[dict] # Snapshots de estados anteriores (Max 100)
    
    # Resultados del Testing
    test_inputs: dict # { 'variable_1': 'valor' }
    test_outputs: dict # { 'A': 'Respuesta modelo...', 'B': ... }
    
    # Evaluación
    judge_result: dict # { 'winner': 'A', 'reason': '...', 'tags': [...] }
```

---

## 🔌 API Endpoints Nuevos

- `POST /api/arena/execute`: Recibe `variant_ids` y `test_input`. Retorna outputs de LLM.
- `POST /api/arena/judge`: Ejecuta el Agente Juez sobre los outputs actuales.
- `POST /api/workflow/{thread_id}/refine`: Envía feedback y selección para iniciar nueva iteración.
- `POST /api/workflow/{thread_id}/history`: Obtiene la lista de versiones anteriores.
- `POST /api/workflow/{thread_id}/rollback`: Restaura un estado anterior.

---

## ✅ Criterios de Aceptación (DoD)

1.  **Testing Funcional:** El usuario puede ingresar un input, confirmar la advertencia de costos, y ver las 3 respuestas del LLM.
2.  **Juez Inteligente:** El sistema marca automáticamente la mejor respuesta usando el mismo modelo configurado.
3.  **Refinamiento Efectivo:** El usuario puede pedir cambios ("Más formal") y obtener versiones nuevas coherentes.
4.  **Gestión de Memoria:** El historial permite "undo" y respeta el límite de 100 iteraciones.
5.  **Multi-API:** Funciona correctamente con proveedores compatibles con OpenAI (OpenRouter, DeepSeek, etc.).

---

> **Decisiones de Diseño:**
> 1. **Juez:** Usa el mismo modelo del usuario (no un modelo externo fijo).
> 2. **APIs:** Prioridad a APIs estándar sobre ejecución local (Ollama) en esta fase.
> 3. **Límite:** Historial rotativo de 100 pasos.
