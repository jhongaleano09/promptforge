# 02. Roadmap de Sprints - PromptForge

**Fecha de Creación:** 17 de Febrero de 2026  
**Versión del Documento:** 1.0  
**Estado:** ✅ ACTIVO  
**Duración Total Estimada:** 19-27 días (~4-6 semanas)

---

## 📋 Resumen Ejecutivo

Este documento define la hoja de ruta de desarrollo de PromptForge organizada en **5 Sprints** incrementales. Cada Sprint tiene objetivos claros, tareas bien definidas y criterios de éxito medibles.

**Filosofía de Desarrollo:**
- ✅ **Iterativo e Incremental:** Cada Sprint entrega valor funcional
- ✅ **Defensa en Profundidad:** Correcciones en múltiples capas (backend, frontend, UX)
- ✅ **Calidad sobre Velocidad:** Mejor un Sprint completo que múltiples incompletos
- ✅ **Documentación Continua:** Actualizar PROGRESS.md en cada tarea completada

---

## 🗓️ Cronograma General

| Sprint | Nombre | Prioridad | Duración | Tareas | Estado |
|--------|--------|-----------|----------|--------|--------|
| **Sprint 1** | Fundamentos y Corrección de Bugs | 🔴 CRÍTICA | 3-5 días | 5 | ⏳ Pendiente |
| **Sprint 2** | Gestión de Configuración | 🟠 ALTA | 4-6 días | 5 | ⏳ Pendiente |
| **Sprint 3** | Internacionalización | 🟡 MEDIA-ALTA | 5-7 días | 5 | ⏳ Pendiente |
| **Sprint 4** | Tipos de Prompt Modulares | 🟡 MEDIA | 4-5 días | 4 | ⏳ Pendiente |
| **Sprint 5** | Optimización y Deployment | 🟢 BAJA-MEDIA | 3-4 días | 5 | ⏳ Pendiente |
| **TOTAL** | - | - | **19-27 días** | **24 tareas** | - |

---

## 🎯 Sprint 1: Fundamentos y Corrección de Bugs

**Duración:** 3-5 días  
**Prioridad:** 🔴 CRÍTICA  
**Objetivo:** Estabilizar la aplicación corrigiendo bugs críticos y mejorando la navegación básica

### **Tareas:**

1. **1.1 - Evaluación de Arquitectura** (4 horas)
   - Documentar estructura completa del proyecto
   - Mapear dependencias entre componentes
   - Identificar áreas de mejora
   - **Entregable:** Documento de arquitectura actualizado

2. **1.2 - Análisis de Logs y Errores** (3 horas)
   - Revisar backend.log y frontend.log
   - Clasificar errores por severidad
   - Crear plan de corrección
   - **Entregable:** Reporte de errores con plan de acción

3. **1.3 - Bug Crítico: Respuesta Vacía del Asistente** (6-8 horas) 🔥
   - Corregir mismatch entre `messages` y `clarification_dialogue`
   - Implementar 3 capas de fixes (backend, API, frontend)
   - Testing completo del flujo de clarificación
   - **Entregable:** Flujo de clarificación funcional end-to-end

4. **1.4 - Navegación: Botón Home** (3-4 horas)
   - Agregar botón "Volver al Inicio" en settings
   - Implementar header global con navegación
   - Mantener estado al navegar
   - **Entregable:** Navegación consistente entre vistas

5. **1.5 - Mejoras UX Básico** (4-5 horas)
   - Corregir "Translation missing: loading"
   - Agregar spinners de carga apropiados
   - Corregir Fast Refresh errors
   - Eliminar warnings menores
   - **Entregable:** Experiencia de usuario pulida

### **Criterios de Éxito del Sprint 1:**
- ✅ Bug de respuesta vacía completamente resuelto
- ✅ Usuario puede navegar fluidamente entre home y settings
- ✅ No hay keys de traducción faltantes
- ✅ Logs limpios sin warnings críticos
- ✅ Fast Refresh funciona sin recargas completas

