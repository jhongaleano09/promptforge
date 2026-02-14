from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from litellm import completion, AuthenticationError, RateLimitError
import litellm
from app.db.database import get_db
from app.db.models import Settings
from app.core.security import security_service
from app.api.schemas import SettingsCreate, ValidationRequest
from app.services.llm_engine import run_prompt_variant
from app.agents.graph import get_graph
from app.agents.state import PromptState
from typing import Dict, Any, List
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
import aiosqlite
from langchain_core.messages import HumanMessage

router = APIRouter()

# ... (Existing settings endpoints) ...

@router.post("/settings/validate")
async def validate_settings(request: ValidationRequest):
    """
    Validates the API key by making a small request to the LLM provider.
    """
    try:
        # Simple test message
        messages = [{"role": "user", "content": "Hello"}]
        
        # We assume the model to test against based on provider or a default
        # Ideally this should be dynamic, but for validation we can pick a cheap one
        test_model = "gpt-3.5-turbo" if request.provider == "openai" else "claude-3-haiku-20240307"
        if request.provider == "anthropic":
             test_model = "claude-3-haiku-20240307"
        
        # Attempt completion
        response = completion(
            model=test_model,
            messages=messages,
            api_key=request.api_key,
            max_tokens=5
        )
        
        return {"status": "success", "message": "API Key is valid"}

    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded or insufficient quota")
    except Exception as e:
        # In a real scenario, check for timeout specifically if needed
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/settings/save")
async def save_settings(settings_in: SettingsCreate, db: Session = Depends(get_db)):
    """
    Validates and then saves the encrypted settings.
    """
    try:
        # Same logic as validate
        test_model = "gpt-3.5-turbo" if settings_in.provider == "openai" else "claude-3-haiku-20240307"
        completion(
            model=test_model,
            messages=[{"role": "user", "content": "Test"}],
            api_key=settings_in.api_key,
            max_tokens=1
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Validation failed: {str(e)}")

    # 2. Encrypt
    encrypted_key = security_service.encrypt_key(settings_in.api_key)

    # 3. Save to DB
    # Check if settings exist (single user app?)
    # Assuming single user configuration for now
    db_settings = db.query(Settings).first()
    if not db_settings:
        db_settings = Settings()
        db.add(db_settings)
    
    db_settings.provider = settings_in.provider
    db_settings.api_key_encrypted = encrypted_key
    db_settings.model_preference = settings_in.model_preference
    
    db.commit()
    db.refresh(db_settings)
    
    return {"status": "success", "message": "Settings saved securely"}

@router.get("/settings")
async def get_settings(db: Session = Depends(get_db)):
    """
    Retrieve settings (masking the API key).
    """
    db_settings = db.query(Settings).first()
    if not db_settings:
        return {"configured": False}
    
    return {
        "configured": True,
        "provider": db_settings.provider,
        "model_preference": db_settings.model_preference,
        # Do not return the API key!
    }

@router.get("/models")
async def list_models(provider: str):
    """
    Returns a list of available models for the given provider.
    This is a simplified list for the prototype.
    """
    if provider == "openai":
        return ["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
    elif provider == "anthropic":
        return ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
    elif provider == "ollama":
        return ["llama3", "mistral", "gemma"]
    else:
        return ["default-model"]

# --- Arena & Workflow Endpoints ---

@router.post("/arena/execute")
async def execute_prompt_variant(
    payload: Dict[str, Any], 
    db: Session = Depends(get_db)
):
    """
    Executes a single prompt variant against the configured LLM.
    Payload: { "variant_text": "...", "prompt_type": "...", "input_data": {...} }
    """
    variant_text = payload.get("variant_text")
    prompt_type = payload.get("prompt_type", "normal")
    input_data = payload.get("input_data", {})

    if not variant_text:
        raise HTTPException(status_code=400, detail="Missing variant_text")

    # Retrieve API Key
    db_settings = db.query(Settings).first()
    if not db_settings or not db_settings.api_key_encrypted:
        raise HTTPException(status_code=400, detail="LLM Settings not configured")

    api_key = security_service.decrypt_key(db_settings.api_key_encrypted)
    model_config = {
        "model": db_settings.model_preference or "gpt-3.5-turbo",
        "api_key": api_key,
        "base_url": None # Add base_url logic if supporting other providers
    }

    try:
        result = await run_prompt_variant(
            variant_text=variant_text,
            prompt_type=prompt_type,
            input_data=input_data,
            model_config=model_config
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/workflow/{thread_id}/update_test_results")
async def update_test_results(
    thread_id: str,
    payload: Dict[str, Any]
):
    """
    Updates the state with test results (test_inputs, test_outputs).
    """
    # In a real app with LangGraph Cloud or persistent checkpointer, we'd update state here.
    # For this local prototype using SQLite checkpointer, we need to access the checkpointer.
    # This requires dependency injection of the checkpointer which is async.
    # For simplicity, we might just pass the results in the next run call.
    return {"status": "simulated_update", "message": "State update logic pending integration"}

@router.post("/workflow/{thread_id}/run")
async def run_workflow(
    thread_id: str,
    payload: Dict[str, Any]
):
    """
    Runs or resumes the workflow.
    Payload: { "user_input": "...", "selected_variant": "...", "user_feedback": "..." }
    """
    user_input = payload.get("user_input")
    selected_variant = payload.get("selected_variant")
    user_feedback = payload.get("user_feedback")

    # Inputs for the graph
    inputs = {}
    if user_input:
        inputs["user_input"] = user_input
    
    # If refining, we inject selected_variant and feedback into state
    if selected_variant:
        inputs["selected_variant"] = selected_variant
    if user_feedback:
        inputs["user_feedback"] = user_feedback

    # Config for checkpointer
    config = {"configurable": {"thread_id": thread_id}}

    # Initialize Checkpointer & Graph
    async with aiosqlite.connect("database.sqlite") as conn:
        checkpointer = AsyncSqliteSaver(conn)
        # Initialize the checkpointer tables if they don't exist
        await checkpointer.setup()
        
        graph = get_graph(checkpointer)

        # Run the graph
        # streaming mode is better for long running processes, 
        # but for simple request/response we can use ainvoke if quick.
        # However, clarifier might stop.
        
        final_state = await graph.ainvoke(inputs, config=config)
        
        return {
            "state": final_state,
            "thread_id": thread_id,
            "next": "evaluate" if selected_variant else "clarify_result" 
        }
