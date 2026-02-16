# 06. Fase de Consolidación y Despliegue

**Objetivo:** Profesionalizar el repositorio para facilitar su adopción, colaboración y despliegue, asegurando que el proyecto sea accesible tanto para usuarios finales como para desarrolladores.

## 🧠 Estrategia Técnica
Esta fase no añade funcionalidades de negocio, sino que mejora la **Developer Experience (DX)** y la **infraestructura**. Se adopta un enfoque híbrido:
1.  **Docker:** Para "funcionar a la primera" (Usuarios/Demos).
2.  **Local:** Para desarrollo activo y debugging (Contribuidores).

---

## 🛠️ Tareas Técnicas Detalladas

### 6.1 Containerización (Docker)
Empaquetar la aplicación para eliminar el problema de "en mi máquina funciona".

- [ ] **Backend Dockerfile:**
    - Imagen base: `python:3.11-slim` (ligera).
    - Usuario: No-root (seguridad).
    - Dependencias: Instalación optimizada de `requirements.txt`.
    - Variables: Soporte para `DATABASE_URL` externa.
- [ ] **Frontend Dockerfile:**
    - Imagen base: `node:20-alpine`.
    - Build: **Multi-stage** (deps -> builder -> runner).
    - Modo: `output: "standalone"` en Next.js para reducir tamaño de imagen (requiere editar `next.config.ts`).
- [ ] **Orquestación (`docker-compose.yml`):**
    - Servicios: `backend`, `frontend`.
    - Redes: `promptforge-net` (aislamiento).
    - Volúmenes: Persistencia de SQLite en `./promptforge_data`.
    - Variables de Entorno: Inyección de `NEXT_PUBLIC_API_URL` al build time o runtime.
- [ ] **Archivos de Ignorados:**
    - Crear `.dockerignore` para evitar copiar `node_modules`, `venv`, `.git`, etc.

### 6.2 Documentación Maestra (`README.md`)
La carta de presentación del proyecto.

- [ ] **Estructura Separada (Clean UX):**
    - **`README.md` (Inglés):** Archivo principal por defecto.
    - **`README_ES.md` (Español):** Archivo separado completamente en español.
    - **Navegación:** En el encabezado de ambos archivos, poner enlaces claros tipo "tabs" (ej: `[ 🇬🇧 English ] [ 🇪🇸 Español ]`) para cambiar de idioma fácilmente sin scroll infinito.
- [ ] **Contenido Esencial (En ambos idiomas):**
    - **Badges:** Estado, Licencia.
    - **Elevator Pitch:** ¿Qué es y qué no es? (Calidad vs Cantidad).
    - **Arquitectura:** Diagrama textual (Mermaid o ASCII).
    - **Quick Start:** Comando `docker-compose up`.
    - **Dev Setup:** Guías paso a paso para Python/Node.
    - **Configuración:** Explicación de `.env` y API Keys.

### 6.3 Limpieza y Estandarización
- [ ] **Variables de Entorno y Puertos:**
    - Centralizar configuración.
    - **Puertos Configurables:** Modificar `docker-compose.yml` para permitir cambiar los puertos expuestos (ej: `8080:8000`) mediante variables de entorno (`APP_PORT`, `API_PORT`) para evitar conflictos con otros proyectos del usuario (puertos 3000/8000 son muy comunes).

---

## ❓ Decisiones de Implementación (Respuestas)
1.  **Persistencia:** Se confirma uso de **SQLite** con volumen local `./promptforge_data` (suficiente para ~100 iteraciones).
2.  **Puertos:** Se harán **configurables en el host** vía `.env` (ej: `PORT_FRONTEND=3005`), manteniendo defaults internos (3000/8000) para no romper la configuración del contenedor. Esto evita conflictos de "puerto en uso".
3.  **Hot Reload (Modo Producción vs Desarrollo):** 
    - **Decisión:** La imagen por defecto en Docker será **Producción (Optimizada)**.
    - *Razón:* El usuario final quiere "instalar y usar". No necesita que el servidor se reinicie al tocar archivos. Esto hace la imagen más ligera y rápida.
    - *Nota:* Si un desarrollador quiere Hot Reload, usará el setup local documentado.

---

## ✅ Buenas Prácticas a Seguir
-   **Seguridad:** Nunca correr contenedores como `root` si no es necesario.
-   **Eficiencia:** Usar `.dockerignore` es crítico para no enviar contextos de build gigantes (node_modules).
-   **Claridad:** El README debe asumir que el usuario **no sabe nada** del proyecto.
