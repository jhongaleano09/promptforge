#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
  cp .env.example .env
fi

if [ -f ".env" ]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

if docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD="docker-compose"
else
  echo "Docker Compose not found. Install Docker Desktop and try again."
  exit 1
fi

$COMPOSE_CMD up -d --build

APP_PORT_DISPLAY="${APP_PORT:-3000}"
API_PORT_DISPLAY="${API_PORT:-8000}"

echo "PromptForge is running:"
echo "Frontend: http://localhost:${APP_PORT_DISPLAY}"
echo "Backend Docs: http://localhost:${API_PORT_DISPLAY}/docs"
