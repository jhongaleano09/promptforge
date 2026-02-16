# 09. Fase: Validación de API Key de Test

**Estado:** 🆕 PLANIFICADA - Lista para Implementación  
**Prioridad:** 4 (BAJA - Solo para desarrollador/propietario)  
**Estimado:** 1-2 días

---

## 🎯 Objetivos

Implementar un sistema de validación de API key exclusiva para pruebas que:
1. Solo el propietario (desarrollador) pueda usar la API key de test
2. La API key de test NO se guarde en la base de datos
3. La API key de test NO aparezca en la UI de usuarios normales
4. Validación temporal sin persistencia (solo para pruebas)
5. Seguridad para evitar uso no autorizado

---

## 🗺 Desglose de Tareas

### Tarea 9.1: Crear Endpoint de Validación Especial

**Archivo:** `backend/app/api/endpoints.py`

**Objetivo:** Implementar endpoint `/api/settings/validate-test` que valide API key sin guardarla en base de datos.

**Diferencias con `/api/settings/validate`:**

| Aspecto | `/api/settings/validate` | `/api/settings/validate-test` |
|---------|-------------------------------|--------------------------------|
| **Guarda en BD** | ✅ Sí | ❌ NO |
| **Aparece en UI normal** | ✅ Sí | ❌ NO |
| **Uso** | Producción (usuarios finales) | Solo pruebas del propietario |
| **Persistencia** | Permanente | Temporal (sin guardar) |
| **Accesibilidad** | Pública (requiere autenticación) | Restringida (modo especial) |

**Implementación:**

#### 9.1.1: Estructura del Endpoint

```python
@router.post("/settings/validate-test")
async def validate_test_key(request: ValidationRequest):
    """
    Valida una API key SIN guardarla en base de datos.
    Solo para pruebas del propietario/desarrollador.
    
    Endpoint diferente de /settings/validate que:
    - Valida Y guarda en BD
    - Es para producción (usuarios finales)
    
    Args:
        request: ValidationRequest con provider, api_key
    
    Returns:
        JSON con resultado de validación
        
    Raises:
        HTTPException: Si la validación falla
    """
    # Implementación detallada en tareas siguientes
    pass
```

#### 9.1.2: Validación con Servicio LLM

**Objetivo:** Llamar realmente al servicio (OpenAI, Anthropic, etc.) para verificar que la API key funciona.

**Pasos de Implementación:**

1. **Obtener modelo de prueba según proveedor**
   - OpenAI: `gpt-3.5-turbo` (económico)
   - Anthropic: `claude-3-haiku-20240307` (económico)
   - Ollama: `llama3` (local, no tiene costo)

2. **Construir mensaje de prueba**
   - Simple: "Hello" o "Test"
   - Corto: máximo 5-10 tokens
   - Objetivo: validar rápidamente sin gastar mucho

3. **Llamar al servicio con LiteLLM**
```python
# Pseudocódigo
try:
    response = await litellm.acompletion(
        model=test_model,
        messages=[{"role": "user", "content": test_message}],
        api_key=request.api_key,
        max_tokens=5
    )
    
    # Validación exitosa
    return {
        "status": "success",
        "message": "API Key is valid",
        "provider": request.provider,
        "test_response": response.choices[0].message.content
    }
    
except AuthenticationError as e:
    # API key inválida
    raise HTTPException(
        status_code=401,
        detail="Invalid API Key. Please check your credentials."
    )
    
except RateLimitError as e:
    # Límite de cuota o rate limit
    raise HTTPException(
        status_code=429,
        detail="Rate limit exceeded or insufficient quota. Please check your OpenAI dashboard."
    )
    
except Exception as e:
    # Error general
    raise HTTPException(
        status_code=500,
        detail=f"Validation failed: {str(e)}"
    )
```

#### 9.1.3: Validación del Proveedor

**Objetivo:** Asegurar que el proveedor sea válido antes de intentar validar.

**Validaciones:**
```python
# Lista de proveedores soportados
SUPPORTED_PROVIDERS = ["openai", "anthropic", "ollama"]

# Validar que el proveedor esté en la lista
if request.provider not in SUPPORTED_PROVIDERS:
    raise HTTPException(
        status_code=400,
        detail=f"Provider '{request.provider}' is not supported. Supported providers: {', '.join(SUPPORTED_PROVIDERS)}"
    )
```

