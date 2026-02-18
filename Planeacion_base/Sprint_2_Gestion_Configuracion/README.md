# Sprint 2: Gestión de Configuración

## Descripción General
Este Sprint se enfoca en mejorar la gestión de configuraciones de la aplicación, permitiendo múltiples configuraciones de proveedores y modelos, gestión centralizada de preferencias de usuario, y una interfaz mejorada para la configuración.

## Duración Estimada
**4-6 días**

## Prioridad
🔴 **ALTA** - Fundamental para flexibilidad y escalabilidad del sistema

## Prerequisitos
- ✅ Sprint 1 completado (especialmente tarea 1.3 - bug crítico corregido)
- ✅ Sistema funcional con navegación básica
- ✅ Base de datos con tabla `user_preferences` existente

## Objetivos del Sprint

### Objetivo Principal
Transformar el sistema de configuración de una única API key a un sistema flexible que soporte múltiples proveedores y modelos con perfiles configurables.

### Objetivos Específicos
1. Implementar sistema de múltiples proveedores (OpenAI, Anthropic, Google, etc.)
2. Permitir configuración de múltiples API keys por proveedor
3. Crear sistema de preferencias de usuario persistente
4. Mejorar UI de configuración con validación en tiempo real
5. Implementar sistema de detección y validación de API keys

## Estructura de Archivos

```
Sprint_2_Gestion_Configuracion/
├── README.md                           # Este archivo
├── 2.1_sistema_multiproveedores.md     # Sistema de múltiples proveedores
├── 2.2_gestion_api_keys.md             # Gestión de múltiples API keys
├── 2.3_preferencias_usuario.md         # Sistema de preferencias persistente
├── 2.4_validacion_tiempo_real.md       # Validación de configuración
└── 2.5_ui_configuracion_mejorada.md    # Interfaz mejorada de settings
```

## Tareas del Sprint

### 2.1 - Sistema de Múltiples Proveedores 🔴 CRÍTICA
**Duración**: 1-2 días  
**Descripción**: Implementar soporte para múltiples proveedores de LLM (OpenAI, Anthropic, Google, etc.) con detección automática de modelos disponibles.

**Entregables**:
- Backend puede manejar llamadas a diferentes proveedores
- Frontend permite seleccionar provider desde UI
- Configuración de modelos por provider
- Detección automática de modelos disponibles

### 2.2 - Gestión de Múltiples API Keys 🟠 ALTA
**Duración**: 1 día  
**Descripción**: Permitir configurar y almacenar múltiples API keys por proveedor con encriptación segura.

**Entregables**:
- CRUD de API keys en backend
- UI para agregar/editar/eliminar API keys
- Encriptación segura de keys en base de datos
- Validación de formato de API keys

### 2.3 - Sistema de Preferencias de Usuario 🟠 ALTA
**Duración**: 1 día  
**Descripción**: Utilizar tabla `user_preferences` existente para persistir configuraciones del usuario (idioma, modelo preferido, etc.).

**Entregables**:
- Endpoints de backend para preferencias
- Sincronización entre Zustand y base de datos
- Persistencia de configuración entre sesiones
- Migración de data existente si aplica

### 2.4 - Validación en Tiempo Real 🟡 MEDIA
**Duración**: 0.5-1 día  
**Descripción**: Implementar validación de configuración en tiempo real (API keys válidas, modelos disponibles, etc.).

**Entregables**:
- Endpoint de validación de API keys
- Feedback visual inmediato en UI
- Detección de errores comunes
- Sugerencias de corrección

### 2.5 - UI de Configuración Mejorada 🟡 MEDIA
**Duración**: 1-1.5 días  
**Descripción**: Rediseñar interfaz de configuración con mejor UX, organización por tabs, y validación visual.

**Entregables**:
- UI organizada por tabs (General, Providers, Advanced)
- Validación visual inline
- Tooltips explicativos
- Preview de configuración actual

## Relación con Otros Sprints

### Depende de:
- **Sprint 1**: Base funcional y bugs críticos corregidos

### Habilita:
- **Sprint 3**: Preferencias de idioma para i18n
- **Sprint 4**: Configuración de tipos de prompt modulares
- **Sprint 5**: Configuración de deployment

## Archivos Principales Afectados

### Backend:
```
backend/app/
├── api/
│   ├── endpoints.py              # Modificar: endpoints de settings
│   ├── user_preferences.py       # Modificar: expandir preferencias
│   └── providers.py              # CREAR: gestión de providers
├── db/
│   ├── models.py                 # Modificar: modelos de configuración
│   └── migrations/               # CREAR: migraciones necesarias
├── services/
│   ├── provider_manager.py       # CREAR: abstracción de providers
│   └── key_validator.py          # CREAR: validación de API keys
└── config.py                     # Modificar: configuración general
```

