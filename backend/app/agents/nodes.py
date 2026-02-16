import json
import asyncio
import logging
from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from app.agents.state import PromptState
from app.prompts.templates import CLARIFIER_TEMPLATE, GENERATOR_TEMPLATE, EVALUATOR_TEMPLATE, JUDGE_TEMPLATE, REFINER_TEMPLATE
from litellm import acompletion

logger = logging.getLogger(__name__)

# --- Helpers ---

def parse_json_output(content: str) -> Any:
    """
    Parses JSON content from LLM output, handling markdown code blocks.
    """
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
) -> Any:
    """
    Wrapper for LiteLLM call.
    """
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
        logger.info(f"llm_call success: model={model}, parsed_type={type(parsed)}, keys={list(parsed.keys()) if isinstance(parsed, dict) else 'not dict'}")
        return parsed
    except Exception as e:
        logger.error(f"llm_call parse error: {e}, content={content[:200]}...")
        raise

# --- Nodes ---

async def clarify_node(state: PromptState):
    """
    Analyzes user input, asks clarifying questions, or extracts final requirements.
    """
    from app.core.config_service import get_config_service

    user_input = state["user_input"]
    history = state.get("clarification_dialogue", [])

    # Obtener provider del estado (si fue especificado)
    selected_provider = state.get("selected_provider", None)

    # Construct conversation history string for the prompt context
    conversation_text = f"User Initial Input: {user_input}\n\nHistory:\n"
    for msg in history:
        if isinstance(msg, HumanMessage):
            conversation_text += f"User: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            conversation_text += f"Assistant: {msg.content}\n"

    # Prepare Prompt
    prompt = CLARIFIER_TEMPLATE.format(
        user_input=conversation_text,
        interaction_language="Spanish"
    )

    # Obtener API key activa del provider seleccionado
    config_service = await get_config_service()
    api_key_info = await config_service.get_active_api_key(selected_provider)

    if not api_key_info:
        return {
            "messages": [AIMessage(content="Error: No hay API key activa configurada para el proveedor seleccionado.")]
        }

    # Call LLM con API key
    try:
        result = await llm_call(
            prompt,
            model=api_key_info['model_preference'],
            api_key=api_key_info['api_key']
        )
    except Exception as e:
        return {"messages": [AIMessage(content=f"Error en el paso de clarificación: {str(e)}")]}

    # Logic: If questions exist, we must ask them.
    questions = result.get("questions", [])

    if questions:
        # When there are questions, store them separately and store requirements as a dict
        return {
            "requirements": {
                "questions": questions,
                "has_questions": True
            },
            "messages": [AIMessage(content=json.dumps(questions))]
        }
    else:
        # No questions, we have requirements as a dict
        return {
            "requirements": {
                **result,
                "has_questions": False
            }
        }

async def generate_node(state: PromptState):
    """
    Generates 3 variants in parallel.
    """
    from app.core.config_service import get_config_service

    # Log input state for debugging
    logger.info(f"generate_node input state keys: {list(state.keys())}")
    logger.info(f"requirements type: {type(state.get('requirements'))}, value: {state.get('requirements')}")

    requirements = state["requirements"]

    # Obtener provider seleccionado
    selected_provider = state.get("selected_provider", None)

    clarified_reqs_str = f"Original Request: {state['user_input']}\n"
    for msg in state.get("clarification_dialogue", []):
         if isinstance(msg, HumanMessage):
            clarified_reqs_str += f"User Answer: {msg.content}\n"

    prompt_type = requirements.get("detected_type", "normal")
    target_lang = "Spanish"

    # Define Personas
    personas = [
        {
            "id": "A",
            "name": "Direct & Concise",
            "description": "Focus on brevity, minimal fluff, token efficiency. Ideal for speed."
        },
        {
            "id": "B",
            "name": "Chain of Thought",
            "description": "Instructs model to think step-by-step. Great for reasoning and complex logic."
        },
        {
            "id": "C",
            "name": "Few-Shot / Contextual",
            "description": "Robust definition, includes examples (placeholders), extensive context."
        }
    ]

    # Obtener API key activa
    config_service = await get_config_service()
    api_key_info = await config_service.get_active_api_key(selected_provider)

    if not api_key_info:
        return {
            "messages": [AIMessage(content="Error: No hay API key activa configurada.")]
        }

    tasks = []
    for persona in personas:
        prompt = GENERATOR_TEMPLATE.format(
            clarified_requirements=clarified_reqs_str,
            prompt_type=prompt_type,
            target_language=target_lang,
            persona_name=persona["name"],
            persona_description=persona["description"]
        )
        # Usar API key y modelo del provider
        tasks.append(llm_call(
            prompt,
            model=api_key_info['model_preference'],
            api_key=api_key_info['api_key']
        ))

    logger.info(f"Starting {len(tasks)} llm_call tasks for generation")
    results = await asyncio.gather(*tasks)
    logger.info(f"llm_call results received: {len(results)} results")

    # Add IDs to results and ensure correct format
    formatted_results = []
    for i, res in enumerate(results):
        try:
            logger.info(f"Processing result {i}: type={type(res)}, keys={list(res.keys()) if isinstance(res, dict) else 'not dict'}")

            if isinstance(res, dict):
                res["id"] = personas[i]["id"]
                # Ensure that result has a 'content' field
                if "content" not in res:
                    # Try to find content in description or use whole result
                    if "description" in res:
                        res["content"] = res["description"]
                    else:
                        res["content"] = json.dumps(res)  # Fallback: use entire JSON
                formatted_results.append(res)
            else:
                logger.error(f"Result {i} is not a dict, it's a {type(res)}: {str(res)[:200]}")
        except Exception as e:
            logger.error(f"Error processing result {i}: {e}")
            formatted_results.append({
                "id": personas[i]["id"],
                "name": personas[i]["name"],
                "description": personas[i]["description"],
                "content": f"Error: {str(e)}"
            })

    logger.info(f"Generated {len(formatted_results)} variants with format: {[type(r) for r in formatted_results]}")

    result_state = {
        "generated_variants": formatted_results
    }

    logger.info(f"generate_node returning state with generated_variants type: {type(result_state['generated_variants'])}, len={len(formatted_results)}")

    return result_state

