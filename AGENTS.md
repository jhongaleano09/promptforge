# Agent Directives & Repository Context (AGENTS.md)

Welcome, Agents. This file contains the essential rules, context, and commands for operating in this repository. Ensure you adhere to these guidelines to maintain a consistent, functional, and high-quality codebase.

## Repository Structure

This is a full-stack project consisting of:
- **`backend/`**: Python 3.x, FastAPI, SQLAlchemy, LangChain/LangGraph, SQLite, Pytest.
- **`frontend/`**: Next.js (App Router), React 19, Tailwind CSS, TypeScript, Zustand.

## 1. Build, Lint, and Test Commands

Always execute commands within their respective directories (`cd backend` or `cd frontend` or use `workdir` param).

### Backend (`/backend`)
- **Install Dependencies**: `pip install -r requirements.txt`
- **Run Server**: `uvicorn main:app --reload`
- **Run All Tests**: `pytest tests/ -v`
- **Run a Specific Test File**: `pytest tests/test_validation_endpoint.py -v`
- **Run a Single Test Function**: `pytest tests/test_validation_endpoint.py::test_validation_success -v`
- **Run Tests with Print Output**: Add `-s` flag (e.g., `pytest tests/ -v -s`)

### Frontend (`/frontend`)
- **Install Dependencies**: `npm install`
- **Run Development Server**: `npm run dev`
- **Build Production**: `npm run build`
- **Run Linter**: `npm run lint`

## 2. Code Style Guidelines

### 2.1. Backend (Python/FastAPI)
- **Imports**: Group imports (standard library, third-party, local). Use absolute imports starting with `app.` (e.g., `from app.db.database import get_db`).
- **Formatting**: Adhere to PEP 8. Use standard 4-space indentation.
- **Types**: Use Python type hints extensively (`typing.Dict`, `List`, `Optional`, etc.). Use Pydantic models for request/response validation (located in `app.api.schemas`).
- **Naming Conventions**:
  - `snake_case` for variables, functions, and file names.
  - `PascalCase` for classes (e.g., SQLAlchemy models, Pydantic schemas).
  - UPPERCASE for constants.
- **Error Handling**: Use `try...except` blocks and log errors using the standard `logging` module. Raise FastAPI `HTTPException` with appropriate HTTP status codes for API errors.
- **Database**: Use SQLAlchemy ORM (`Session`, `Depends(get_db)`) for database interactions.

### 2.2. Frontend (Next.js/React)
- **Language**: Strictly TypeScript (`.ts`, `.tsx`). No plain JavaScript unless absolutely necessary for configuration files.
- **Imports**: Use path aliases (`@/components/...`, `@/lib/...`, `@/store/...`). Group external libraries first, then internal components, then utils/styles.
- **Components**: Write functional components using React Hooks. Use `'use client'` explicitly at the top of the file when utilizing hooks like `useState`, `useEffect`, or browser APIs.
- **Styling**: Use Tailwind CSS utility classes. Combine classes using the `cn()` utility (`clsx` + `tailwind-merge`) located in `@/lib/utils`.
- **State Management**: Use Zustand for global state (`useWorkflowStore`). Use Context API where strictly necessary.
- **Naming Conventions**:
  - `kebab-case` for component files (e.g., `onboarding-form.tsx`) to match existing conventions.
  - `PascalCase` for React components inside files.
  - `camelCase` for hooks (`useLanguage`), functions, and variables.

## 3. General Agentic Rules
- **Verify Before Modifying**: Use read tools to inspect files and context before proposing or writing code.
- **No Hallucinated Dependencies**: Do not introduce new libraries unless explicitly requested. Check `requirements.txt` or `package.json` first.
- **Absolute Paths**: When using file system tools (like read/write), always use absolute paths from the project root.
- **Tests**: When adding a backend feature, also write the corresponding test in `backend/tests/`.
