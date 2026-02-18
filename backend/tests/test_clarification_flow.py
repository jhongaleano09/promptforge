"""
Test manual del flujo de clarificación para debugging.

Este test simula el flujo completo:
1. Usuario envía prompt inicial
2. Sistema genera preguntas de clarificación
3. Usuario responde a las preguntas
4. Sistema debería generar el prompt final
"""

import pytest
import sys
import os
import json
from httpx import AsyncClient

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.agents.nodes import clarify_node, generate_node
from app.agents.state import PromptState
from langchain_core.messages import HumanMessage, AIMessage


@pytest.mark.asyncio
async def test_full_clarification_flow():
    """
    Test completo del flujo de clarificación.
    
    Flujo esperado:
    1. Usuario envía prompt inicial
    2. Clarify genera preguntas
    3. Usuario responde a preguntas
    4. Workflow detecta respuestas y genera prompt final
    
    Este test debe revelar dónde se queda congelado el flujo.
    """
    
    client = AsyncClient(base_url="http://localhost:8001/api")
    
    # Paso 1: Iniciar workflow con prompt inicial
    print("\n=== PASO 1: Iniciar workflow ===")
    start_response = await client.post(
        "/workflow/stream/start",
        json={
            "user_input": "Crea un logo para mi startup de tecnología",
            "provider": "openai",
            "prompt_type": "basic"
        },
        timeout=30.0
    )
    
    assert start_response.status_code == 200
    start_data = start_response.json()
    
    print(f"✓ Workflow iniciado")
    print(f"  Thread ID: {start_data.get('thread_id')}")
    print(f"  Status: {start_data.get('status')}")
    print(f"  Message: {start_data.get('message', '')[:100]}...")
    print(f"  Questions: {start_data.get('questions', [])}")
    
    # Deberíamos tener preguntas
    questions = start_data.get('questions', [])
    assert len(questions) > 0, "Debería haber preguntas de clarificación"
    print(f"✓ Se generaron {len(questions)} preguntas")
    
    # Paso 2: Simular respuesta del usuario
    print("\n=== PASO 2: Responder a preguntas ===")
    thread_id = start_data['thread_id']
    
    # Simular respuesta del usuario (una respuesta consolidada)
    user_answer = "Startup se llama 'TechVision', sector es SaaS, colores azul y verde minimalista"
    
    print(f"Enviando respuesta al thread {thread_id}...")
    answer_response = await client.post(
        f"/workflow/{thread_id}/answer",
        json={"answer": user_answer},
        timeout=60.0
    )
    
    assert answer_response.status_code == 200
    answer_data = answer_response.json()
    
    print(f"✓ Respuesta enviada")
    print(f"  Status después de respuesta: {answer_data.get('status')}")
    print(f"  Message: {answer_data.get('message', '')[:100]}...")
    print(f"  Variants: {len(answer_data.get('variants', []))}")
    
    # Paso 3: Verificar que el workflow continuó
    print("\n=== PASO 3: Verificar resultado ===")
    
    # Si el flujo funciona, deberíamos tener variants generadas
    variants = answer_data.get('variants', [])
    
    if len(variants) > 0:
        print(f"✅ ÉXITO: Se generaron {len(variants)} variantes")
        print(f"  Status final: {answer_data.get('status')}")
        for i, variant in enumerate(variants):
            print(f"  Variant {i+1}: {variant.get('content', '')[:50]}...")
    else:
        print(f"❌ FALLÓ: No se generaron variantes")
        print(f"  Status final: {answer_data.get('status')}")
        print(f"  Message: {answer_data.get('message', '')}")
        
        # Diagnóstico
        if answer_data.get('status') == 'clarifying':
            print("\n⚠️  DIAGNÓSTICO: Workflow está atascado en 'clarifying'")
            print("El workflow generó preguntas nuevamente en lugar de procesar respuestas")
            print("Posible causa: clarify_node no detecta respuestas del usuario")
    
    return answer_data


def test_clarify_node_with_answer_history():
    """
    Test unitario: Verificar qué hace clarify_node cuando hay respuestas.
    """
    
    async def _test():
        # Estado simulado después de que usuario responde
        state = {
            "original_prompt": "Crea un logo",
            "user_input": "Crea un logo",
            "workflow_type": "clarification",
            "clarification_dialogue": [
                AIMessage(content='["¿Cuál es el nombre?", "¿Qué sector?"]'),
                HumanMessage(content="Se llama TechVision, sector SaaS")
            ],
            "user_preferences": {
                "language": "es",
                "name": None,
                "country": None
            },
            "llm_provider": "openai",
            "llm_model": "gpt-4"
        }
        
        print("\n=== Testing clarify_node con respuestas en historial ===")
        print(f"Historial tiene {len(state['clarification_dialogue'])} mensajes")
        
        # El nodo debería detectar que hay respuestas y proceder a generar
        # NO debería generar más preguntas
        
        # Mock LLM para ver qué hace el nodo
        from unittest.mock import AsyncMock, patch
        
        mock_llm = AsyncMock()
        mock_response = json.dumps({
            "questions": ["¿Nombre?", "¿Sector?"]
        })
        mock_llm.ainvoke.return_value.content = mock_response
        
        with patch('app.agents.nodes.llm_call', return_value=mock_llm.ainvoke.return_value):
            result = await clarify_node(state)
        
        print(f"Resultado de clarify_node:")
        print(f"  requirements.has_questions: {result['requirements']['has_questions']}")
        print(f"  requirements.questions: {result['requirements'].get('questions', [])}")
        print(f"  clarification_dialogue: {len(result.get('clarification_dialogue', []))} mensajes")
        
        # DIAGNÓSTICO: Si has_questions es True, el nodo generó NUEVAS preguntas
        # Si debería haber sido False para proceder a generate
        
        if result['requirements']['has_questions']:
            print("\n❌ BUG DETECTADO:")
            print("El nodo generó preguntas nuevamente en lugar de procesar las respuestas")
            print("Expected: has_questions=False para proceder a generate")
            print("Actual: has_questions=True, genera más preguntas → workflow se queda en loop")
        else:
            print("\n✅ CORRECTO:")
            print("El nodo detectó que hay suficientes respuestas")
            print("Expected: has_questions=False, procede a generate")
        
        return result
    
    import asyncio
    return asyncio.run(_test())


if __name__ == "__main__":
    import asyncio
    
    print("="*70)
    print("TEST DEL FLUJO DE CLARIFICACIÓN")
    print("="*70)
    print("\nEste test simula el flujo completo para identificar dónde")
    print("se queda congelado el workflow cuando el usuario responde.")
    print("="*70 + "\n")
    
    # Test unitario (no requiere servidor corriendo)
    print("Test 1: Unitario - Qué hace clarify_node con respuestas?")
    print("-" * 70)
    test_clarify_node_with_answer_history()
    
    # Test de integración (requiere servidor corriendo)
    print("\n\nTest 2: Integración - Flujo completo con servidor real")
    print("-" * 70)
    print("Requiere servidor backend corriendo en http://localhost:8001")
    print("\nSi el servidor no está corriendo, este test fallará.")
    
    try:
        asyncio.run(test_full_clarification_flow())
    except Exception as e:
        print(f"\n❌ Error en test: {e}")
        print("\nPosibles causas:")
        print("1. Servidor no está corriendo")
        print("2. No hay API key configurada")
        print("3. Timeout del servidor")
        sys.exit(1)
