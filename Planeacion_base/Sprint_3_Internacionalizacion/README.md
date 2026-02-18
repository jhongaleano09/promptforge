# Sprint 3: Internacionalización (i18n)

## Descripción General
Implementar sistema robusto de internacionalización para soportar múltiples idiomas con cambio dinámico, persistencia de preferencias, y cobertura completa de toda la UI.

## Duración Estimada
**5-7 días**

## Prioridad
🟡 **MEDIA-ALTA** - Importante para alcance global

## Prerequisitos
- ✅ Sprint 2 completado (preferencias de usuario)
- ✅ Sistema de preferencias persistente funcionando

## Objetivos

1. Implementar sistema i18n completo (react-i18next o next-intl)
2. Traducir toda la interfaz a ES/EN (mínimo)
3. Selector de idioma en Header/Settings
4. Persistencia de idioma seleccionado
5. Soporte para fechas, números, y formatos localizados

## Estructura de Archivos

```
Sprint_3_Internacionalizacion/
├── README.md
├── 3.1_implementacion_i18n.md          # Setup de react-i18next
├── 3.2_traduccion_completa.md          # Traducir toda la UI
├── 3.3_selector_idioma.md              # Componente selector
├── 3.4_persistencia_idioma.md          # Guardar preferencia
└── 3.5_formatos_localizados.md         # Fechas, números, moneda
```

## Tareas

### 3.1 - Implementación de i18n 🔴 CRÍTICA (2 días)
Setup de react-i18next, estructura de archivos de traducción, detección de idioma

### 3.2 - Traducción Completa 🟠 ALTA (2 días)
Traducir TODA la interfaz, identificar strings hardcoded, crear keys estructuradas

### 3.3 - Selector de Idioma 🟡 MEDIA (1 día)
Componente para cambiar idioma dinámicamente, integrar en Header

### 3.4 - Persistencia de Idioma 🟡 MEDIA (0.5 días)
Guardar idioma en user_preferences, cargar al inicio

### 3.5 - Formatos Localizados 🟢 BAJA (0.5-1 día)
Formateo de fechas, números, moneda según locale

## Resultado Esperado

Usuario puede cambiar entre español e inglés dinámicamente, cambio persiste entre sesiones, toda la UI se traduce correctamente.

⚠️ Actualizar PROGRESS.md después de cada tarea
