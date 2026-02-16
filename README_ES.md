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

## ⚡ Inicio Rápido (Docker)

La forma más fácil de ejecutar PromptForge es usando Docker.

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/jhongaleano09/promptforge.git
    cd promptforge
    ```

2.  **Configurar Entorno:**
    Copia la configuración de ejemplo:
    ```bash
    cp .env.example .env
    ```
    *Opcional:* Edita `.env` para ajustar puertos o pre-cargar claves API.

3.  **Ejecutar con Docker Compose:**
    ```bash
    docker-compose up -d --build
    ```

4.  **Acceder a la Aplicación:**
    *   **Frontend:** [http://localhost:3000](http://localhost:3000)
    *   **Backend Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

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

## 🔐 Configuración

| Variable | Descripción | Predeterminado |
| :--- | :--- | :--- |
| `BACKEND_PORT` | Puerto para la API Python | `8000` |
| `FRONTEND_PORT` | Puerto para la UI Web | `3000` |
| `ENCRYPTION_KEY` | Clave para encriptar credenciales | (Generada por backend si está vacía) |
| `DATABASE_URL` | Cadena de conexión SQLAlchemy | `sqlite:///./data/database.sqlite` |

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
