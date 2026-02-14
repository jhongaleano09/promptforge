import litellm
from jinja2 import Template
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

async def run_prompt_variant(
    variant_text: str,
    prompt_type: str,
    input_data: Dict[str, Any],
    model_config: Dict[str, Any]
) -> str:
    """
    Executes a prompt variant against the configured LLM.

    Args:
        variant_text: The prompt template string.
        prompt_type: "normal" or "system".
        input_data: Dictionary of variables to inject into the template.
        model_config: Configuration for the LLM (model name, api_key, etc).

    Returns:
        The generated text response.
    """
    try:
        # 1. Variable Substitution (Jinja2)
        template = Template(variant_text)
        rendered_content = template.render(**input_data)

        messages = []
        
        # 2. Construct Payload based on Prompt Type
        if prompt_type == "system":
            # For System Prompts, the variant IS the system message.
            # We need a user input to test it against.
            user_input = input_data.get("user_test_input", "")
            if not user_input:
                logger.warning("System prompt execution requested without 'user_test_input'.")
            
            messages = [
                {"role": "system", "content": rendered_content},
                {"role": "user", "content": user_input}
            ]
        else:
            # For Normal Prompts, the variant is usually the user message or a template for it.
            # We assume the rendered content is the full prompt message for the user role.
            # Alternatively, if the prompt is a full conversation history, we'd need to parse it, 
            # but for now we assume it's a single prompt.
            messages = [
                {"role": "user", "content": rendered_content}
            ]

        # 3. Call LiteLLM
        response = await litellm.acompletion(
            model=model_config.get("model", "gpt-3.5-turbo"),
            api_key=model_config.get("api_key"),
            base_url=model_config.get("base_url"), # For OpenRouter, Ollama, etc.
            messages=messages,
            temperature=model_config.get("temperature", 0.7),
            max_tokens=model_config.get("max_tokens", 1000)
        )

        # 4. Extract Response
        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"Error executing prompt variant: {str(e)}")
        raise e