### Frontend:
```
frontend/src/
├── app/
│   └── settings/
│       └── page.tsx              # Modificar: UI mejorada
├── components/
│   ├── settings/
│   │   ├── ProviderSelector.tsx  # CREAR: selector de provider
│   │   ├── ApiKeyManager.tsx     # CREAR: gestión de keys
│   │   ├── ModelSelector.tsx     # CREAR: selector de modelos
│   │   └── PreferencesForm.tsx   # CREAR: formulario de preferencias
│   └── ui/
│       └── Tabs.tsx              # CREAR: componente de tabs
├── store/
│   ├── settingsStore.ts          # Modificar: store de settings
│   └── preferenceStore.ts        # CREAR: store de preferencias
└── lib/
    └── validators.ts             # CREAR: validadores frontend
```

## Criterios de Aceptación del Sprint

### Funcionales:
- [ ] Usuario puede seleccionar entre múltiples providers
- [ ] Usuario puede configurar API keys para cada provider
- [ ] Configuración persiste entre sesiones
- [ ] Validación de API keys funciona correctamente
- [ ] UI de settings es intuitiva y organizada

### Técnicos:
- [ ] API keys encriptadas en base de datos
- [ ] Endpoints RESTful bien diseñados
- [ ] Type safety en TypeScript/Python
- [ ] Sin regresiones de Sprint 1
- [ ] Código bien documentado

### UX/UI:
- [ ] Feedback visual claro en validaciones
- [ ] Estados de carga apropiados
- [ ] Mensajes de error comprensibles
- [ ] Diseño responsive
- [ ] Accesible por teclado

## Riesgos y Mitigaciones

### Riesgo 1: Complejidad de Múltiples Providers
**Impacto**: Alto  
**Probabilidad**: Media  
**Mitigación**: Crear abstracción de provider_manager que unifique interfaces

### Riesgo 2: Seguridad de API Keys
**Impacto**: Crítico  
**Probabilidad**: Baja  
**Mitigación**: Usar encriptación robusta (Fernet) y nunca loguear keys completas

### Riesgo 3: Migración de Configuración Existente
**Impacto**: Medio  
**Probabilidad**: Media  
**Mitigación**: Crear script de migración y mantener backwards compatibility

## Métricas de Éxito

1. **Funcionalidad**: 100% de providers soportados funcionan correctamente
2. **Seguridad**: 0 API keys expuestas en logs o respuestas
3. **UX**: Tiempo de configuración < 2 minutos para usuario nuevo
4. **Performance**: Validación de API key < 1 segundo
5. **Confiabilidad**: 0 pérdida de configuración entre sesiones

## Testing Requerido

### Tests Manuales:
- Configurar cada provider disponible
- Agregar/editar/eliminar API keys
- Validar keys correctas e incorrectas
- Cambiar preferencias y verificar persistencia
- Probar en diferentes navegadores

### Tests Automatizados (Opcional para Sprint 5):
- Unit tests de validadores
- Integration tests de endpoints
- E2E tests de flujo de configuración

## Notas Importantes

⚠️ **SEGURIDAD**: API keys deben encriptarse SIEMPRE antes de almacenar en BD

📝 **DOCUMENTACIÓN**: Documentar formato de cada provider en código

🔄 **PROGRESS.md**: Actualizar después de cada tarea completada

🎯 **ENFOQUE**: Priorizar funcionalidad sobre perfección visual (mejoras visuales en Sprint 5)

## Resultado Esperado

Al finalizar Sprint 2:

### Antes:
```
Settings:
  Provider: [OpenAI]  (hardcoded)
  API Key: [__________]
  Model: [gpt-4]  (hardcoded)
```

### Después:
```
Settings (con tabs):

[General] [Providers] [Advanced]

Provider: [OpenAI ▼]  [Anthropic] [Google]
  
API Keys:
  ✅ sk-proj-abc...xyz (OpenAI)  [Edit] [Delete]
  ✅ sk-ant-xyz...abc (Anthropic) [Edit] [Delete]
  [+ Add New Key]

Models Available:
  ○ gpt-4-turbo
  ● gpt-4  (selected)
  ○ gpt-3.5-turbo

User Preferences:
  Language: [Español ▼]
  Default Model: [gpt-4 ▼]
  Auto-save: [✓]
```

## Referencias

- OpenAI API: https://platform.openai.com/docs/api-reference
- Anthropic API: https://docs.anthropic.com/claude/reference
- Google Gemini API: https://ai.google.dev/docs
- Fernet Encryption: https://cryptography.io/en/latest/fernet/
- SQLAlchemy Encryption: https://sqlalchemy-utils.readthedocs.io/

---

**Próximo Sprint**: Sprint 3 - Internacionalización (depende de preferencias de usuario de Sprint 2)