---

## 🔧 Sprint 2: Gestión de Configuración

**Duración:** 4-6 días  
**Prioridad:** 🟠 ALTA  
**Objetivo:** Sistema robusto de gestión de API keys y preferencias de usuario

### **Tareas:**

1. **2.1 - Tabla user_preferences** (4-5 horas)
   - Validar modelo `UserPreferences` existente
   - Agregar campos adicionales si necesarios
   - Endpoints GET/PUT `/api/user/preferences`
   - **Entregable:** Sistema de preferencias funcional

2. **2.2 - API Keys Multiproveedor** (6-8 horas)
   - Validar tabla `ApiKey` multi-proveedor
   - Implementar límite de 3 keys por proveedor
   - Validación real con servicios LLM
   - Una key activa por proveedor
   - **Entregable:** Gestión completa de API keys backend

3. **2.3 - UI API Keys Manager** (8-10 horas)
   - Componente visual para gestión de keys
   - Lista, agregar, eliminar, activar keys
   - Validación en tiempo real
   - Confirmación de eliminación
   - **Entregable:** UI completa de gestión de keys

4. **2.4 - Validación de Configuración** (3-4 horas)
   - Endpoint `/api/settings/validate-active`
   - Verificar key activa al inicio de workflow
   - Mensajes instructivos claros
   - **Entregable:** Validación automática de configuración

5. **2.5 - Integración con Settings** (4-5 horas)
   - Página `/settings` completa y funcional
   - Botón de acceso desde header
   - Persistencia de cambios
   - Sincronización con workflow
   - **Entregable:** Settings page production-ready

### **Criterios de Éxito del Sprint 2:**
- ✅ Usuario puede gestionar múltiples API keys
- ✅ Sistema valida configuración antes de workflow
- ✅ UI intuitiva para gestión de keys
- ✅ Persistencia correcta de preferencias
- ✅ Mensajes claros si falta configuración

---

## 🌍 Sprint 3: Internacionalización

**Duración:** 5-7 días  
**Prioridad:** 🟡 MEDIA-ALTA  
**Objetivo:** Soporte completo español/inglés en UI y agentes

### **Tareas:**

1. **3.1 - Templates Bilingües** (6-8 horas)
   - Crear `backend/app/prompts/i18n_templates.py`
   - Templates ES/EN para todos los nodos
   - Función `get_templates(language)`
   - Validación de integridad
   - **Entregable:** Sistema de templates i18n completo

2. **3.2 - Backend i18n** (5-6 horas)
   - Campo `language` en `PromptState`
   - Actualizar nodos para usar templates dinámicos
   - Endpoints `/api/user/language` GET/PUT
   - **Entregable:** Backend multiidioma funcional

3. **3.3 - Frontend Context i18n** (6-7 horas)
   - `LanguageContext.tsx` completo
   - Hook `useLanguage()`
   - Carga de archivos JSON
   - Persistencia localStorage + backend
   - **Entregable:** Sistema i18n frontend completo

4. **3.4 - Traducciones UI** (8-10 horas)
   - Completar `public/i18n/spanish.json`
   - Completar `public/i18n/english.json`
   - Migrar todos los textos de UI
   - Componente `LanguageSwitcher`
   - **Entregable:** UI completamente traducida

5. **3.5 - Testing i18n** (4-5 horas)
   - Testing workflow en español
   - Testing workflow en inglés
   - Verificar persistencia de preferencia
   - Edge cases y fallbacks
   - **Entregable:** i18n completamente testeado

### **Criterios de Éxito del Sprint 3:**
- ✅ UI completamente traducida en ES/EN
- ✅ Agentes responden en idioma seleccionado
- ✅ Preferencia de idioma persiste correctamente
- ✅ Switching de idioma en tiempo real funciona
- ✅ Sin keys de traducción faltantes

