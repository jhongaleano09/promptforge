"""
Additional Prompt Workflow Module

Specialized LangGraph workflow for improving existing prompts.
This workflow is designed specifically for analyzing, identifying weaknesses,
and generating improved versions of existing prompts.
"""

from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import json
import logging

from app.agents.state import PromptState
from app.prompts.helpers import get_node_templates, get_interaction_language_name
from litellm import acompletion

logger = logging.getLogger(__name__)


# --- Helpers (reused from nodes.py) ---

def parse_json_output(content: str) -> any:
    """Parses JSON content from LLM output, handling markdown code blocks."""
    content = content.strip()
    if content.startswith("```json"):
        content = content.split("```json")[1]
    if content.startswith("```"):
        content = content.split("```")[0]
    if content.endswith("```"):
        content = content.rsplit("```", 1)[0]
    return json.loads(content.strip())


async def llm_call(
    prompt: str,
    model: str = "gpt-3.5-turbo",
    api_key: str = None,
    json_mode: bool = True
) -> any:
    """Wrapper for LiteLLM call."""
    if not api_key:
        raise ValueError("API key is required")

    messages = [{"role": "user", "content": prompt}]

    response = await acompletion(
        model=model,
        messages=messages,
        api_key=api_key,
        response_format={"type": "json_object"} if json_mode else None
    )

    content = response.choices[0].message.content

    try:
        parsed = parse_json_output(content)
        logger.info(f"llm_call success: model={model}, parsed_type={type(parsed)}")
        return parsed
    except Exception as e:
        logger.error(f"llm_call parse error: {e}, content={content[:200]}...")
        raise


# --- Additional Prompt Nodes ---

async def analyze_original_prompt_node(state: PromptState) -> dict:
    """
    Analyzes an existing prompt to identify strengths and weaknesses.
    Evaluates clarity, completeness, and structure.
    """
    try:
        from app.core.config_service import get_config_service

        user_input = state["user_input"]

        # The user input should contain the original prompt
        original_prompt = user_input

        selected_provider = state.get("selected_provider", None)

        # Get templates
        templates = get_node_templates(state)
        interaction_lang = get_interaction_language_name(state)

        # Build prompt
        prompt = templates["additional_analyze"].format(
            original_prompt=original_prompt
        )

        # Get API key
        config_service = await get_config_service()
        api_key_info = await config_service.get_active_api_key(selected_provider)

        if not api_key_info:
            logger.error("No active API key found in analyze_original_prompt_node")
            return {
                "prompt_analysis": {
                    "error": "No API key available",
                    "strengths": [],
                    "weaknesses": [],
                    "clarity_score": 0,
                    "completeness_score": 0,
                    "potential_issues": ["No API key"],
                    "suggested_improvements": []
                }
            }

        # Call LLM
        try:
            result = await llm_call(
                prompt,
                model=api_key_info['model_preference'],
                api_key=api_key_info['api_key']
            )
        except Exception as e:
            logger.error(f"Error in llm_call from analyze_original_prompt_node: {e}")
            return {
                "prompt_analysis": {
                    "error": str(e),
                    "strengths": [],
                    "weaknesses": [f"Error: {str(e)}"],
                    "clarity_score": 0,
                    "completeness_score": 0,
                    "potential_issues": [],
                    "suggested_improvements": []
                }
            }

        return {"prompt_analysis": result}

    except Exception as e:
        logger.error(f"Unexpected error in analyze_original_prompt_node: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {
            "prompt_analysis": {
                "error": str(e),
                "strengths": [],
                "weaknesses": [f"Error inesperado: {str(e)}"],
                "clarity_score": 0,
                "completeness_score": 0,
                "potential_issues": [],
                "suggested_improvements": []
            }
        }


async def identify_weaknesses_node(state: PromptState) -> dict:
    """
    Identifies specific improvement areas in the prompt.
    Categorizes ambiguities, missing instructions, and structural issues.
    """
    try:
        from app.core.config_service import get_config_service

        user_input = state["user_input"]
        analysis = state.get("prompt_analysis", {})

        selected_provider = state.get("selected_provider", None)

        # Get templates
        templates = get_node_templates(state)
        interaction_lang = get_interaction_language_name(state)

        # Determine prompt purpose from user input context
        prompt_purpose = "General improvement"

        # Build prompt
        prompt = templates["additional_weakness"].format(
            original_prompt=user_input,
            analysis=str(analysis)
        )

        # Get API key
        config_service = await get_config_service()
        api_key_info = await config_service.get_active_api_key(selected_provider)

        if not api_key_info:
            return {
                "prompt_weaknesses": {
                    "error": "No API key available",
                    "ambiguities": [],
                    "missing_instructions": [],
                    "structure_issues": [],
                    "tone_issues": [],
                    "optimization_opportunities": []
                }
            }

        # Call LLM
        result = await llm_call(
            prompt,
            model=api_key_info['model_preference'],
            api_key=api_key_info['api_key']
        )

        return {"prompt_weaknesses": result}

    except Exception as e:
        logger.error(f"Error in identify_weaknesses_node: {e}")
        return {
            "prompt_weaknesses": {
                "error": str(e),
                "ambiguities": [],
                "missing_instructions": [],
                "structure_issues": [],
                "tone_issues": [],
                "optimization_opportunities": []
            }
        }


