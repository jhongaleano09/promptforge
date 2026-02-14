import pytest
import sys
import os

# Add the backend directory to sys.path so we can import 'app'
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.prompts.service import PromptService

def test_clarifier_prompt_rendering_spanish():
    """Test that the clarifier prompt inserts user input and language correctly (Spanish Default)."""
    user_input = "Necesito un correo para ventas"
    prompt = PromptService.get_clarification_prompt(
        user_input=user_input,
        interaction_language="Spanish"
    )
    assert user_input in prompt
    assert "**These questions must be in Spanish.**" in prompt
    assert "Pregunta 1 (Spanish)?" in prompt
    assert "Output strictly in valid JSON format" in prompt

def test_clarifier_prompt_rendering_english():
    """Test that the clarifier prompt switches to English when requested."""
    user_input = "I need a sales email"
    prompt = PromptService.get_clarification_prompt(
        user_input=user_input,
        interaction_language="English"
    )
    assert user_input in prompt
    assert "**These questions must be in English.**" in prompt
    assert "Pregunta 1 (English)?" in prompt

def test_generator_prompt_rendering():
    """Test that the generator prompt handles context and target language."""
    requirements = "Escribir un poema sobre IA"
    prompt = PromptService.get_generation_prompt(
        clarified_requirements=requirements,
        prompt_type="creative",
        target_language="French"
    )
    assert requirements in prompt
    assert 'Prompt Type: "creative"' in prompt
    assert 'Target Language: "French"' in prompt
    assert "Variant A (The Direct/Concise)" in prompt
    assert "Variant B (Chain-of-Thought)" in prompt

def test_evaluator_prompt_rendering():
    """Test the evaluator prompt structure and language injection."""
    candidate = "Escribe un poema"
    requirements = "Debe rimar"
    prompt = PromptService.get_evaluation_prompt(
        candidate_prompt=candidate,
        original_requirements=requirements,
        interaction_language="German"
    )
    assert candidate in prompt
    assert requirements in prompt
    assert 'Interaction Language: "German"' in prompt
    assert "Score (1-10)" in prompt

def test_refiner_prompt_rendering():
    """Test the refiner prompt inputs."""
    original = "Prompt v1"
    feedback = "Too long"
    suggestions = "Shorten it"
    prompt = PromptService.get_refinement_prompt(
        original_prompt=original,
        evaluator_feedback=feedback,
        suggestions=suggestions,
        target_language="Spanish"
    )
    assert original in prompt
    assert feedback in prompt
    assert suggestions in prompt
    assert 'Target Language: "Spanish"' in prompt

def test_prompt_json_structure_validity():
    """
    Validation check: Ensure the output templates contain the JSON structure keywords.
    """
    prompt = PromptService.get_clarification_prompt("test")
    assert "{" in prompt and "}" in prompt
    assert '"ambiguities"' in prompt
