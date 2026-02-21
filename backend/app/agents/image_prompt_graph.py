"""
Image Prompt Workflow Module

Specialized LangGraph workflow for generating image generation prompts.
This workflow is designed specifically for creating prompts optimized for
DALL-E, Midjourney, and Stable Diffusion.
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


# --- Image Prompt Nodes ---

async def analyze_visual_requirements_node(state: PromptState) -> dict:
    """
    Analyzes user input for visual requirements.
    Identifies missing details about style, composition, lighting, etc.
    """
    try:
        from app.core.config_service import get_config_service

        user_input = state["user_input"]
        history = state.get("clarification_dialogue", [])

        # Check if user already answered questions
        has_user_answers = any(isinstance(msg, HumanMessage) for msg in history)

        if has_user_answers:
            logger.info("[IMAGE_CLARIFY] User answered. Processing requirements...")

            # Extract user answers
            user_answers = [msg.content for msg in history if isinstance(msg, HumanMessage)]

            return {
                "requirements": {
                    "has_questions": False,
                    "user_answers": user_answers,
                    "clarified": True
                },
                "clarification_dialogue": [
                    AIMessage(content="Gracias por tus respuestas. Generando tu image prompt ahora...")
                ]
            }

        # Get selected provider
        selected_provider = state.get("selected_provider", None)
        selected_model = state.get("selected_model", None)

        # Build conversation context
        conversation_text = f"User Initial Input: {user_input}\n\nHistory:\n"
        for msg in history:
            if isinstance(msg, HumanMessage):
                conversation_text += f"User: {msg.content}\n"
            elif isinstance(msg, AIMessage):
                conversation_text += f"Assistant: {msg.content}\n"

        # Get templates
        templates = get_node_templates(state)
        interaction_lang = get_interaction_language_name(state)

        # Build prompt
        prompt = templates["image_clarifier"].format(
            user_input=conversation_text,
            interaction_language=interaction_lang
        )

        # Get API key
        config_service = await get_config_service()
        api_key_info = await config_service.get_active_api_key(selected_provider)

        if not api_key_info:
            logger.error("No active API key found in analyze_visual_requirements_node")
            return {
                "requirements": {
                    "has_questions": True,
                    "questions": [
                        "Error: No hay API key activa configurada. Por favor, configure una API key en los ajustes."
                    ]
                },
                "clarification_dialogue": [
                    AIMessage(
                        content="Error: No hay API key activa configurada para el proveedor seleccionado."
                    )
                ]
            }

        # Call LLM
        try:
            result = await llm_call(
                prompt,
                model=state.get('selected_model') or api_key_info['model_preference'],
                api_key=api_key_info['api_key']
            )
        except Exception as e:
            logger.error(f"Error in llm_call from analyze_visual_requirements_node: {e}")
            return {
                "requirements": {
                    "has_questions": True,
                    "questions": [f"Error en la llamada al LLM: {str(e)}"]
                },
                "clarification_dialogue": [
                    AIMessage(content=f"Error en el paso de clarificación: {str(e)}")
                ]
            }

        # Check if questions exist
        questions = result.get("questions", [])

        if questions:
            return {
                "requirements": {
                    "questions": questions,
                    "has_questions": True
                },
                "clarification_dialogue": [AIMessage(content=json.dumps(questions))]
            }
        else:
            # No questions, we have requirements as a dict
            return {
                "requirements": {
                    **result,
                    "has_questions": False
                }
            }

    except Exception as e:
        logger.error(f"Unexpected error in analyze_visual_requirements_node: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {
            "requirements": {
                "has_questions": True,
                "questions": [f"Error inesperado: {str(e)}"]
            },
            "clarification_dialogue": [
                AIMessage(content=f"Error en el paso de clarificación: {str(e)}")
            ]
        }


async def optimize_for_platform_node(state: PromptState) -> dict:
    """
    Optimizes the image prompt for a specific platform (DALL-E, Midjourney, SD).
    Generates platform-specific keywords and technical parameters.
    """
    try:
        from app.core.config_service import get_config_service

        requirements = state["requirements"]
        selected_provider = state.get("selected_provider", None)
        selected_model = state.get("selected_model", None)

        # Determine target platform (default to DALL-E if not specified)
        target_platform = requirements.get("target_platform", "DALL-E")

        # Build requirements text
        reqs_text = f"Original Request: {state['user_input']}\n"
        for msg in state.get("clarification_dialogue", []):
            if isinstance(msg, HumanMessage):
                reqs_text += f"User Answer: {msg.content}\n"

        # Get templates
        templates = get_node_templates(state)
        interaction_lang = get_interaction_language_name(state)

        # Build prompt
        prompt = templates["image_platform"].format(
            base_prompt=reqs_text,
            platform=target_platform
        )

        # Get API key
        config_service = await get_config_service()
        api_key_info = await config_service.get_active_api_key(selected_provider)

        if not api_key_info:
            return {
                "platform_optimization": {
                    "error": "No API key available",
                    "optimized_prompt": "Error",
                    "platform_specific_keywords": [],
                    "technical_parameters": {},
                    "style_recommendations": []
                }
            }

        # Call LLM
        result = await llm_call(
            prompt,
            model=state.get('selected_model') or api_key_info['model_preference'],
            api_key=api_key_info['api_key']
        )

        return {"platform_optimization": result}

    except Exception as e:
        logger.error(f"Error in optimize_for_platform_node: {e}")
        return {
            "platform_optimization": {
                "error": str(e),
                "optimized_prompt": "Error",
                "platform_specific_keywords": [],
                "technical_parameters": {},
                "style_recommendations": []
            }
        }


async def include_negative_prompts_node(state: PromptState) -> dict:
    """
    Generates negative prompts to exclude unwanted elements.
    Identifies quality issues and elements to exclude.
    """
    try:
        from app.core.config_service import get_config_service

        base_prompt = state.get("platform_optimization", {}).get("optimized_prompt", "")
        selected_provider = state.get("selected_provider", None)
        selected_model = state.get("selected_model", None)

        # Get templates
        templates = get_node_templates(state)
        interaction_lang = get_interaction_language_name(state)

        # Build prompt
        prompt = templates["image_negative"].format(
            image_prompt=base_prompt
        )

        # Get API key
        config_service = await get_config_service()
        api_key_info = await config_service.get_active_api_key(selected_provider)

        if not api_key_info:
            return {
                "negative_prompt": {
                    "error": "No API key available",
                    "negative_prompt": "",
                    "excluded_elements": [],
                    "quality_keywords": [],
                    "explanation": "Error"
                }
            }

        # Call LLM
        result = await llm_call(
            prompt,
            model=state.get('selected_model') or api_key_info['model_preference'],
            api_key=api_key_info['api_key']
        )

        return {"negative_prompt": result}

    except Exception as e:
        logger.error(f"Error in include_negative_prompts_node: {e}")
        return {
            "negative_prompt": {
                "error": str(e),
                "negative_prompt": "",
                "excluded_elements": [],
                "quality_keywords": [],
                "explanation": f"Error: {str(e)}"
            }
        }


async def generate_image_prompt_node(state: PromptState) -> dict:
    """
    Consolidates all components into a final image prompt.
    Creates an optimized prompt with structure: [subject] [style] [lighting] [composition] [details]
    """
    try:
        from app.core.config_service import get_config_service

        requirements = state["requirements"]
        optimization = state.get("platform_optimization", {})
        negative = state.get("negative_prompt", {})
        selected_provider = state.get("selected_provider", None)
        selected_model = state.get("selected_model", None)

        # Determine platform
        platform = requirements.get("target_platform", "DALL-E")

        # Get templates
        templates = get_node_templates(state)
        interaction_lang = get_interaction_language_name(state)

        # Build prompt
        prompt = templates["image_generator"].format(
            base_prompt=str(requirements),
            optimization=str(optimization),
            negative_prompt=str(negative),
            additional_details=requirements.get("additional_details", ""),
            platform=platform,
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
                        "name": "Image Prompt",
                        "description": "Error: No API key",
                        "content": "Error: No hay API key activa configurada."
                    }
                ]
            }

        # Call LLM
        result = await llm_call(
            prompt,
            model=state.get('selected_model') or api_key_info['model_preference'],
            api_key=api_key_info['api_key']
        )

        # Return as a single variant (image prompt is single output)
        return {
            "generated_variants": [
                {
                    "id": "A",
                    "name": "Image Prompt",
                    "description": f"Optimized for {platform}",
                    "content": result.get("content", "")
                }
            ]
        }

    except Exception as e:
        logger.error(f"Error in generate_image_prompt_node: {e}")
        return {
            "generated_variants": [
                {
                    "id": "A",
                    "name": "Image Prompt",
                    "description": "Error",
                    "content": f"Error generando image prompt: {str(e)}"
                }
            ]
        }


# --- Graph Construction ---

def should_continue_image(state: PromptState) -> Literal["optimize_platform", END]:
    """
    Decides if we should proceed to optimization or wait for user input.
    """
    requirements = state.get("requirements", {})
    questions = requirements.get("questions", [])
    user_answers = requirements.get("user_answers", [])

    # If user answered, proceed
    if user_answers:
        logger.info("[IMAGE_SHOULD_CONTINUE] Usuario respondió. Procediendo a optimize_platform...")
        return "optimize_platform"

    # If questions and no answers, wait
    if questions and not user_answers:
        logger.info("[IMAGE_SHOULD_CONTINUE] Hay preguntas sin respuestas. Esperando...")
        return END

    # No questions, proceed
    logger.info("[IMAGE_SHOULD_CONTINUE] No hay preguntas. Procediendo...")
    return "optimize_platform"


# Build the graph
workflow = StateGraph(PromptState)

# Add nodes
workflow.add_node("analyze_visual_requirements", analyze_visual_requirements_node)
workflow.add_node("optimize_for_platform", optimize_for_platform_node)
workflow.add_node("include_negative_prompts", include_negative_prompts_node)
workflow.add_node("generate_image_prompt", generate_image_prompt_node)

# Add edges
workflow.set_entry_point("analyze_visual_requirements")

workflow.add_conditional_edges(
    "analyze_visual_requirements",
    should_continue_image,
    {
        "optimize_platform": "optimize_for_platform",
        END: END
    }
)

workflow.add_edge("optimize_for_platform", "include_negative_prompts")
workflow.add_edge("include_negative_prompts", "generate_image_prompt")
workflow.add_edge("generate_image_prompt", END)


# --- Compilation ---
def get_graph(checkpointer=None):
    """Returns the compiled image prompt workflow."""
    return workflow.compile(checkpointer=checkpointer)
