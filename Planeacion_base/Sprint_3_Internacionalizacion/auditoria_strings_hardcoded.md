# Auditoría de Strings Hardcoded - Sprint 3

**Fecha:** 18 de Febrero de 2026  
**Versión:** 1.0  
**Estado:** ✅ COMPLETO  
**Objetivo:** Documentar todos los strings hardcoded que necesitan internacionalización

---

## 📊 Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Componentes auditados | 13 |
| Strings hardcoded totales | ~100+ |
| Componentes completamente internacionalizados | 7 |
| Componentes pendientes de internacionalización | 6 |
| Stores con strings hardcoded | 2 |

---

## ✅ Componentes Completamente Internacionalizados

Estos componentes ya usan el hook `useLanguage()` y no tienen strings hardcoded:

1. `frontend/src/app/page.tsx` - Página principal
2. `frontend/src/components/prompt-type-selector.tsx` - Selector de tipo de prompt
3. `frontend/src/components/arena/PromptCard.tsx` - Card de variante
4. `frontend/src/components/arena/ArenaView.tsx` - Vista de arena
5. `frontend/src/components/arena/ChatInterface.tsx` - Chat de clarificación
6. `frontend/src/components/onboarding-form.tsx` - Formulario de onboarding
7. `frontend/src/components/language-switcher.tsx` - Selector de idioma

---

## 🟨 Componentes Pendientes de Internacionalización

### Prioridad ALTA

#### 1. `frontend/src/components/api-keys-manager.tsx`

**Líneas con strings hardcoded:** ~30 strings en inglés

**Strings identificados:**
```typescript
// Línea ~297
"API Keys Management"

// Línea ~298
"Manage your LLM provider API keys"

// Línea ~306
"Add New Key"

// Línea ~318
"Configuration Required"

// Línea ~331
"No API keys configured yet"

// Línea ~334
"Add Your First Key"

// Línea ~352
"Active"

// Línea ~370
"Activate"

// Línea ~414
"Add New API Key"

// Línea ~415
"Add a new API key for your LLM provider"

// Línea ~419, 425, 426, 427
"Provider"

// Línea ~432
"API Key"

// Línea ~436
"Enter your API key"

// Línea ~452
"Default Model"

// Línea ~528
"Add Key"

// Línea ~520
"Validating..."

// Línea ~525
"Retrying in {countdown}s..."

// Línea ~510
"Cancel"

// Línea ~542
"Delete API Key?"

// Línea ~625
"Delete"

// Línea ~617
"Deleting..."

// Línea ~555
"Warning"

// Línea ~557
"This is your only API key. You'll need to add a new one before using PromptForge."

// Y múltiples mensajes de error adicionales
```

**Acción requerida:** Reemplazar todos los strings con `t('api_keys.xxx')`

---

#### 2. `frontend/src/components/settings/advanced-settings.tsx`

**Líneas con strings hardcoded:** ~15 strings en inglés

**Strings identificados:**
```typescript
// Línea ~65
"Advanced Settings"

// Línea ~66-67
"Configure LLM provider, models, and generation parameters"

// Línea ~73
"Default Provider"

// Línea ~87
"Default Model"

// Línea ~114
"Temperature"

// Línea ~126
"Higher values make output more random. Lower values make it more focused."

// Línea ~132
"Max Tokens"

// Línea ~144
"Maximum number of tokens to generate. Higher values allow longer responses."

// Línea ~150
"Top P"

// Línea ~162
"Only sample from the top percentage of most likely tokens."

// Línea ~187
"Save Changes"

// Línea ~177
"Saving..."

// Línea ~182
"Saved"
```

**Acción requerida:** Reemplazar todos los strings con `t('advanced_settings.xxx')`

---

#### 3. `frontend/src/components/settings/preferences-form.tsx`

**Líneas con strings hardcoded:** ~20 strings en inglés

**Strings identificados:**
```typescript
// Línea ~75
"General Preferences"

// Línea ~76-77
"Configure your personal preferences and appearance"

// Línea ~83
"Your Name"

// Línea ~85
"Enter your name"

// Línea ~93
"Country"

// Línea ~95
"Enter your country"

// Línea ~105
"Language"

// Línea ~111
"Auto-save Preferences"

// Línea ~113
"Automatically save changes as you type"

// Línea ~135
"Theme"

// Línea ~137
"Light mode" / "Dark mode"

// Línea ~153
"Save Changes"

// Línea ~156
"Last saved:"

// Línea ~178
"Save"

// Línea ~168
"Saving..."

// Línea ~173
"Saved"
```

**Acción requerida:** Reemplazar todos los strings con `t('preferences_form.xxx')`

---

#### 4. `frontend/src/app/settings/page.tsx`

**Líneas con strings hardcoded:** ~4 strings en inglés

**Strings identificados:**
```typescript
// Línea ~12
"Settings"

// Línea ~16
"Providers"

// Línea ~17
"General"

// Línea ~18
"Advanced"
```

**Acción requerida:** Reemplazar todos los strings con `t('settings_page.xxx')`

---

#### 5. `frontend/src/components/provider-selector.tsx`

**Líneas con strings hardcoded:** ~8 strings en inglés

