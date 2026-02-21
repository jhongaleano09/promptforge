# [🇬🇧 English](README.md) [🇪🇸 Español]

# PromptForge 🔨

**Plataforma Profesional de Ingeniería de Prompts**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

PromptForge transforma ideas vagas en prompts listos para producción mediante un proceso estructurado de clarificación, generación de variantes y pruebas competitivas (Arena).

## 🚀 ¿Por qué PromptForge?

La mayoría de herramientas se enfocan en la **cantidad** (bibliotecas de snippets). PromptForge se enfoca en la **calidad** mediante ingeniería:

1.  **Calidad sobre Cantidad:** Generamos 3 variantes competitivas distintas para cada problema.
2.  **Human-in-the-Loop:** Tú eres el juez. Nuestra "Arena" te permite probar los prompts lado a lado.
3.  **Agnóstico del Modelo:** Funciona con OpenAI, Anthropic y LLMs locales (vía Ollama).
4.  **Seguro:** Tus claves API se almacenan encriptadas en reposo.

## 🏗️ Arquitectura

```mermaid
graph TD
    User[Usuario] --> Frontend[Frontend Next.js]
    Frontend --> Backend[Backend FastAPI]
    Backend --> DB[(SQLite + Claves Encriptadas)]
    Backend --> Orchestrator[Orquestador LangGraph]
    Orchestrator --> Agents[Agentes IA (Generador/Crítico)]
    Agents --> LLM[Interfaz LLM (LiteLLM)]
```

## ⚡ Inicio Rápido (Docker, local-first)

La forma más fácil de ejecutar PromptForge localmente es usando Docker.

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/jhongaleano09/promptforge.git
    cd promptforge
    ```

    Si hace falta, haz ejecutable el script (Linux/macOS):
    ```bash
    chmod +x run-local.sh
    ```

2.  **Iniciar la app (un comando):**
    ```bash
    ./run-local.sh
    ```
    Esto crea un `.env` desde `.env.example` si hace falta y levanta los contenedores.

    Windows (PowerShell):
    ```powershell
    .\run-local.ps1
    ```

3.  **Acceder a la aplicación:**
    *   **Frontend:** [http://localhost:3000](http://localhost:3000)
    *   **Backend Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

4.  **Agregar tu API key en la UI:**
    Ve a Settings → Providers y agrega tu clave localmente. Nada sale de tu máquina.

## 🛠️ Configuración de Desarrollo

Si deseas contribuir o modificar el código:

### Backend (Python)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend (Node.js)
```bash
cd frontend
npm install
npm run dev
```

## 🔐 Configuración (local)

| Variable | Descripción | Predeterminado |
| :--- | :--- | :--- |
| `API_PORT` | Puerto para la API Python | `8000` |
| `APP_PORT` | Puerto para la UI Web | `3000` |
| `PROMPTFORGE_SECRET_KEY` | Clave para encriptar credenciales | (Auto-generada si está vacía) |
| `DATABASE_URL` | Cadena de conexión SQLAlchemy | `sqlite+aiosqlite:///data/database.sqlite` |

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