**Consideraciones:**
- Case-insensitive (aceptar "OpenAI", "OPENAI", "openai")
- Mensaje de error claro y específico
- Listar proveedores soportados en el mensaje

#### 9.1.4: Rate Limiting (Opcional pero Recomendado)

**Objetivo:** Prevenir abusos del endpoint de validación de prueba.

**Implementación:**
```python
from slowapi import Request
from functools import wraps
import time
from collections import defaultdict

# Almacenamiento en memoria (simple para prototipo)
validation_attempts = defaultdict(list)
RATE_LIMIT = 10  # Máximo 10 validaciones por hora
RATE_WINDOW = 3600  # 1 hora en segundos

def rate_limit_decorator(request: Request):
    """Decorator para rate limiting en validaciones de prueba."""
    client_ip = request.client.host
    current_time = time.time()
    
    # Limpiar intentos antiguos
    validation_attempts[client_ip] = [
        attempt for attempt in validation_attempts[client_ip]
        if current_time - attempt < RATE_WINDOW
    ]
    
    # Verificar límite
    if len(validation_attempts[client_ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Maximum {RATE_LIMIT} validations per hour."
        )
    
    # Guardar intento
    validation_attempts[client_ip].append(current_time)
    return True

# Aplicar al endpoint
@router.post("/settings/validate-test")
@rate_limit_decorator  # Aplicar rate limiting
async def validate_test_key(request: ValidationRequest):
    # ... lógica de validación
    pass
```

**Mejoras futuras (no implementar ahora):**
- Usar Redis para rate limiting distribuido
- Implementar rate limiting por API key (no solo por IP)
- Agregar cooldown entre validaciones fallidas

**❓ Preguntas Clave:**

1. ¿Deseas implementar rate limiting ahora (recomendado) o dejarlo para una fase posterior?
2. ¿Deberíamos usar 10 validaciones por hora o un número diferente?
3. ¿Deseas implementar el rate limiting con un decorador de Python o con middleware de FastAPI?
4. ¿Qué debería pasar si se excede el límite? ¿Error HTTP 429 o permitir con un warning?

#### 9.1.5: Logging de Validaciones de Prueba

**Objetivo:** Registrar todas las validaciones de API key de prueba para auditoría.

**Implementación:**
```python
import logging

# Configurar logger específico para validaciones de prueba
test_validation_logger = logging.getLogger("test_validations")
test_validation_logger.setLevel(logging.INFO)

# Handler personalizado
handler = logging.FileHandler('logs/test_validations.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
test_validation_logger.addHandler(handler)

@router.post("/settings/validate-test")
async def validate_test_key(request: Request, validation_request: ValidationRequest):
    # ... lógica de validación
    
    # Registrar la validación
    client_ip = request.client.host
    result_status = "success" if "status" in response else "error"
    
    test_validation_logger.info(
        f"IP: {client_ip} | Provider: {request.provider} | "
        f"Status: {result_status} | Message: {response.get('message', 'N/A')}"
    )
    
    return response
```

**Información registrada:**
- IP del cliente
- Proveedor
- Status (success/error)
- Mensaje de resultado o error
- Timestamp (agregado automáticamente por el logger)

**Consideraciones:**
- NO guardar la API key en el log (seguridad)
- Guardar solo metadatos (IP, proveedor, status)
- Rotar logs periódicamente (no crecer indefinidamente)

**❓ Preguntas Clave:**

1. ¿Deseas guardar el log en `logs/test_validations.log` o usar la ruta `backend.log` existente?
2. ¿Deseas agregar el user agent del cliente en el log o solo la IP?
3. ¿Deberíamos usar diferentes niveles de logging (INFO, WARNING, ERROR) según el resultado de la validación?
4. ¿Deberíamos agregar también el timestamp exacto en formato ISO 8601 en el mensaje del log?
5. ¿Cómo deseas que se manejen los logs en producción? ¿Rotar automáticamente o archivar por fecha?

---

### Tarea 9.2: Modo de Test para Propietario

**Opción A: Variable de Entorno (RECOMENDADA)**

**Objetivo:** Permitir habilitar un "modo de test" mediante variable de entorno.

**Implementación en backend:**