---

## 🎨 Sprint 4: Tipos de Prompt Modulares

**Duración:** 4-5 días  
**Prioridad:** 🟡 MEDIA  
**Objetivo:** Soporte para múltiples tipos de prompt con workflows específicos

### **Tareas:**

1. **4.1 - Factory Pattern** (5-6 horas)
   - Validar `workflow_factory.py` existente
   - Enum `PromptType` completo
   - Factory retorna workflow según tipo
   - Configuración por tipo
   - **Entregable:** Factory pattern funcional

2. **4.2 - Workflows Modulares** (10-12 horas)
   - Workflow BASIC (ya funcional)
   - Workflow SYSTEM (implementar)
   - Workflow IMAGE (implementar)
   - Workflow ADDITIONAL (implementar)
   - **Entregable:** 4 workflows completos y funcionales

3. **4.3 - UI Selector de Tipos** (6-8 horas)
   - Componente `PromptTypeSelector`
   - Cards visuales para cada tipo
   - Descripciones claras
   - Integración en página principal
   - **Entregable:** Selector de tipos intuitivo

4. **4.4 - Testing de Tipos** (4-5 horas)
   - Validar cada tipo de prompt
   - Testing de switching entre tipos
   - Verificar persistencia
   - Documentar casos de uso
   - **Entregable:** Workflows modulares testeados

### **Criterios de Éxito del Sprint 4:**
- ✅ 4 tipos de prompt funcionales
- ✅ Usuario puede seleccionar tipo fácilmente
- ✅ Workflows específicos para cada tipo
- ✅ Switching entre tipos sin errores
- ✅ Casos de uso documentados

---

## 🚀 Sprint 5: Optimización y Deployment

**Duración:** 3-4 días  
**Prioridad:** 🟢 BAJA-MEDIA  
**Objetivo:** Pulir, optimizar y preparar para producción

### **Tareas:**

1. **5.1 - Tarjeta de Contexto** (4-5 horas) 📊
   - Componente visual al lado derecho
   - Mostrar: Tokens, Modelo, Provider
   - Actualización en tiempo real
   - UI minimalista
   - **Entregable:** Tarjeta de contexto funcional

2. **5.2 - Dockerización** (5-6 horas)
   - Validar Dockerfiles existentes
   - Actualizar docker-compose.yml
   - Testing de containers
   - Documentación de deployment
   - **Entregable:** Deployment dockerizado funcional

3. **5.3 - Documentación README** (6-8 horas)
   - README.md completo y actualizado
   - Screenshots o GIFs
   - Guías de instalación y uso
   - Troubleshooting
   - **Entregable:** Documentación production-ready

4. **5.4 - Testing E2E** (6-8 horas)
   - Tests end-to-end del flujo completo
   - Testing de regresión
   - Performance testing
   - Security audit básico
   - **Entregable:** Suite de tests completa

5. **5.5 - Mejoras de Performance** (4-5 horas)
   - Optimización de queries DB
   - Caching de traducciones
   - Lazy loading de componentes
   - Minificación de bundles
   - **Entregable:** Performance optimizado

### **Criterios de Éxito del Sprint 5:**
- ✅ Tarjeta de contexto visible y funcional
- ✅ Deployment con Docker funciona
- ✅ Documentación completa y clara
- ✅ Tests E2E passing
- ✅ Performance mejorado mediblemente

---

## 📊 Estimaciones de Esfuerzo

### **Por Sprint:**

| Sprint | Horas Min | Horas Max | Días (8h/día) |
|--------|-----------|-----------|---------------|
| Sprint 1 | 20h | 28h | 3-4 días |
| Sprint 2 | 25h | 32h | 3-4 días |
| Sprint 3 | 29h | 36h | 4-5 días |
| Sprint 4 | 25h | 31h | 3-4 días |
| Sprint 5 | 25h | 32h | 3-4 días |
| **TOTAL** | **124h** | **159h** | **16-21 días** |

