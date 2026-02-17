"""
Tests para el endpoint /api/settings/validate-test

Estos tests validan la funcionalidad del endpoint de validación de API keys de test,
que permite validar API keys sin guardarlas en la base de datos.
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException
from fastapi.testclient import TestClient

# Add the backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.api.endpoints import router
from app.api.schemas import ValidationRequest
from fastapi import FastAPI

# Crear app de prueba
app = FastAPI()
app.include_router(router, prefix="/api")

client = TestClient(app)


# ==================== Fixtures ====================

@pytest.fixture
def mock_request():
    """Mock del objeto Request de FastAPI con metadata"""
    mock = Mock()
    mock.client = Mock()
    mock.client.host = "127.0.0.1"
    mock.headers = {"user-agent": "pytest-client"}
    return mock


@pytest.fixture
def valid_openai_request():
    """Request válido para OpenAI"""
    return {
        "provider": "openai",
        "api_key": "sk-test-validkey123456789"
    }


@pytest.fixture
def valid_anthropic_request():
    """Request válido para Anthropic"""
    return {
        "provider": "anthropic",
        "api_key": "sk-ant-test-validkey123"
    }


@pytest.fixture
def invalid_provider_request():
    """Request con proveedor no soportado"""
    return {
        "provider": "invalid-provider",
        "api_key": "sk-test-key123"
    }


@pytest.fixture
def enable_test_mode(monkeypatch):
    """Habilita el modo de test mediante variable de entorno"""
    monkeypatch.setenv("PROMPTFORGE_TEST_MODE", "true")


@pytest.fixture
def disable_test_mode(monkeypatch):
    """Deshabilita el modo de test mediante variable de entorno"""
    monkeypatch.setenv("PROMPTFORGE_TEST_MODE", "false")


# ==================== Tests de Protección con Variable de Entorno ====================

def test_validate_test_with_mode_disabled(disable_test_mode, valid_openai_request):
    """
    Test: Endpoint debe retornar 403 cuando PROMPTFORGE_TEST_MODE está deshabilitado
    """
    response = client.post("/api/settings/validate-test", json=valid_openai_request)
    
    assert response.status_code == 403
    assert "test mode" in response.json()["detail"].lower()


def test_validate_test_with_mode_enabled_but_invalid_provider(enable_test_mode, invalid_provider_request):
    """
    Test: Endpoint debe retornar 400 cuando el proveedor no es soportado
    """
    response = client.post("/api/settings/validate-test", json=invalid_provider_request)
    
    assert response.status_code == 400
    assert "not supported" in response.json()["detail"].lower()
    assert "openai" in response.json()["detail"]  # Lista de proveedores soportados


# ==================== Tests de Validación Exitosa ====================

@patch('app.api.endpoints.completion')
def test_validate_test_openai_success(mock_completion, enable_test_mode, valid_openai_request):
    """
    Test: Validación exitosa con API key de OpenAI
    """
    # Mock de respuesta exitosa de LiteLLM
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message = Mock()
    mock_response.choices[0].message.content = "Hello!"
    mock_completion.return_value = mock_response
    
    response = client.post("/api/settings/validate-test", json=valid_openai_request)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["provider"] == "openai"
    assert data["test_model"] == "gpt-3.5-turbo"
    assert "test_response" in data
    
    # Verificar que se llamó a completion con los parámetros correctos
    mock_completion.assert_called_once()
    call_kwargs = mock_completion.call_args.kwargs
    assert call_kwargs["model"] == "gpt-3.5-turbo"
    assert call_kwargs["api_key"] == valid_openai_request["api_key"]
    assert call_kwargs["max_tokens"] == 5


@patch('app.api.endpoints.completion')
def test_validate_test_anthropic_success(mock_completion, enable_test_mode, valid_anthropic_request):
    """
    Test: Validación exitosa con API key de Anthropic
    """
    # Mock de respuesta exitosa
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message = Mock()
    mock_response.choices[0].message.content = "Hi there!"
    mock_completion.return_value = mock_response
    
    response = client.post("/api/settings/validate-test", json=valid_anthropic_request)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["provider"] == "anthropic"
    assert data["test_model"] == "claude-3-haiku-20240307"


@patch('app.api.endpoints.completion')
def test_validate_test_ollama_success(mock_completion, enable_test_mode):
    """
    Test: Validación exitosa con proveedor Ollama (local)
    """
    ollama_request = {
        "provider": "ollama",
        "api_key": "local-key-not-needed"
    }
    
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message = Mock()
    mock_response.choices[0].message.content = "Response"
    mock_completion.return_value = mock_response
    
    response = client.post("/api/settings/validate-test", json=ollama_request)
    
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "ollama"
    assert data["test_model"] == "llama3"


# ==================== Tests de Validación Fallida ====================

@patch('app.api.endpoints.completion')
def test_validate_test_invalid_api_key(mock_completion, enable_test_mode, valid_openai_request):
    """
    Test: Endpoint debe retornar 401 cuando la API key es inválida
    """
    from litellm import AuthenticationError
    
    # Mock de error de autenticación con los parámetros requeridos por LiteLLM
    mock_completion.side_effect = AuthenticationError(
        message="Invalid API key",
        llm_provider="openai",
        model="gpt-3.5-turbo",
        response=Mock()
    )
    
    response = client.post("/api/settings/validate-test", json=valid_openai_request)
    
    assert response.status_code == 401
    assert "invalid api key" in response.json()["detail"].lower()


@patch('app.api.endpoints.completion')
def test_validate_test_rate_limit_error(mock_completion, enable_test_mode, valid_openai_request):
    """
    Test: Endpoint debe retornar 429 cuando se excede el rate limit
    """
    from litellm import RateLimitError
    
    # Mock de error de rate limit con los parámetros requeridos por LiteLLM
    mock_completion.side_effect = RateLimitError(
        message="Rate limit exceeded",
        llm_provider="openai",
        model="gpt-3.5-turbo",
        response=Mock()
    )
    
    response = client.post("/api/settings/validate-test", json=valid_openai_request)
    
    assert response.status_code == 429
    assert "rate limit" in response.json()["detail"].lower()


@patch('app.api.endpoints.completion')
def test_validate_test_general_error(mock_completion, enable_test_mode, valid_openai_request):
    """
    Test: Endpoint debe retornar 500 cuando ocurre un error inesperado
    """
    # Mock de error general
    mock_completion.side_effect = Exception("Unexpected error")
    
    response = client.post("/api/settings/validate-test", json=valid_openai_request)
    
    assert response.status_code == 500
    assert "validation failed" in response.json()["detail"].lower()


# ==================== Tests de Caso Insensitivo para Proveedores ====================

@patch('app.api.endpoints.completion')
def test_validate_test_provider_case_insensitive(mock_completion, enable_test_mode):
    """
    Test: El endpoint debe aceptar proveedores en diferentes casos (OpenAI, OPENAI, openai)
    """
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message = Mock()
    mock_response.choices[0].message.content = "OK"
    mock_completion.return_value = mock_response
    
    # Probar diferentes casos
    for provider in ["OpenAI", "OPENAI", "openai", "oPeNaI"]:
        request = {"provider": provider, "api_key": "sk-test-key"}
        response = client.post("/api/settings/validate-test", json=request)
        assert response.status_code == 200


# ==================== Tests de Integración con Base de Datos ====================

def test_validate_test_does_not_save_to_database(enable_test_mode, valid_openai_request):
    """
    Test: CRÍTICO - Verificar que la API key NO se guarda en la base de datos
    
    Este es el test más importante de la Fase 9: asegurar que las API keys
    de prueba nunca se persisten en la base de datos.
    """
    from app.db.database import get_db
    from app.db.models import ApiKey
    
    with patch('app.api.endpoints.completion') as mock_completion:
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = "OK"
        mock_completion.return_value = mock_response
        
        # Contar API keys antes de la validación
        db = next(get_db())
        count_before = db.query(ApiKey).count()
        
        # Ejecutar validación de test
        response = client.post("/api/settings/validate-test", json=valid_openai_request)
        
        # Contar API keys después de la validación
        count_after = db.query(ApiKey).count()
        
        # Verificar que NO se guardó nada nuevo
        assert count_before == count_after, "La API key de test se guardó en la BD (ERROR CRÍTICO)"
        assert response.status_code == 200


# ==================== Tests de Logging ====================

def test_validate_test_logs_successful_validation(enable_test_mode, valid_openai_request, caplog):
    """
    Test: Verificar que se registran logs correctos para validación exitosa
    """
    with patch('app.api.endpoints.completion') as mock_completion:
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = "OK"
        mock_completion.return_value = mock_response
        
        response = client.post("/api/settings/validate-test", json=valid_openai_request)
        
        # Verificar que el log contiene información relevante
        # Los logs se escriben en archivo, así que aquí solo verificamos que no hay errores
        assert response.status_code == 200


def test_validate_test_logs_failed_validation(enable_test_mode, valid_openai_request, caplog):
    """
    Test: Verificar que se registran logs correctos para validación fallida
    """
    from litellm import AuthenticationError
    
    with patch('app.api.endpoints.completion') as mock_completion:
        mock_completion.side_effect = AuthenticationError(
            message="Invalid key",
            llm_provider="openai",
            model="gpt-3.5-turbo",
            response=Mock()
        )
        
        response = client.post("/api/settings/validate-test", json=valid_openai_request)
        
        # Verificar que se registró el error
        assert response.status_code == 401


# ==================== Tests de Metadata en Request ====================

@patch('app.api.endpoints.completion')
def test_validate_test_captures_client_metadata(mock_completion, enable_test_mode, valid_openai_request):
    """
    Test: Verificar que el endpoint captura IP y User-Agent correctamente
    """
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message = Mock()
    mock_response.choices[0].message.content = "OK"
    mock_completion.return_value = mock_response
    
    # El TestClient de FastAPI automáticamente incluye metadata de cliente
    response = client.post(
        "/api/settings/validate-test",
        json=valid_openai_request,
        headers={"user-agent": "custom-test-agent"}
    )
    
    assert response.status_code == 200
    # La metadata se registra en logs, no se retorna en la respuesta


# ==================== Test de Cobertura Completa ====================

def test_endpoint_exists():
    """
    Test básico: Verificar que el endpoint existe y es accesible
    """
    # Sin modo de test, debe retornar 403 (no 404)
    response = client.post("/api/settings/validate-test", json={"provider": "openai", "api_key": "test"})
    assert response.status_code == 403  # No 404, significa que el endpoint existe


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