async def suggest_improvements_node(state: PromptState) -> dict:
    """
    Generates specific, actionable suggestions for improvement.
    Creates concrete improvements that address identified weaknesses.
    """
    try:
        from app.core.config_service import get_config_service

        user_input = state["user_input"]
        weaknesses = state.get("prompt_weaknesses", {})

        selected_provider = state.get("selected_provider", None)

        # Get templates
        templates = get_node_templates(state)
        interaction_lang = get_interaction_language_name(state)

        # Determine prompt purpose
        prompt_purpose = "General prompt improvement"

        # Build prompt
        prompt = templates["additional_improve"].format(
            original_prompt=user_input,
            weaknesses=str(weaknesses),
            prompt_purpose=prompt_purpose,
            target_language=interaction_lang
        )

        # Get API key
        config_service = await get_config_service()
        api_key_info = await config_service.get_active_api_key(selected_provider)

        if not api_key_info:
            return {
                "improvement_suggestions": {
                    "error": "No API key available",
                    "suggestions": []
                }
            }

        # Call LLM
        result = await llm_call(
            prompt,
            model=api_key_info['model_preference'],
            api_key=api_key_info['api_key']
        )

        return {"improvement_suggestions": result}

    except Exception as e:
        logger.error(f"Error in suggest_improvements_node: {e}")
        return {
            "improvement_suggestions": {
                "error": str(e),
                "suggestions": []
            }
        }


async def generate_refined_prompt_node(state: PromptState) -> dict:
    """
    Applies improvements to generate a refined version of the prompt.
    Creates an improved prompt that maintains original intent while applying fixes.
    """
    try:
        from app.core.config_service import get_config_service

        user_input = state["user_input"]
        suggestions = state.get("improvement_suggestions", {})

        selected_provider = state.get("selected_provider", None)

        # Get templates
        templates = get_node_templates(state)
        interaction_lang = get_interaction_language_name(state)

        # Build prompt
        prompt = templates["additional_generator"].format(
            original_prompt=user_input,
            suggestions=str(suggestions),
            user_context="",
            target_language=interaction_lang
        )

        # Get API key
        config_service = await get_config_service()
        api_key_info = await config_service.get_active_api_key(selected_provider)

        if not api_key_info:
            return {
                "generated_variants": [
                    {
                        "id": "A",
                        "name": "Refined Prompt",
                        "description": "Error: No API key",
                        "content": "Error: No hay API key activa configurada."
                    }
                ]
            }

        # Call LLM
        result = await llm_call(
            prompt,
            model=api_key_info['model_preference'],
            api_key=api_key_info['api_key']
        )

        # Return as a single variant (refined prompt is single output)
        return {
            "generated_variants": [
                {
                    "id": "A",
                    "name": "Refined Prompt",
                    "description": "Improved version of your original prompt",
                    "content": result.get("content", "")
                }
            ]
        }

    except Exception as e:
        logger.error(f"Error in generate_refined_prompt_node: {e}")
        return {
            "generated_variants": [
                {
                    "id": "A",
                    "name": "Refined Prompt",
                    "description": "Error",
                    "content": f"Error generando refined prompt: {str(e)}"
                }
            ]
        }


# --- Graph Construction ---

# Build the graph
workflow = StateGraph(PromptState)

# Add nodes
workflow.add_node("analyze_original_prompt", analyze_original_prompt_node)
workflow.add_node("identify_weaknesses", identify_weaknesses_node)
workflow.add_node("suggest_improvements", suggest_improvements_node)
workflow.add_node("generate_refined_prompt", generate_refined_prompt_node)

# Add edges
workflow.set_entry_point("analyze_original_prompt")

workflow.add_edge("analyze_original_prompt", "identify_weaknesses")
workflow.add_edge("identify_weaknesses", "suggest_improvements")
workflow.add_edge("suggest_improvements", "generate_refined_prompt")
workflow.add_edge("generate_refined_prompt", END)


# --- Compilation ---
def get_graph(checkpointer=None):
    """Returns the compiled additional prompt workflow."""
    return workflow.compile(checkpointer=checkpointer)
