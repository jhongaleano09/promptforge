# Fase 4: La Arena (Frontend & UX)

**Objetivo:** Crear la interfaz visual donde el usuario interactúa con los prompts. Debe sentirse profesional, rápido y claro.

## 🛠️ Tareas Técnicas

### 4.1 Componentes UI Base
- [ ] **Chat Interface:** Para la fase de clarificación (Estilo WhatsApp/ChatGPT).
- [ ] **PromptCard Component:** Tarjeta que muestra:
  - Título (Variante A).
  - Contenido del Prompt (con sintaxis highlighting).
  - Badges de Score (Evaluación).
  - Botones: "Copiar", "Editar", "Probar".

### 4.2 Vista de "Arena" (Comparación)
- [ ] Layout de 3 Columnas (Responsive: pasa a carrusel en móvil).
- [ ] **Diff Viewer:** (Opcional para V2) Mostrar diferencias entre iteraciones.
- [ ] Visualización de Scores:
  - Gráfico de radar o barras simples para mostrar "Claridad", "Seguridad", etc.

### 4.3 Conexión Real-Time
- [ ] Implementar **Streaming** de texto. No esperar a que el prompt esté 100% generado para mostrarlo. Ver letra por letra aparecer genera percepción de velocidad.
- [ ] Manejo de estados de carga granular ("Generando Variante A...", "Evaluando Variante B...").

## ✅ Criterios de Aceptación (DoD)
1.  El usuario ve las preguntas del agente clarificador y puede responder.
2.  Al finalizar la clarificación, la pantalla se transforma en la "Arena" de 3 columnas.
3.  Los prompts se ven formateados (Markdown support).
4.  Los scores de evaluación son visibles y fáciles de entender.

## ❓ Preguntas Clave para el Usuario
1.  **Edición Manual:** Si el usuario edita un prompt manualmente en la Arena, ¿se pierde el score de evaluación anterior (ya que el texto cambió) y se fuerza una re-evaluación, o simplemente se marca como "Editado"? RTA/ En caso de que el usuario edite un prompt desde la Interfaz de usuario, se debe mantener el score de la evaluacion anterior asi cambiara el prompt, no seria necesaria una reevaluacion del mismo, se marcara como editado y se procede con el flujo.
2.  **Exportación:** ¿Qué formatos son prioritarios para el botón "Exportar"? RTA/ habilitar una opion de copiar y habilitar la funcion de exportar en texto plano. asi en caso de ser un formato complicado asi el mismo sea un JSON o un .md desde el .txt les sera facil de manipular al usuario. 
3.  **Tema Visual:** ¿Preferencia por Dark Mode por defecto (común en herramientas de dev) o Light Mode? RTA/ Dark Mode inicialmente, pero puede habilitar el swich botton para tener ambas formas, habilita el swich mode. 
