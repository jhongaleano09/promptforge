#!/bin/bash

# Script de prueba manual para el endpoint /api/settings/validate-test
# Fase 9: Validación de API Key de Test

echo "=== Prueba Manual del Endpoint de Validación de Test ==="
echo ""

BASE_URL="http://localhost:8002"
ENDPOINT="/api/settings/validate-test"

echo "1. Test: Proveedor no soportado (debe retornar 400)"
echo "---------------------------------------------------"
curl -X POST $BASE_URL$ENDPOINT \
  -H "Content-Type: application/json" \
  -d '{"provider":"invalid-provider","api_key":"test"}' \
  -s | python3 -m json.tool
echo ""
echo ""

echo "2. Test: API Key inválida de OpenAI (debe retornar 401)"
echo "-------------------------------------------------------"
curl -X POST $BASE_URL$ENDPOINT \
  -H "Content-Type: application/json" \
  -d '{"provider":"openai","api_key":"sk-invalid-key"}' \
  -s | python3 -m json.tool
echo ""
echo ""

echo "3. Test: Verificar que NO se guarda en BD"
echo "----------------------------------------"
echo "Antes de validar, verificar el número de API keys en la BD:"
sqlite3 ../database.sqlite "SELECT COUNT(*) as total FROM api_keys;" 2>/dev/null || echo "No se pudo contar"

echo ""
echo "Ejecutando validación de test..."
curl -X POST $BASE_URL$ENDPOINT \
  -H "Content-Type: application/json" \
  -d '{"provider":"anthropic","api_key":"sk-ant-test-fake"}' \
  -s > /dev/null

echo ""
echo "Después de validar, verificar el número de API keys en la BD:"
sqlite3 ../database.sqlite "SELECT COUNT(*) as total FROM api_keys;" 2>/dev/null || echo "No se pudo contar"
echo "(El número debe ser el mismo - NO debe incrementar)"

echo ""
echo ""

echo "4. Test: Verificar logs"
echo "----------------------"
echo "Últimas 5 líneas del log de validaciones:"
tail -5 ../logs/test_validations.log 2>/dev/null || echo "Log file not found"

echo ""
echo ""

echo "=== Prueba Manual Completada ==="
echo ""
echo "NOTAS:"
echo "- Para que este script funcione, el backend debe estar corriendo con:"
echo "  PROMPTFORGE_TEST_MODE=true python3 -m uvicorn main:app --port 8002"
echo "- Si el modo de test está deshabilitado, todos los tests retornarán 403"
echo ""