1. **Agregar validación en endpoints existentes**
```python
import os

@router.post("/settings/validate-test")
async def validate_test_key(request: ValidationRequest):
    # Verificar si estamos en modo de test
    test_mode = os.getenv("PROMPTFORGE_TEST_MODE", "false").lower() == "true"
    
    if not test_mode:
        raise HTTPException(
            status_code=403,
            detail="Test validation endpoint is only available in test mode. Set PROMPTFORGE_TEST_MODE=true to enable."
        )
    
    # ... lógica de validación
    pass
```

2. **Documentación de variables de entorno**
- Agregar a `.env.example`:
```bash
# Modo de test para validación de API keys sin persistencia
# WARNING: Solo habilitar si eres el propietario/desarrollador
PROMPTFORGE_TEST_MODE=false
```

**Ventajas:**
- Simple de implementar
- Fácil de deshabilitar en producción
- No requiere cambios en el frontend

**❓ Preguntas Clave:**

1. ¿Deseas que el mensaje de error sea específico sobre que este endpoint es solo para desarrolladores o genérico?
2. ¿Deberíamos agregar una lista blanca de IPs que pueden usar el modo de test (solo tu IP, etc.)?
3. ¿Deseas que el modo de test también habilite otros endpoints de debugging o solo el de validación?

**Opción B: Parámetro de URL (Alternativa)**

**Objetivo:** Permitir acceder al modo de test mediante parámetros en la URL.

**Implementación en backend:**
```python
@router.post("/settings/validate-test")
async def validate_test_key(request: Request, validation_request: ValidationRequest):
    # Verificar si hay parámetro de test en la query string
    test_mode = request.query_params.get("test_mode", "false").lower() == "true"
    test_key = request.query_params.get("test_key")
    
    if not test_mode or not test_key:
        raise HTTPException(
            status_code=403,
            detail="Test mode requires ?test_mode=true&test_key=<your_test_key>"
        )
    
    # Opcional: Validar que la test_key sea correcta
    # Esto agrega una capa extra de seguridad
    # if test_key != os.getenv("PROMPTFORGE_TEST_KEY"):
    #     raise HTTPException(status_code=403, detail="Invalid test key")
    
    # ... lógica de validación
    pass
```

**Uso:**
```
curl -X POST http://localhost:8001/api/settings/validate-test?test_mode=true&test_key=sk-proj... \
  -H "Content-Type: application/json" \
  -d '{"provider":"openai","api_key":"sk-proj..."}'
```

**Ventajas:**
- Más seguro (puedes rotar la test_key)
- Flexible (puedes habilitar/deshabilitar sin reiniciar backend)
- No requiere cambios en archivos de configuración

**Desventajas:**
- Más complejo de usar (URL larga)
- Visible en la barra de direcciones (puede ser copiada)

**❓ Preguntas Clave:**

1. ¿Deseas implementar Opción A (variable de entorno), Opción B (parámetro de URL), o ambas?
2. ¿Si implementamos ambas, cuál debería tener prioridad (variable de entorno vs parámetro)?
3. ¿Deseas que la validación de la test_key en Opción B sea opcional o requerida?

**Opción C: Token de Validación de Un Solo Uso (MÁS SEGURO)**

**Objetivo:** Generar tokens temporales que expiran después de un tiempo limitado y solo pueden usarse una vez.

**Implementación en backend:**
```python
from app.core.security import generate_temp_token, validate_temp_token
from datetime import datetime, timedelta

@router.post("/settings/validate-test")
async def validate_test_key(request: Request, validation_request: ValidationRequest):
    # Verificar si hay un token de test válido en la solicitud
    provided_token = request.query_params.get("test_token")
    
    if provided_token:
        # Validar que el token sea válido y no expirado
        if not validate_temp_token(provided_token):
            raise HTTPException(
                status_code=403,
                detail="Invalid or expired test token"
            )
        # Token válido, continuar
    else:
        # No hay token, generar uno
        test_token = generate_temp_token(expiry_minutes=60)  # Expira en 1 hora
        
        # Retornar el token en la respuesta
        return {
            "status": "token_generated",
            "message": "Test token generated. Use this token for validations in the next 60 minutes.",
            "test_token": test_token,
            "expires_at": (datetime.now() + timedelta(hours=1)).isoformat()
        }
    
    # ... lógica de validación de la API key
    pass
```