async def evaluate_node(state: PromptState):
    """
    Evaluates 3 generated variants.
    """
    from app.core.config_service import get_config_service

    variants = state.get("generated_variants", [])

    # Obtener provider seleccionado
    selected_provider = state.get("selected_provider", None)

    # Obtener API key activa
    config_service = await get_config_service()
    api_key_info = await config_service.get_active_api_key(selected_provider)

    if not api_key_info:
        return {
            "messages": [AIMessage(content="Error: No hay API key activa configurada.")]
        }

    # Log variants for debugging
    logger.info(f"evaluate_node: variants type={type(variants)}, len={len(variants)}, variants={variants[:1] if variants else 'empty'}")

    clarified_reqs_str = f"Original Request: {state['user_input']}\n"

    evaluations = {}

    tasks = []
    variant_ids = []

    for variant in variants:
        try:
            if not isinstance(variant, dict):
                logger.error(f"Variant is not a dict: {type(variant)}, value={str(variant)[:200]}")
                continue

            content = variant.get("content", "")
            if not content:
                logger.error(f"Variant missing 'content' field: {variant}")
                continue

            prompt = EVALUATOR_TEMPLATE.format(
                original_requirements=clarified_reqs_str,
                candidate_prompt=content,
                interaction_language="Spanish"
            )
            tasks.append(llm_call(
                prompt,
                model=api_key_info['model_preference'],
                api_key=api_key_info['api_key']
            ))
            variant_ids.append(variant.get("id", ""))
        except Exception as e:
            logger.error(f"Error preparing evaluation task: {e}")
            continue

    if not tasks:
        logger.error("No valid evaluation tasks were created")
        return {
            "evaluations": {}
        }

    results = await asyncio.gather(*tasks)

    for i, res in enumerate(results):
        if i < len(variant_ids):
            evaluations[variant_ids[i]] = res

    return {
        "evaluations": evaluations
    }

async def judge_node(state: PromptState):
    """
    Analyzes execution results and selects a winner.
    """
    from app.core.config_service import get_config_service

    test_outputs = state.get("test_outputs", {})
    test_inputs = state.get("test_inputs", {})

    # Obtener provider seleccionado
    selected_provider = state.get("selected_provider", None)

    # Obtener API key activa
    config_service = await get_config_service()
    api_key_info = await config_service.get_active_api_key(selected_provider)

    if not api_key_info:
        return {
            "judge_result": {"error": "No hay API key activa configurada."}
        }

    # Construct input for Judge
    user_test_input = test_inputs.get("user_test_input", "")
    if not user_test_input and test_inputs:
         user_test_input = str(list(test_inputs.values())[0])

    if not test_outputs:
        return {"judge_result": {"error": "No test outputs to judge"}}

    output_a = test_outputs.get("A", "No output generated")
    output_b = test_outputs.get("B", "No output generated")
    output_c = test_outputs.get("C", "No output generated")

    prompt = JUDGE_TEMPLATE.format(
        original_intent=state["user_input"],
        test_input=user_test_input,
        output_a=output_a,
        output_b=output_b,
        output_c=output_c
    )

    try:
        result = await llm_call(
            prompt,
            model=api_key_info['model_preference'],
            api_key=api_key_info['api_key']
        )
    except Exception as e:
        return {"judge_result": {"error": f"Judge failed: {str(e)}"}}

    return {
        "judge_result": result
    }

async def refiner_node(state: PromptState):
    """
    Generates new variants based on feedback.
    """
    from app.core.config_service import get_config_service

    selected_variant_id = state.get("selected_variant")

    if not selected_variant_id:
        return {
            "messages": [AIMessage(content="Error: No variant selected for refinement.")]
        }

    # Obtener provider seleccionado
    selected_provider = state.get("selected_provider", None)

    # Obtener API key activa
    config_service = await get_config_service()
    api_key_info = await config_service.get_active_api_key(selected_provider)

    if not api_key_info:
        return {
            "messages": [AIMessage(content="Error: No hay API key activa configurada.")]
        }

    # Find content of selected variant
    selected_content = ""
    for v in state.get("generated_variants", []):
        if v["id"] == selected_variant_id:
            selected_content = v["content"]
            break

    user_feedback = state.get("user_feedback", "Improve this.")

    # Re-construct context
    original_context = f"Original Request: {state['user_input']}"

    prompt = REFINER_TEMPLATE.format(
        seed_prompt=selected_content,
        user_feedback=user_feedback,
        original_context=original_context
    )

    try:
        result = await llm_call(
            prompt,
            model=api_key_info['model_preference'],
            api_key=api_key_info['api_key']
        )
        new_variants = result.get("variations", [])

        return {
            "generated_variants": new_variants,
            "evaluations": {},
            "test_outputs": {},
            "judge_result": {}
        }

    except Exception as e:
         return {
             "messages": [AIMessage(content=f"Error en refinamiento: {str(e)}")]
         }
