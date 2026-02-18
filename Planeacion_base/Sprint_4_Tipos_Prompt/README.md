# Sprint 4: Tipos de Prompt Modulares

## Descripción General
Implementar sistema de tipos de prompt modulares (System Prompt, Image Prompt, Additional Prompts) con workflows específicos para cada tipo.

## Duración Estimada
**4-5 días**

## Prioridad
🟡 **MEDIA** - Feature de valor agregado

## Prerequisitos
- ✅ Sprint 1-2 completados
- ✅ Sistema de providers funcionando

## Objetivos

1. Crear workflows específicos por tipo de prompt
2. UI para seleccionar tipo de prompt
3. Generación especializada según tipo
4. Templates predefinidos por tipo

## Estructura de Archivos

```
Sprint_4_Tipos_Prompt/
├── README.md
├── 4.1_workflows_especializados.md     # Crear graphs por tipo
├── 4.2_selector_tipo_prompt.md         # UI para seleccionar tipo
├── 4.3_templates_predefinidos.md       # Templates por tipo
└── 4.4_generacion_especializada.md     # Lógica específica por tipo
```

## Tareas

### 4.1 - Workflows Especializados 🔴 CRÍTICA (2 días)
Crear LangGraph workflows para cada tipo: system_prompt_graph, image_prompt_graph, additional_prompt_graph

### 4.2 - Selector de Tipo 🟠 ALTA (1 día)
UI para seleccionar tipo de prompt antes de enviar

### 4.3 - Templates Predefinidos 🟡 MEDIA (1 día)
Biblioteca de templates para cada tipo

### 4.4 - Generación Especializada 🟡 MEDIA (1 día)
Lógica de generación específica según tipo de prompt

## Resultado Esperado

Usuario puede seleccionar entre tipos de prompt, cada tipo tiene workflow y templates especializados.

⚠️ Actualizar PROGRESS.md después de cada tarea