**Implementación de tokens:**
```python
# backend/app/core/test_token_manager.py

from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import os

# Usar la misma clave de encriptación
fernet = Fernet(os.getenv("PROMPTFORGE_SECRET_KEY"))

# Almacenamiento en memoria (simple para prototipo)
# En producción, usar Redis o base de datos
active_tokens = {}

def generate_temp_token(expiry_minutes: int = 60) -> str:
    """
    Genera un token temporal de validación.
    
    Args:
        expiry_minutes: Minutos hasta que el token expire
    
    Returns:
        Token encriptado
    """
    # Crear payload con timestamp de expiración
    payload = {
        "type": "test_validation",
        "expires_at": (datetime.now() + timedelta(minutes=expiry_minutes)).isoformat(),
        "created_at": datetime.now().isoformat()
    }
    
    # Encriptar el payload
    token = fernet.encrypt(str(payload).encode()).decode()
    
    # Limpiar tokens expirados
    cleanup_expired_tokens()
    
    return token

def validate_temp_token(token: str) -> bool:
    """
    Valida si un token de prueba es válido y no ha expirado.
    
    Args:
        token: Token a validar
    
    Returns:
        True si es válido, False si es inválido o expirado
    """
    try:
        # Desencriptar el token
        decrypted = fernet.decrypt(token.encode()).decode()
        payload = eval(decrypted)  # Parsear el JSON
        
        # Verificar tipo
        if payload.get("type") != "test_validation":
            return False
        
        # Verificar expiración
        expires_at = datetime.fromisoformat(payload["expires_at"])
        if datetime.now() > expires_at:
            return False
        
        return True
    
    except Exception:
        return False

def cleanup_expired_tokens():
    """
    Elimina tokens expirados del almacenamiento en memoria.
    """
    current_time = datetime.now()
    
    for token_str, payload_str in list(active_tokens.items()):
        try:
            payload = eval(payload_str)
            expires_at = datetime.fromisoformat(payload["expires_at"])
            
            if current_time > expires_at:
                del active_tokens[token_str]
        except:
            del active_tokens[token_str]
```

**Ventajas:**
- Más seguro (tokens expiran)
- No expone la API key de test
- Puede rastrear quién está usando el token
- Fácil de revocar (limpiar tokens)

**Desventajas:**
- Más complejo de implementar
- Requiere gestión de tokens
- El usuario debe copiar el token en cada validación

**❓ Preguntas Clave:**

1. ¿Deseas implementar Opción C (tokens) o prefieres Opción A o B?
2. ¿Deseas que los tokens expiren en 1 hora o prefieres un tiempo diferente?
3. ¿Deberíamos guardar un registro de tokens generados con qué IP los usó (para auditoría)?
4. ¿Deseas agregar un endpoint para revocar tokens manualmente?

---

### Tarea 9.3: Implementación en Frontend - Modo de Test

**Opción A: Variable de Entorno (Backend)**

Si se usa la opción de variable de entorno (`PROMPTFORGE_TEST_MODE=true`):

**No se requiere cambios en el frontend.**

El endpoint `/api/settings/validate-test` solo estará disponible cuando la variable de entorno esté activada. El frontend normal no podrá acceder a este endpoint sin la variable activada.

**Uso para propietario/desarrollador:**
1. Configurar variable en `.env.local` o `.env` del backend:
```bash
PROMPTFORGE_TEST_MODE=true
```

2. Reiniciar backend
3. Usar `curl` o Postman para probar el endpoint:
```bash
curl -X POST http://localhost:8001/api/settings/validate-test \
  -H "Content-Type: application/json" \
  -d '{"provider":"openai","api_key":"sk-proj-wzf0..."}'
```

4. Verificar que la API key de test NO se guarde en la base de datos

**Opción B: Parámetro de URL (Backend + Frontend)**

Si se usa la opción de parámetro de URL (`?test_mode=true&test_key=sk-...`):

**Implementación en frontend:**

