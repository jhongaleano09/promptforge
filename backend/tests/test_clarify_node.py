"""
Test for clarify_node to ensure it writes to the correct state field.

This test validates the fix for the critical bug where clarify_node was writing
to 'messages' instead of 'clarification_dialogue', causing empty responses in the UI.

Bug fix: Sprint 1, Tarea 1.3
"""

import pytest
import sys
import os
import json
from unittest.mock import AsyncMock, patch, MagicMock

# Add the backend directory to sys.path so we can import 'app'
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.agents.nodes import clarify_node
from app.agents.state import PromptState
from langchain_core.messages import AIMessage


@pytest.fixture
def mock_state():
    """Create a mock PromptState for testing."""
    return {
        "user_input": "Crea un logo para mi startup",
        "original_prompt": "Crea un logo para mi startup",
        "workflow_type": "clarification",
        "requirements": {},
        "user_preferences": {
            "language": "es",
            "name": None,
            "country": None
        },
        "llm_provider": "openai",
        "llm_model": "gpt-4"
    }


@pytest.fixture
def mock_llm_response():
    """Mock LLM response with clarification questions."""
    return {
        "questions": [
            "¿Cuál es el nombre de tu startup?",
            "¿A qué sector pertenece tu negocio?",
            "¿Tienes preferencia de colores?"
        ]
    }


@pytest.mark.asyncio
async def test_clarify_node_writes_to_correct_field(mock_state, mock_llm_response):
    """
    CRITICAL TEST: Verify that clarify_node writes to 'clarification_dialogue' field.
    
    This test validates the fix for the bug where users saw empty responses because
    clarify_node was writing to 'messages' but format_response was reading from
    'clarification_dialogue'.
    
    Expected behavior:
    - clarify_node should return dict with 'clarification_dialogue' key
    - The value should be a list containing an AIMessage
    - The AIMessage content should contain the JSON questions
    """
    
    # Mock the LLM call
    with patch('app.agents.nodes.llm_call') as mock_llm_call:
        mock_llm_call.return_value = mock_llm_response
        
        # We also need to mock config_service because clarify_node gets the active API key
        with patch('app.core.config_service.get_config_service') as mock_get_config:
            mock_config = AsyncMock()
            mock_config.get_active_api_key.return_value = {"api_key": "test_key", "model_preference": "test-model"}
            mock_get_config.return_value = mock_config

            # Execute clarify_node
            result = await clarify_node(mock_state)
        
        # CRITICAL ASSERTION: Must write to 'clarification_dialogue', NOT 'messages'
        assert "clarification_dialogue" in result, \
            "Bug detected! clarify_node should write to 'clarification_dialogue' field"
        
        # Verify 'messages' field is NOT used (old buggy behavior)
        assert "messages" not in result, \
            "Bug detected! clarify_node should NOT write to 'messages' field"
        
        # Verify the value is a list with at least one message
        assert isinstance(result["clarification_dialogue"], list), \
            "clarification_dialogue should be a list"
        assert len(result["clarification_dialogue"]) > 0, \
            "clarification_dialogue should contain at least one message"
        
        # Verify the first element is an AIMessage
        first_message = result["clarification_dialogue"][0]
        assert isinstance(first_message, AIMessage), \
            "clarification_dialogue should contain AIMessage objects"
        
        # Verify the message content contains valid JSON questions
        content = first_message.content
        assert content is not None and content != "", \
            "AIMessage content should not be empty"
        
        # Verify we can parse the JSON
        if isinstance(content, str):
            questions_data = json.loads(content)
        else:
            questions_data = content
            
        assert isinstance(questions_data, (list, dict)), \
            "Message content should be valid JSON"


@pytest.mark.asyncio
async def test_clarify_node_error_handling_writes_to_correct_field(mock_state):
    """
    Test that error handling also writes to 'clarification_dialogue'.
    
    When clarify_node encounters an error, it should still write the error message
    to the correct field so the user can see what went wrong.
    """
    
    # Mock LLM to raise an exception
    with patch('app.agents.nodes.llm_call') as mock_llm_call:
        mock_llm_call.side_effect = Exception("API key invalid")
        
        with patch('app.core.config_service.get_config_service') as mock_get_config:
            mock_config = AsyncMock()
            mock_config.get_active_api_key.return_value = {"api_key": "test_key", "model_preference": "test-model"}
            mock_get_config.return_value = mock_config

            # Execute clarify_node (should handle error gracefully)
            result = await clarify_node(mock_state)
        
        # Even in error state, should write to correct field
        assert "clarification_dialogue" in result, \
            "Error handling should also write to 'clarification_dialogue'"
        
        # Verify error message is present
        assert len(result["clarification_dialogue"]) > 0, \
            "Error message should be written to clarification_dialogue"
        
        error_message = result["clarification_dialogue"][0]
        assert isinstance(error_message, AIMessage), \
            "Error should be wrapped in AIMessage"
        
        error_content = str(error_message.content)
        assert "Error" in error_content or "error" in error_content.lower(), \
            "Error message should indicate an error occurred"


@pytest.mark.asyncio
async def test_clarify_node_requirements_structure(mock_state, mock_llm_response):
    """
    Test that clarify_node also correctly populates the requirements field.
    
    The requirements field should contain:
    - has_questions: True (when questions exist)
    - questions: list of question strings
    """
    
    with patch('app.agents.nodes.llm_call') as mock_llm_call:
        mock_llm_call.return_value = mock_llm_response
        
        with patch('app.core.config_service.get_config_service') as mock_get_config:
            mock_config = AsyncMock()
            mock_config.get_active_api_key.return_value = {"api_key": "test_key", "model_preference": "test-model"}
            mock_get_config.return_value = mock_config

            result = await clarify_node(mock_state)
        
        # Verify requirements structure
        assert "requirements" in result, \
            "Result should contain requirements field"
        
        requirements = result["requirements"]
        assert requirements.get("has_questions") is True, \
            "has_questions should be True when questions exist"
        
        assert "questions" in requirements, \
            "requirements should contain questions list"
        
        assert isinstance(requirements["questions"], list), \
            "questions should be a list"
        
        assert len(requirements["questions"]) > 0, \
            "questions list should not be empty"


@pytest.mark.asyncio
async def test_clarify_node_integration_with_format_response(mock_state, mock_llm_response):
    """
    Integration test: Verify that the output of clarify_node can be correctly
    read by format_response.
    
    This simulates the actual workflow where clarify_node writes to state
    and format_response reads from it.
    """
    
    with patch('app.agents.nodes.llm_call') as mock_llm_call:
        mock_llm_call.return_value = mock_llm_response
        
        with patch('app.core.config_service.get_config_service') as mock_get_config:
            mock_config = AsyncMock()
            mock_config.get_active_api_key.return_value = {"api_key": "test_key", "model_preference": "test-model"}
            mock_get_config.return_value = mock_config

            # Execute clarify_node
            clarify_result = await clarify_node(mock_state)
        
        # Simulate state update (LangGraph would do this automatically)
        updated_state = {**mock_state, **clarify_result}
        
        # Verify format_response can read from clarification_dialogue
        dialogue = updated_state.get("clarification_dialogue", [])
        
        assert len(dialogue) > 0, \
            "format_response should be able to read clarification_dialogue from state"
        
        last_message = dialogue[-1]
        assert isinstance(last_message, AIMessage), \
            "Last message should be AIMessage type"
        
        assert last_message.content != "", \
            "Message content should not be empty (this was the original bug!)"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
