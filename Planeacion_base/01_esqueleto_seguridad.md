# Fase 1: Esqueleto, Seguridad y Configuración

**Objetivo:** Establecer la base del proyecto, asegurar que podemos guardar secretos (API Keys) de forma segura y validar que tenemos conexión con los LLMs antes de intentar cualquier operación compleja.

## 🛠️ Tareas Técnicas

### 1.1 Inicialización del Monorepo
- [ ] Crear estructura de directorios:
  ```text
  promptforge/
  ├── backend/ (Python/FastAPI)
  ├── frontend/ (Next.js)
  └── shared/ (Tipos/Schemas si aplica)
  ```
- [ ] Inicializar Git.
- [ ] **Backend:** `poetry init` o `pip install -r requirements.txt` (FastAPI, SQLAlchemy, Pydantic, LiteLLM, Cryptography).
- [ ] **Frontend:** `npx create-next-app@latest` (TypeScript, Tailwind, ESLint).

### 1.2 Base de Datos y Persistencia
- [ ] Diseñar modelo `Settings` en SQLAlchemy:
  - `id`: PK
  - `provider`: String (openai, anthropic, etc.)
  - `api_key_encrypted`: Binary (blob)
  - `model_preference`: String
- [ ] Implementar `SecurityService`:
  - Generar y guardar una `SECRET_KEY` maestra local (en archivo `.env` o en carpeta de config del usuario) la primera vez que se corre la app.
  - Métodos: `encrypt_key(raw_key)`, `decrypt_key(encrypted_key)`.

### 1.3 API de Configuración (Backend)
- [ ] Endpoint `POST /api/settings/validate`:
  - Recibe `{ provider, api_key }`.
  - Realiza una llamada de prueba ("Ping") al LLM con `max_tokens=1`.
  - Captura errores específicos:
    - `AuthenticationError` -> "API Key inválida".
    - `RateLimitError` -> "Sin saldo o límite excedido".
    - `Timeout` -> "Error de conexión".
  - Retorna éxito o error detallado.
- [ ] Endpoint `POST /api/settings/save`:
  - Llama a `validate` internamente.
  - Si es válido -> Encripta -> Guarda en SQLite.

### 1.4 Interfaz de Onboarding (Frontend)
- [ ] Pantalla de bienvenida (si no hay keys guardadas).
- [ ] Formulario de configuración:
  - Selector de Proveedor (OpenAI, Anthropic, etc.).
  - Input de API Key (tipo password).
  - Botón "Validar y Guardar".
- [ ] Indicador de carga (spinner) durante el Ping.
- [ ] Toast/Notificación de éxito o error.

## ✅ Criterios de Aceptación (DoD)
1.  La aplicación levanta backend y frontend sin errores.
2.  El usuario puede ingresar una Key inválida y recibir un error claro.
3.  El usuario puede ingresar una Key válida, se guarda, y si reinicia la aplicación, la Key persiste (no se le pide de nuevo).
4.  La base de datos SQLite contiene la Key en formato ilegible (encriptado).

## ❓ Preguntas Clave para el Usuario
1.  **Ubicación de la BD:** ¿Prefieres que el archivo `database.sqlite` se guarde en la carpeta del proyecto (fácil de borrar) o en la carpeta de configuración del sistema operativo (`~/.config/promptforge`, más persistente)? RTA/ en la carpeta del proyecto.
2.  **Gestión de Modelos:** Al validar la API Key, ¿quieres que intentemos listar los modelos disponibles automáticamente (si la API lo permite) para llenar un dropdown, o prefieres que el usuario escriba el nombre del modelo (ej: "gpt-4-turbo") manualmente? RTA/ Correcto debemos listar los modelos diponibles de forma automatica para dar la opcion al usuario de seleccionar el modelo a usar.
3.  **Fallback:** Si la validación (Ping) falla por timeout (común en redes lentas), ¿permitimos "Guardar de todos modos" bajo riesgo del usuario, o bloqueamos el guardado obligatoriamente? RTA/ iniciar un contador de 10 segundos e indicamos al usuario que algo paso y que estamos nuevamente intentando conectarnos con la API, que nos espere mientras realizamos nuevamente una validación. en caso de tener nuevamente una respuesta negativa, indicar al usuario para que valide la API KEY y poder continuar.
