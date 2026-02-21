"""
System Prompt Workflow Module

Specialized LangGraph workflow for generating system prompts.
This workflow is designed specifically for creating prompts that define
chatbot/assistant behavior, personality, and boundaries.
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


# --- System Prompt Nodes ---

async def analyze_system_requirements_node(state: PromptState) -> dict:
    """
    Analyzes user input for system prompt requirements.
    Identifies missing information about bot role, behavior, and boundaries.
    """
    try:
        from app.core.config_service import get_config_service

        user_input = state["user_input"]
        history = state.get("clarification_dialogue", [])

        # Check if user already answered questions
        has_user_answers = any(isinstance(msg, HumanMessage) for msg in history)

        if has_user_answers:
            logger.info("[SYSTEM_CLARIFY] User answered. Processing requirements...")

            # Extract user answers
            user_answers = [msg.content for msg in history if isinstance(msg, HumanMessage)]

            return {
                "requirements": {
                    "has_questions": False,
                    "user_answers": user_answers,
                    "clarified": True
                },
                "clarification_dialogue": [
                    AIMessage(content="Gracias por tus respuestas. Generando tu system prompt ahora...")
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
        prompt = templates["system_clarifier"].format(
            user_input=conversation_text,
            interaction_language=interaction_lang
        )

        # Get API key
        config_service = await get_config_service()
        api_key_info = await config_service.get_active_api_key(selected_provider)

        if not api_key_info:
            logger.error("No active API key found in analyze_system_requirements_node")
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
            logger.error(f"Error in llm_call from analyze_system_requirements_node: {e}")
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
        logger.error(f"Unexpected error in analyze_system_requirements_node: {e}")
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


async def define_bot_personality_node(state: PromptState) -> dict:
    """
    Defines the personality and tone of the bot based on requirements.
    Generates voice, tone, personality traits, and communication style.
    """
    try:
        from app.core.config_service import get_config_service

        requirements = state["requirements"]
        selected_provider = state.get("selected_provider", None)
        selected_model = state.get("selected_model", None)

        # Build requirements text
        reqs_text = f"Original Request: {state['user_input']}\n"
        for msg in state.get("clarification_dialogue", []):
            if isinstance(msg, HumanMessage):
                reqs_text += f"User Answer: {msg.content}\n"

        # Get templates
        templates = get_node_templates(state)
        interaction_lang = get_interaction_language_name(state)

        # Determine target tone from requirements
        target_tone = requirements.get("target_tone", "professional")

        # Build prompt
        prompt = templates["system_personality"].format(
            bot_requirements=reqs_text,
            target_tone=target_tone
        )

        # Get API key
        config_service = await get_config_service()
        api_key_info = await config_service.get_active_api_key(selected_provider)

        if not api_key_info:
            return {
                "bot_personality": {
                    "error": "No API key available",
                    "voice": "Error",
                    "tone": "Error",
                    "personality_traits": [],
                    "communication_style": "Error"
                }
            }

        # Call LLM
        result = await llm_call(
            prompt,
            model=state.get('selected_model') or api_key_info['model_preference'],
            api_key=api_key_info['api_key']
        )

        return {"bot_personality": result}

    except Exception as e:
        logger.error(f"Error in define_bot_personality_node: {e}")
        return {
            "bot_personality": {
                "error": str(e),
                "voice": "Error",
                "tone": "Error",
                "personality_traits": [],
                "communication_style": f"Error: {str(e)}"
            }
        }


async def set_behavior_boundaries_node(state: PromptState) -> dict:
    """
    Establishes behavior rules and constraints for the bot.
    Generates allowed behaviors, prohibited behaviors, and edge case handling.
    """
    try:
        from app.core.config_service import get_config_service

        requirements = state["requirements"]
        personality = state.get("bot_personality", {})
        selected_provider = state.get("selected_provider", None)
        selected_model = state.get("selected_model", None)

        # Get templates
        templates = get_node_templates(state)
        interaction_lang = get_interaction_language_name(state)

        # Build prompt
        prompt = templates["system_boundaries"].format(
            bot_requirements=str(requirements),
            personality_definition=str(personality)
        )

        # Get API key
        config_service = await get_config_service()
        api_key_info = await config_service.get_active_api_key(selected_provider)

        if not api_key_info:
            return {
                "bot_boundaries": {
                    "error": "No API key available",
                    "allowed_behaviors": [],
                    "prohibited_behaviors": [],
                    "information_limits": [],
                    "edge_case_handling": "Error"
                }
            }

        # Call LLM
        result = await llm_call(
            prompt,
            model=state.get('selected_model') or api_key_info['model_preference'],
            api_key=api_key_info['api_key']
        )

        return {"bot_boundaries": result}

    except Exception as e:
        logger.error(f"Error in set_behavior_boundaries_node: {e}")
        return {
            "bot_boundaries": {
                "error": str(e),
                "allowed_behaviors": [],
                "prohibited_behaviors": [],
                "information_limits": [],
                "edge_case_handling": f"Error: {str(e)}"
            }
        }


async def generate_system_prompt_node(state: PromptState) -> dict:
    """
    Consolidates all components into a final system prompt.
    Creates a professional, complete system prompt with role, personality, and boundaries.
    """
    try:
        from app.core.config_service import get_config_service

        requirements = state["requirements"]
        personality = state.get("bot_personality", {})
        boundaries = state.get("bot_boundaries", {})
        selected_provider = state.get("selected_provider", None)
        selected_model = state.get("selected_model", None)

        # Get templates
        templates = get_node_templates(state)
        interaction_lang = get_interaction_language_name(state)

        # Build bot role from requirements
        bot_role = requirements.get("bot_role", "AI Assistant")

        # Build prompt
        prompt = templates["system_generator"].format(
            bot_role=bot_role,
            personality=str(personality),
            boundaries=str(boundaries),
            additional_requirements=str(requirements.get("additional_requirements", "")),
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
                        "name": "System Prompt",
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

        # Return as a single variant (system prompt is single output)
        return {
            "generated_variants": [
                {
                    "id": "A",
                    "name": "System Prompt",
                    "description": "Custom system prompt for your chatbot/assistant",
                    "content": result.get("content", "")
                }
            ]
        }

    except Exception as e:
        logger.error(f"Error in generate_system_prompt_node: {e}")
        return {
            "generated_variants": [
                {
                    "id": "A",
                    "name": "System Prompt",
                    "description": "Error",
                    "content": f"Error generando system prompt: {str(e)}"
                }
            ]
        }


# --- Graph Construction ---

def should_continue_system(state: PromptState) -> Literal["define_personality", END]:
    """
    Decides if we should proceed to personality definition or wait for user input.
    """
    requirements = state.get("requirements", {})
    questions = requirements.get("questions", [])
    user_answers = requirements.get("user_answers", [])

    # If user answered, proceed
    if user_answers:
        logger.info("[SYSTEM_SHOULD_CONTINUE] Usuario respondió. Procediendo a define_personality...")
        return "define_personality"

    # If questions and no answers, wait
    if questions and not user_answers:
        logger.info("[SYSTEM_SHOULD_CONTINUE] Hay preguntas sin respuestas. Esperando...")
        return END

    # No questions, proceed
    logger.info("[SYSTEM_SHOULD_CONTINUE] No hay preguntas. Procediendo...")
    return "define_personality"


# Build the graph
workflow = StateGraph(PromptState)

# Add nodes
workflow.add_node("analyze_system_requirements", analyze_system_requirements_node)
workflow.add_node("define_bot_personality", define_bot_personality_node)
workflow.add_node("set_behavior_boundaries", set_behavior_boundaries_node)
workflow.add_node("generate_system_prompt", generate_system_prompt_node)

# Add edges
workflow.set_entry_point("analyze_system_requirements")

workflow.add_conditional_edges(
    "analyze_system_requirements",
    should_continue_system,
    {
        "define_personality": "define_bot_personality",
        END: END
    }
)

workflow.add_edge("define_bot_personality", "set_behavior_boundaries")
workflow.add_edge("set_behavior_boundaries", "generate_system_prompt")
workflow.add_edge("generate_system_prompt", END)


# --- Compilation ---
def get_graph(checkpointer=None):
    """Returns the compiled system prompt workflow."""
    return workflow.compile(checkpointer=checkpointer)