### **Agregando Buffer (20%):**

**Duración Real Estimada:** 19-27 días de trabajo  
**Duración Calendario:** 4-6 semanas (considerando interrupciones)

---

## 🎯 Dependencias Entre Sprints

```
Sprint 1 (Fundamentos)
    ↓
Sprint 2 (Configuración) ← Depende de Sprint 1
    ↓
Sprint 3 (i18n) ← Depende de Sprint 2 (user_preferences)
    ↓
Sprint 4 (Tipos) ← Depende de Sprint 3 (templates i18n)
    ↓
Sprint 5 (Optimización) ← Depende de todos los anteriores
```

**Nota:** Los Sprints deben completarse en orden debido a dependencias técnicas.

---

## 📈 Indicadores de Progreso

### **Métricas de Éxito por Sprint:**

**Sprint 1:**
- Bugs críticos resueltos: 3/3
- Navegación implementada: 100%
- Logs limpios: ✅

**Sprint 2:**
- Endpoints implementados: 5/5
- UI components completos: 3/3
- Validación funcionando: ✅

**Sprint 3:**
- Idiomas soportados: 2/2
- Archivos de traducción completos: 2/2
- Templates bilingües: 5/5

**Sprint 4:**
- Tipos de prompt funcionales: 4/4
- Workflows implementados: 4/4
- Selector UI funcional: ✅

**Sprint 5:**
- Tarjeta de contexto: ✅
- Docker funcional: ✅
- Tests E2E passing: ✅
- Documentación completa: ✅

---

## 🔄 Proceso de Trabajo

### **Inicio de Sprint:**
1. Revisar objetivos y tareas del Sprint
2. Leer documento de estado actual
3. Configurar entorno de desarrollo
4. Crear branch para el Sprint (opcional)

### **Durante el Sprint:**
1. Completar tareas en orden de prioridad
2. Testing continuo de cada tarea
3. **Actualizar PROGRESS.md al completar cada tarea** ✅
4. Documentar decisiones importantes

### **Fin de Sprint:**
1. Revisar criterios de éxito
2. Testing completo del Sprint
3. Actualizar PROGRESS.md con % de completitud
4. Commit de todos los cambios
5. Opcional: Demo/revisión de lo implementado

---

## 📝 Notas Importantes

### **Flexibilidad:**
- Las estimaciones son orientativas, no estrictas
- Si una tarea toma más tiempo, priorizar calidad sobre velocidad
- Está bien ajustar el alcance de un Sprint si es necesario

### **Calidad sobre Cantidad:**
- Mejor completar 4 tareas perfectamente que 6 a medias
- Cada tarea debe pasar criterios de éxito antes de marcarla completa
- El código debe ser revisado y testeado

### **Comunicación:**
- Documentar decisiones importantes en los archivos de Sprint
- Actualizar PROGRESS.md frecuentemente
- Mantener README.md actualizado con nuevas funcionalidades

---

## 🎯 Visión Post-Sprints

Al completar los 5 Sprints, PromptForge estará en estado **production-ready** con:

✅ **Funcionalidad completa:** Todos los flujos principales funcionando  
✅ **Múltiples idiomas:** Soporte ES/EN end-to-end  
✅ **Tipos de prompt:** Basic, System, Image, Additional funcionales  
✅ **UX pulida:** Navegación intuitiva, feedback claro  
✅ **Deployment listo:** Docker configurado y documentado  
✅ **Testing robusto:** Suite de tests E2E  
✅ **Documentación completa:** README, guías, troubleshooting  

---

> **Recordatorio:** Este roadmap es una guía, no una prisión. Ajusta según sea necesario, pero siempre prioriza calidad y experiencia de usuario.

**Última Actualización:** 17 de Febrero de 2026  
**Próxima Revisión:** Al completar cada Sprint