1. **Crear componente de "Modo de Test"** (opcional)
```typescript
'use client';

import { useState } from 'react';

export function TestModePanel() {
  const [testMode, setTestMode] = useState(false);
  const [testKey, setTestKey] = useState('');

  return (
    <div className="p-4 border rounded-lg bg-orange-50">
      <h3 className="font-semibold mb-2">🧪 Modo de Test</h3>
      
      <div className="space-y-3">
        <div>
          <label className="text-sm font-medium">Activar Modo de Test</label>
          <select
            value={testMode.toString()}
            onChange={(e) => setTestMode(e.target.value === 'true')}
            className="w-full border rounded p-2"
          >
            <option value="false">Deshabilitado</option>
            <option value="true">Habilitado</option>
          </select>
        </div>
        
        {testMode && (
          <div>
            <label className="text-sm font-medium">API Key de Test</label>
            <input
              type="password"
              value={testKey}
              onChange={(e) => setTestKey(e.target.value)}
              placeholder="sk-..."
              className="w-full border rounded p-2"
            />
            <p className="text-xs text-muted-foreground mt-1">
              Esta API key se usará para validaciones de prueba y NO se guardará en la base de datos.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
```

2. **Integrar con `page.tsx`**
```typescript
// Solo mostrar si hay una variable de entorno o flag especial
if (process.env.NEXT_PUBLIC_TEST_MODE === 'true') {
  return <TestModePanel />
}
```

**Uso para propietario/desarrollador:**
1. Agregar variable en `.env.local` del frontend:
```bash
NEXT_PUBLIC_TEST_MODE=true
```

2. Reiniciar frontend
3. Usar el panel para habilitar/deshabilitar modo de test
4. Validar API keys usando el modo de test

**Opción C: Token de Validación (Backend + Frontend)**

Si se usa la opción de tokens:

**Implementación en frontend:**