**Strings identificados:**
```typescript
// Línea ~43
"Loading providers..."

// Línea ~48
"No active providers configured. Please go to Settings."

// Línea ~56
"Using"

// Línea ~63
"Provider:"

// Línea ~71-73
"OpenAI", "Anthropic", "Ollama"
```

**Acción requerida:** Reemplazar todos los strings con `t('provider_selector.xxx')`

---

### Prioridad MEDIA

#### 6. `frontend/src/components/arena/EvaluationChart.tsx`

**Líneas con strings hardcoded:** ~6 strings en inglés

**Strings identificados:**
```typescript
// Línea ~21
"No evaluation data yet"

// Línea ~48
"Evaluation Radar"

// Línea ~27-29
"Clarity", "Safety", "Completeness"

// Línea ~33, 58-59
"Variant ", "Var "
```

**Acción requerida:** Reemplazar todos los strings con `t('evaluation_chart.xxx')`

---

#### 7. `frontend/src/app/layout.tsx`

**Líneas con strings hardcoded:** ~3 strings en inglés

**Strings identificados:**
```typescript
// Línea ~18 (metadata title)
"PromptForge"

// Línea ~19 (metadata description)
"Professional Prompt Engineering Tool"

// Línea ~28 (lang attribute)
lang="en"
```

**Acción requerida:** Internacionalizar metadata y hacer dinámico el atributo lang

---

## 🔴 Stores con Strings Hardcoded

### 1. `frontend/src/store/workflowStore.ts`

**Líneas con strings hardcoded:** ~10 strings (mixto inglés/español)

**Strings identificados:**
```typescript
// Línea ~74 (español)
"No hay ninguna API key activa configurada"

// Línea ~76 (español)
"Configuración requerida: No hay API key activa"

// Línea ~81 (inglés)
"Failed to validate configuration"

// Línea ~162 (inglés)
"Connection lost"

// Línea ~167 (inglés)
"Failed to start workflow"

// Línea ~232 (inglés)
"Failed to submit answer"

// Línea ~259 (inglés)
"Test execution failed"

// Línea ~288 (inglés)
"Refinement failed"
```

**Acción requerida:** Extraer strings de error a componentes que usan `useLanguage()`

---

### 2. `frontend/src/store/preferenceStore.ts`

**Líneas con strings hardcoded:** ~4 strings en inglés

**Strings identificados:**
```typescript
// Línea ~46
"Failed to load preferences"

// Línea ~55
"Error loading preferences:"

// Línea ~82
"Failed to update preferences"

// Línea ~88
"Error updating preferences:"
```

**Acción requerida:** Extraer strings de error a componentes que usan `useLanguage()`

---

## 📚 Estructura de Namespaces Sugerida

Basado en los strings identificados, se sugiere la siguiente estructura de namespaces:

```json
{
  "settings_page": { ... },
  "advanced_settings": { ... },
  "preferences_form": { ... },
  "provider_selector": { ... },
  "evaluation_chart": { ... },
  "errors": { ... }
}
```

---

## 📊 Tabla de Conversión de Strings

| Archivo | Strings totales | Prioridad | Estimación de tiempo |
|---------|----------------|-----------|---------------------|
| api-keys-manager.tsx | ~30 | ALTA | 2 horas |
| advanced-settings.tsx | ~15 | ALTA | 1.5 horas |
| preferences-form.tsx | ~20 | ALTA | 1.5 horas |
| settings/page.tsx | ~4 | ALTA | 1 hora |
| provider-selector.tsx | ~8 | ALTA | 1 hora |
| EvaluationChart.tsx | ~6 | MEDIA | 1.5 horas |
| layout.tsx | ~3 | MEDIA | 1 hora |
| workflowStore.ts | ~10 | ALTA | 2 horas |
| preferenceStore.ts | ~4 | MEDIA | 1 hora |
| **TOTAL** | **~100** | - | **12.5 horas** |

---

## 🎯 Orden de Implementación Recomendado

1. **Fase 2:** Ampliar archivos de traducción (1-2 horas)
2. **Fase 3.1:** api-keys-manager.tsx (2 horas)
3. **Fase 3.2:** advanced-settings.tsx (1.5 horas)
4. **Fase 3.3:** preferences-form.tsx (1.5 horas)
5. **Fase 3.4:** settings/page.tsx (1 hora)
6. **Fase 3.5:** provider-selector.tsx (1 hora)
7. **Fase 3.6:** EvaluationChart.tsx (1.5 horas)
8. **Fase 3.7:** layout.tsx (1 hora)
9. **Fase 4.1:** workflowStore.ts (2 horas)
10. **Fase 4.2:** preferenceStore.ts (1 hora)

**Tiempo total estimado:** 13.5-14.5 horas

---

## ✅ Criterios de Finalización

- [ ] 0 strings hardcoded en componentes UI visibles
- [ ] 0 strings hardcoded en stores
- [ ] Todos los componentes usan `useLanguage()`
- [ ] Claves de traducción agregadas a spanish.json
- [ ] Claves de traducción agregadas a english.json
- [ ] No hay mezcla de idiomas en el código
- [ ] Testing completo en ambos idiomas

---

**Autor:** OpenCode AI  
**Última actualización:** 18 de Febrero de 2026
