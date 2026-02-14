import json
import asyncio
from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from app.agents.state import PromptState
from app.prompts.templates import CLARIFIER_TEMPLATE, GENERATOR_TEMPLATE, EVALUATOR_TEMPLATE
from litellm import acompletion

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

async def llm_call(prompt: str, model: str = "gpt-3.5-turbo", json_mode: bool = True) -> Any:
    """
    Wrapper for LiteLLM call.
    """
    # In a real scenario, we would get the model from config/env
    messages = [{"role": "user", "content": prompt}]
    response = await acompletion(
        model=model,
        messages=messages,
        response_format={"type": "json_object"} if json_mode else None
    )
    content = response.choices[0].message.content
    return parse_json_output(content)

# --- Nodes ---

async def clarify_node(state: PromptState):
    """
    Analyzes user input, asks clarifying questions, or extracts final requirements.
    """
    user_input = state["user_input"]
    history = state.get("clarification_dialogue", [])
    
    # Construct conversation history string for the prompt context
    conversation_text = f"User Initial Input: {user_input}\n\nHistory:\n"
    for msg in history:
        if isinstance(msg, HumanMessage):
            conversation_text += f"User: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            conversation_text += f"Assistant: {msg.content}\n"
            
    # Prepare Prompt
    # We default to English for interaction unless detected otherwise, 
    # but the template has {interaction_language}. 
    # For MVP we assume 'Spanish' as per the prompt instructions implies a Spanish context?
    # The user prompts are in Spanish. Let's default to Spanish for interaction.
    prompt = CLARIFIER_TEMPLATE.format(
        user_input=conversation_text,
        interaction_language="Spanish" 
    )
    
    # Call LLM
    try:
        result = await llm_call(prompt, model="gpt-4o") # Using a smart model for reasoning
    except Exception as e:
        # Fallback or error handling
        return {"messages": [AIMessage(content="Error in clarification step.")]}

    # Logic: If questions exist, we must ask them.
    questions = result.get("questions", [])
    
    if questions:
        # We have questions. 
        # We add the questions to the history (as AIMessage) so the user sees them.
        # But we also need to return them in a structured way if needed.
        # For LangGraph state updates:
        return {
            "requirements": result, # Temporary storage of partial analysis
            "messages": [AIMessage(content=json.dumps(questions))] # Store questions in history
        }
    else:
        # No questions, we have requirements.
        return {
            "requirements": result, # This should contain the final analysis
            # We don't add a message here because we are moving to the next step
        }

async def generate_node(state: PromptState):
    """
    Generates 3 variants in parallel.
    """
    requirements = state["requirements"]
    
    # Extract details from requirements analysis
    # The Clarifier output format is: { "ambiguities": [], "questions": [], "detected_type": "..." }
    # But if it finished, it might just be the analysis. 
    # Ideally, the Clarifier should output a summary of requirements when done.
    # For now, we use the conversation history + initial input as the "clarified requirements" context.
    
    # To improve quality, we might want to have the Clarifier output a "Summary" field in the last step.
    # Let's assume the 'user_input' + 'clarification_dialogue' is enough context, 
    # OR we re-ask the Clarifier to summarize. 
    # For MVP speed, let's just pass the conversation.
    
    clarified_reqs_str = f"Original Request: {state['user_input']}\n"
    for msg in state.get("clarification_dialogue", []):
         if isinstance(msg, HumanMessage):
            clarified_reqs_str += f"User Answer: {msg.content}\n"
    
    prompt_type = requirements.get("detected_type", "normal")
    target_lang = "Spanish" # Defaulting to Spanish per project context
    
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
    
    tasks = []
    for persona in personas:
        prompt = GENERATOR_TEMPLATE.format(
            clarified_requirements=clarified_reqs_str,
            prompt_type=prompt_type,
            target_language=target_lang,
            persona_name=persona["name"],
            persona_description=persona["description"]
        )
        tasks.append(llm_call(prompt, model="gpt-4o"))
        
    results = await asyncio.gather(*tasks)
    
    # Add IDs to results
    for i, res in enumerate(results):
        res["id"] = personas[i]["id"]
        
    return {
        "generated_variants": results
    }

async def evaluate_node(state: PromptState):
    """
    Evaluates the 3 generated variants.
    """
    variants = state["generated_variants"]
    # We re-construct requirements string similarly
    clarified_reqs_str = f"Original Request: {state['user_input']}\n"
    
    evaluations = {}
    
    tasks = []
    variant_ids = []
    
    for variant in variants:
        prompt = EVALUATOR_TEMPLATE.format(
            original_requirements=clarified_reqs_str,
            candidate_prompt=variant["content"],
            interaction_language="Spanish"
        )
        tasks.append(llm_call(prompt, model="gpt-4o"))
        variant_ids.append(variant["id"])
        
    results = await asyncio.gather(*tasks)
    
    for i, res in enumerate(results):
        evaluations[variant_ids[i]] = res
        
    return {
        "evaluations": evaluations
    }