1. **Crear componente de gestión de tokens**
```typescript
'use client';

import { useState, useEffect } from 'react';
import { fetchEventSource } from '@microsoft/fetch-event-source';

export function TestTokenManager() {
  const [testToken, setTestToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Generar token al montar
  useEffect(() => {
    generateTestToken();
  }, []);

  const generateTestToken = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/settings/validate-test`);
      const data = await res.json();
      
      if (data.status === 'token_generated') {
        setTestToken(data.test_token);
      }
    } catch (error) {
      console.error('Error generating test token:', error);
    } finally {
      setLoading(false);
    }
  };

  const validateTestKey = async (apiKey: string) => {
    if (!testToken) {
      alert('Primero genera un token de prueba');
      return;
    }
    
    try {
      const res = await fetch(
        `${API_BASE}/settings/validate-test?test_token=${testToken}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ provider: 'openai', api_key: apiKey })
        }
      );
      
      const data = await res.json();
      
      if (data.status === 'success') {
        alert(`✓ API Key válida: ${data.test_response}`);
      } else {
        alert(`✗ API Key inválida: ${data.message}`);
      }
    } catch (error) {
      console.error('Error validating test key:', error);
    }
  };

  return (
    <div className="p-4 border rounded-lg bg-blue-50">
      <h3 className="font-semibold mb-2">🧪 Gestor de Tokens de Prueba</h3>
      
      <div className="space-y-4">
        <div>
          <p className="text-sm text-muted-foreground mb-2">
            Token actual:
          </p>
          <code className="block p-2 bg-background rounded text-xs">
            {testToken || 'No generado'}
          </code>
        </div>
        
        <button
          onClick={generateTestToken}
          disabled={loading}
          className="px-4 py-2 bg-primary text-primary-foreground rounded"
        >
          {loading ? 'Generando...' : 'Generar Nuevo Token'}
        </button>
      </div>
      
      <div>
        <label className="text-sm font-medium">API Key de Test</label>
        <input
          type="password"
          id="test-api-key"
          placeholder="sk-..."
          className="w-full border rounded p-2"
        />
      </div>
      
      <button
        onClick={() => {
          const apiKeyInput = document.getElementById('test-api-key') as HTMLInputElement;
          validateTestKey(apiKeyInput.value);
        }}
        className="w-full px-4 py-2 bg-green-600 text-white rounded"
      >
        Validar API Key
      </button>
    </div>
  );
}
```

**❓ Preguntas Clave (**

1. ¿Deseas implementar Opción A (variable de entorno), Opción B (parámetro de URL), Opción C (tokens), o una combinación?
2. Si implementamos múltiples opciones, ¿deseas que el frontend soporte cambiar entre ellas fácilmente?
3. ¿Deseas que el modo de test esté siempre visible en el frontend (para desarrollador) o solo con una variable especial?

---

### Tarea 9.4: Testing y Validación

**Objetivo:** Probar completamente la funcionalidad de validación de API key de test.

**Casos de Prueba:**

#### 9.4.1: Pruebas de Backend

1. **Validación exitosa**
   - Enviar API key válida
   - Verificar que retorne status "success"
   - Verificar que NO se guarde en BD
   - Verificar logs de validación

2. **Validación fallida - API Key inválida**
   - Enviar API key inválida
   - Verificar que retorne error 401
   - Verificar mensaje de error claro
   - Verificar que NO se guarde en BD

3. **Validación fallida - Rate limit**
   - Enviar múltiples validaciones rápidamente (más del límite)
   - Verificar que retorne error 429
   - Verificar mensaje de rate limit
   - Esperar a que expire la ventana de tiempo
   - Verificar que permita nuevamente

4. **Validación fallida - Proveedor no soportado**
   - Enviar proveedor inválido
   - Verificar que retorne error 400
   - Verificar lista de proveedores soportados

5. **Validación con modo de test deshabilitado**
   - Llamar al endpoint sin variable de entorno activada
   - Verificar que retorne error 403
   - Verificar mensaje de error específico

#### 9.4.2: Pruebas de Seguridad

1. **Exposición de API key de test**
   - Verificar que la API key NO aparezca en logs
   - Verificar que NO se guarde en ninguna parte
   - Verificar que NO se retorne en ninguna respuesta

2. **Rate limiting**
   - Verificar que previene más de 10 validaciones por hora
   - Verificar que el límite se resetea después del tiempo

3. **Acceso no autorizado**
   - Intentar acceder desde IP diferente (simulado)
   - Verificar que el rate limiting funcione por IP

#### 9.4.3: Pruebas de Integración (si hay frontend)

1. **Validación desde frontend**
   - Usar componente de test
   - Verificar que se pueda generar/validar API keys
   - Verificar que la API key de test se use correctamente

2. **Validación con modo de test**
   - Habilitar modo de test
   - Verificar que el endpoint esté accesible
   - Verificar que el modo de test se pueda deshabilitar

3. **Validación sin modo de test**
   - Verificar que el endpoint NO esté accesible sin modo de test
   - Verificar que la UI normal no muestre opciones de test

**❓ Preguntas Clave:**

1. ¿Deseas crear un script automatizado de pruebas (con pytest o unittest) o pruebas manuales?
2. ¿Qué criterios de éxito considerar para que esta fase esté completa?
3. ¿Deseas que incluyamos pruebas de integración que prueben el flujo completo (validación + uso en workflow)?
4. ¿Deseas agregar tests de carga para verificar que el endpoint responda correctamente bajo presión (múltiples peticiones simultáneas)?

---

## 📊 Summary de Fase 9

### Archivos a Crear

**Backend:**
1. `backend/app/api/endpoints.py` (actualizar) - Endpoint `/api/settings/validate-test`
2. `backend/app/core/test_token_manager.py` - Gestión de tokens (si usa Opción C)

**Frontend (si aplica):**
1. `frontend/src/components/test-mode-panel.tsx` - Panel de modo de test (Opción B)
2. `frontend/src/components/test-token-manager.tsx` - Gestor de tokens (Opción C)

### Tareas Totales: 4
1. [ ] 9.1: Crear endpoint de validación especial
2. [ ] 9.2: Implementar modo de test para propietario
3. [ ] 9.3: Implementación en frontend (si aplica)
4. [ ] 9.4: Testing y validación

### Preguntas Clave Totales: 19
Distribuidas en cada tarea para facilitar la implementación.

---

## 🎯 Criterios de Éxito de Fase 9

Al completar esta fase, el sistema deberá:

1. ✅ Endpoint de validación de test implementado (`/api/settings/validate-test`)
2. ✅ API key de test NO se guarda en base de datos
3. ✅ API key de test NO aparece en UI normal
4. ✅ Solo el propietario puede usar la API key de test
5. ✅ Validación real con el servicio (OpenAI, Anthropic, etc.)
6. ✅ Rate limiting implementado (opcional pero recomendado)
7. ✅ Logging de validaciones para auditoría
8. ✅ Modo de test fácil de habilitar/deshabilitar
9. ✅ Documentación clara para desarrollador/propietario
10. ✅ Testing completo de todas las funcionalidades

---

**Fase 9 - Planificación Creada Por:** OpenCode Assistant  
**Fecha:** 16 de febrero de 2026  
**Versión:** 1.0 - Validación de API Key de Test  
**Estado:** ✅ LISTA PARA IMPLEMENTACIÓN
