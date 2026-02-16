# 08. Fase de Lógica Avanzada: System Prompts

**Objetivo:** Permitir la creación y evaluación efectiva de **System Prompts**, diferenciándolos de los prompts normales. Un System Prompt no puede evaluarse solo con verlo; requiere un "User Input" de prueba para ver cómo reacciona el modelo.

## 🧠 Estrategia Técnica
Esta fase implementa la lógica condicional en el motor de ejecución (`llm_engine.py`) y en la interfaz de usuario (`ArenaView`), permitiendo inyectar variables de prueba en tiempo real.

---

## 🛠️ Tareas Técnicas Detalladas

### 8.1 Backend: Lógica de Ejecución Condicional
El motor debe saber distinguir si está ejecutando un Prompt Normal (Usuario) o un System Prompt.

- [ ] **Actualización de `llm_engine.py`:**
    - Revisar la función `run_prompt_variant`.
    - **Lógica System Prompt:**
        - Si `prompt_type == "system"`:
            - Validar que existe `input_data["user_test_input"]`.
            - Construir mensaje: `[{"role": "system", "content": variant}, {"role": "user", "content": test_input}]`.
    - **Lógica Normal Prompt:**
        - Si `prompt_type == "normal"`:
            - Construir mensaje: `[{"role": "user", "content": variant}]` (o template renderizado).

### 8.2 Frontend: UI de Testing en Arena
La interfaz debe cambiar cuando el usuario está creando un System Prompt.

- [ ] **Input de Prueba Global:**
    - Agregar un campo de texto `Test Input` en la parte superior de la Arena.
    - Este input es **común** para las 3 variantes.
- [ ] **Botón "Test Run":**
    - Acción: Enviar el `Test Input` al backend (`/arena/execute`).
    - Estado: Mostrar loading en las 3 columnas de variantes simultáneamente.
- [ ] **Visualización de Resultados:**
    - Mostrar la respuesta del modelo (Output) debajo de cada variante.
    - Permitir re-ejecutar con diferente input de prueba sin regenerar las variantes.

### 8.3 Backend: Validación de Inputs
- [ ] **Endpoint `/arena/execute`:**
    - Validar que si `prompt_type="system"`, el campo `input_data.user_test_input` no esté vacío.
    - Retornar error 400 claro si falta el input de prueba.

---

## ❓ Preguntas Clave para la Implementación
1.  **Variables en el System Prompt:** Si el system prompt tiene variables (ej: `{{ role }}`), ¿dónde las define el usuario?
    *   *Respuesta:* Por ahora asumimos system prompts estáticos o que el agente generador ya rellenó las variables. Si queremos variables dinámicas, necesitamos un paso previo de "Rellenar Variables".
    *   *Decisión:* Para esta fase, asumir que las variantes generadas ya tienen el contenido final del system prompt.
2.  **Modelo de Ejecución:** ¿Qué modelo se usa para probar el system prompt?
    *   *Decisión:* El mismo que el usuario configuró en Settings (ej: GPT-4).

---

## ✅ Buenas Prácticas a Seguir
-   **Claridad Visual:** Diferenciar claramente qué es el "Prompt" (instrucción al modelo) y qué es el "Output" (respuesta del modelo ante el input de prueba).
-   **Costos:** Advertir al usuario (quizás un tooltip) que probar 3 variantes con un input largo consume tokens x3.
