from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from litellm import completion, AuthenticationError, RateLimitError
import litellm
from app.db.database import get_db
from app.db.models import Settings, ApiKey
from app.core.security import security_service
from app.api.schemas import (
    SettingsCreate, ValidationRequest,
    ApiKeyCreate, ApiKeyResponse, ApiKeysListResponse, ValidationActiveResponse
)
from app.services.llm_engine import run_prompt_variant
from app.agents.graph import get_graph
from app.agents.state import PromptState
from typing import Dict, Any, List, Optional
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
import aiosqlite
from langchain_core.messages import HumanMessage
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

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
    Validates and then saves encrypted settings.
    Legacy endpoint - now uses ApiKey table.
    """
    try:
        # Validate provider
        valid_providers = ["openai", "anthropic", "ollama"]
        if settings_in.provider not in valid_providers:
            raise HTTPException(status_code=400, detail=f"Invalid provider: {settings_in.provider}")

        # Validate API key format
        if not settings_in.api_key or len(settings_in.api_key) < 10:
            raise HTTPException(status_code=400, detail="Invalid API key format")

        # Same logic as validate
        test_model = get_test_model(settings_in.provider, settings_in.model_preference)
        completion(
            model=test_model,
            messages=[{"role": "user", "content": "Test"}],
            api_key=settings_in.api_key,
            max_tokens=1
        )
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Validation failed: {str(e)}")

    # Encrypt
    encrypted_key = security_service.encrypt_key(settings_in.api_key)

    # Save to new ApiKey table (migration from old Settings)
    # First, try to save in new ApiKey table
    try:
        # Deactivate all existing keys for this provider
        db.query(ApiKey).filter(ApiKey.provider == settings_in.provider).update({"is_active": 0})

        # Create new API key
        new_key = ApiKey(
            user_id=None,
            provider=settings_in.provider,
            api_key_encrypted=encrypted_key,
            model_preference=settings_in.model_preference,
            is_active=1,
            usage_count=0,
            last_used_at=None
        )

        db.add(new_key)
        db.commit()

        logger.info(f"API key saved for provider: {settings_in.provider}")

        return {"status": "success", "message": "Settings saved securely"}

    except Exception as e:
        # Fallback to old Settings table if ApiKey fails
        logger.warning(f"Failed to save to ApiKey table, trying legacy Settings table: {e}")

        db_settings = db.query(Settings).first()
        if not db_settings:
            db_settings = Settings()
            db.add(db_settings)

        db_settings.provider = settings_in.provider
        db_settings.api_key_encrypted = encrypted_key
        db_settings.model_preference = settings_in.model_preference

        db.commit()
        db.refresh(db_settings)

        logger.info(f"API key saved to legacy Settings table for provider: {settings_in.provider}")

        return {"status": "success", "message": "Settings saved securely (legacy)"}


@router.get("/settings")
async def get_settings(db: Session = Depends(get_db)):
    """
    Retrieve settings (masking API key).
    Legacy endpoint - now uses ApiKey table.
    """
    # Try to get from new ApiKey table first
    try:
        active_key = db.query(ApiKey).filter(ApiKey.is_active == 1).first()

        if active_key:
            return {
                "configured": True,
                "provider": active_key.provider,
                "model_preference": active_key.model_preference,
                # Do not return the API key!
            }
    except Exception as e:
        logger.warning(f"Failed to query ApiKey table, trying legacy Settings: {e}")

    # Fallback to legacy Settings table
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
    This is a simplified list for prototype.
    """
    if provider == "openai":
        return ["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
    elif provider == "anthropic":
        return ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
    elif provider == "ollama":
        return ["llama3", "mistral", "gemma"]
    else:
        return ["default-model"]

# --- API Keys Management Endpoints (NEW) ---

@router.get("/settings/keys", response_model=ApiKeysListResponse)
async def list_api_keys(db: Session = Depends(get_db)):
    """
    List all API keys with their metadata.
    Does not expose encrypted keys.
    """
    try:
        keys = db.query(ApiKey).order_by(ApiKey.created_at.desc()).all()

        keys_response = [
            ApiKeyResponse(
                id=key.id,
                provider=key.provider,
                model_preference=key.model_preference,
                is_active=key.is_active == 1,
                usage_count=key.usage_count,
                created_at=key.created_at.isoformat() if key.created_at else "",
                updated_at=key.updated_at.isoformat() if key.updated_at else None
            )
            for key in keys
        ]

        logger.info(f"Listed {len(keys_response)} API keys")
        return ApiKeysListResponse(keys=keys_response)

    except Exception as e:
        logger.error(f"Error listing API keys: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/settings/keys", response_model=ApiKeyResponse)
async def create_api_key(key_data: ApiKeyCreate, db: Session = Depends(get_db)):
    """
    Add a new API key with validation.
    Validates the key with the provider before saving.
    """
    try:
        # Validate provider
        valid_providers = ["openai", "anthropic", "ollama"]
        if key_data.provider not in valid_providers:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid provider. Must be one of: {valid_providers}"
            )

        # Validate API key format (basic validation)
        if not key_data.api_key or len(key_data.api_key) < 10:
            raise HTTPException(status_code=400, detail="Invalid API key format")

        # Validate with the provider service
        try:
            test_model = get_test_model(key_data.provider, key_data.model_preference)
            completion(
                model=test_model,
                messages=[{"role": "user", "content": "Hello"}],
                api_key=key_data.api_key,
                max_tokens=5
            )
            logger.info(f"API key validated successfully for provider: {key_data.provider}")
        except AuthenticationError:
            logger.warning(f"Invalid API key for provider: {key_data.provider}")
            raise HTTPException(status_code=401, detail="Invalid API Key")
        except RateLimitError:
            raise HTTPException(status_code=429, detail="Rate limit exceeded or insufficient quota")
        except Exception as e:
            logger.error(f"API key validation error: {e}")
            raise HTTPException(status_code=400, detail=f"Validation failed: {str(e)}")

        # Encrypt the API key
        encrypted_key = security_service.encrypt_key(key_data.api_key)

        # Deactivate all existing keys for this provider
        db.query(ApiKey).filter(ApiKey.provider == key_data.provider).update({"is_active": 0})

        # Create new API key
        new_key = ApiKey(
            user_id=None,
            provider=key_data.provider,
            api_key_encrypted=encrypted_key,
            model_preference=key_data.model_preference,
            is_active=1,
            usage_count=0,
            last_used_at=None
        )

        db.add(new_key)
        db.commit()
        db.refresh(new_key)

        logger.info(f"New API key created for provider: {key_data.provider}, id: {new_key.id}")

        return ApiKeyResponse(
            id=new_key.id,
            provider=new_key.provider,
            model_preference=new_key.model_preference,
            is_active=new_key.is_active == 1,
            usage_count=new_key.usage_count,
            created_at=new_key.created_at.isoformat() if new_key.created_at else "",
            updated_at=new_key.updated_at.isoformat() if new_key.updated_at else None
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating API key: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/settings/keys/{key_id}")
async def delete_api_key(key_id: int, db: Session = Depends(get_db)):
    """
    Delete an API key with validation.
    Requires confirmation if it's the last active key.
    """
    try:
        # Get the key to delete
        key_to_delete = db.query(ApiKey).filter(ApiKey.id == key_id).first()

        if not key_to_delete:
            raise HTTPException(status_code=404, detail="API key not found")

        # Check if it's the last active key
        if key_to_delete.is_active == 1:
            active_keys_count = db.query(ApiKey).filter(ApiKey.is_active == 1).count()

            if active_keys_count == 1:
                # Check if there are any other keys (inactive)
                total_keys_count = db.query(ApiKey).count()

                if total_keys_count == 1:
                    return {
                        "requires_confirmation": True,
                        "message": "This is your only API key. If you delete it, you'll need to add a new one before using PromptForge.",
                        "warning": "no_keys_remaining"
                    }
                else:
                    return {
                        "requires_confirmation": True,
                        "message": "This is your last active API key. Are you sure you want to delete it?",
                        "warning": "last_active_key"
                    }

        # Log deletion for audit
        logger.info(f"Deleting API key id={key_id}, provider={key_to_delete.provider}")

        # Delete the key
        db.delete(key_to_delete)
        db.commit()

        return {
            "status": "success",
            "message": "API key deleted successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting API key: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/settings/keys/{key_id}/activate", response_model=ApiKeyResponse)
async def activate_api_key(key_id: int, db: Session = Depends(get_db)):
    """
    Activate a specific API key and deactivate others of the same provider.
    """
    try:
        # Get the key to activate
        key_to_activate = db.query(ApiKey).filter(ApiKey.id == key_id).first()

        if not key_to_activate:
            raise HTTPException(status_code=404, detail="API key not found")

        # Deactivate all keys of the same provider
        db.query(ApiKey).filter(
            ApiKey.provider == key_to_activate.provider,
            ApiKey.id != key_id
        ).update({"is_active": 0})

        # Activate the selected key
        key_to_activate.is_active = 1
        key_to_activate.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(key_to_activate)

        logger.info(f"Activated API key id={key_id}, provider={key_to_activate.provider}")

        return ApiKeyResponse(
            id=key_to_activate.id,
            provider=key_to_activate.provider,
            model_preference=key_to_activate.model_preference,
            is_active=key_to_activate.is_active == 1,
            usage_count=key_to_activate.usage_count,
            created_at=key_to_activate.created_at.isoformat() if key_to_activate.created_at else "",
            updated_at=key_to_activate.updated_at.isoformat() if key_to_activate.updated_at else None
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error activating API key: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/settings/validate-active", response_model=ValidationActiveResponse)
async def validate_active_keys(db: Session = Depends(get_db)):
    """
    Validate that there's at least one active API key.
    Returns active providers and warnings if applicable.
    """
    try:
        # Get active keys
        active_keys = db.query(ApiKey).filter(ApiKey.is_active == 1).all()
        active_providers = list(set([key.provider for key in active_keys]))

        # Get all providers (active + inactive)
        all_keys = db.query(ApiKey).all()
        all_providers = list(set([key.provider for key in all_keys]))

        warning = None
        if len(active_keys) == 0:
            if len(all_keys) > 0:
                warning = "No hay ninguna API key activa configurada. Por favor activa una para usar PromptForge."
            else:
                warning = "No hay ninguna API key configurada. Por favor configura una para usar PromptForge."

        logger.info(f"Validation: {len(active_keys)} active keys, providers: {active_providers}")

        return ValidationActiveResponse(
            has_active_key=len(active_keys) > 0,
            active_providers=active_providers,
            all_providers=all_providers,
            warning=warning
        )

    except Exception as e:
        logger.error(f"Error validating active keys: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def get_test_model(provider: str, model_preference: str = None) -> str:
    """
    Get the appropriate test model for validation based on provider.
    """
    test_models = {
        "openai": "gpt-3.5-turbo",
        "anthropic": "claude-3-haiku-20240307",
        "ollama": "llama3"
    }

    # If user specified a model preference and it's valid for the provider, use it
    if model_preference:
        valid_models = {
            "openai": ["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
            "anthropic": ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
            "ollama": ["llama3", "mistral", "gemma"]
        }
        if provider in valid_models and model_preference in valid_models[provider]:
            return model_preference

    return test_models.get(provider, "gpt-3.5-turbo")


# --- Endpoint: Listar Providers Activos (New) ---

@router.get("/settings/providers")
async def list_active_providers():
    """
    Lista todos los proveedores con API keys activas.
    Retorna información de modelos y contadores de uso.
    """
    from app.core.config_service import get_config_service

    try:
        config_service = await get_config_service()
        providers = await config_service.get_all_active_providers()

        logger.info(f"Listed {len(providers)} active providers")
        return {"providers": providers}

    except Exception as e:
        logger.error(f"Error listing providers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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

    # Try to retrieve API Key from new ApiKey table
    api_key = None
    model_preference = None

    try:
        active_key = db.query(ApiKey).filter(ApiKey.is_active == 1).first()

        if active_key and active_key.api_key_encrypted:
            api_key = security_service.decrypt_key(active_key.api_key_encrypted)
            model_preference = active_key.model_preference

            # Update usage count
            active_key.usage_count += 1
            active_key.last_used_at = datetime.utcnow()
            db.commit()

            logger.info(f"Using API key from ApiKey table, provider: {active_key.provider}")
        else:
            raise HTTPException(status_code=400, detail="No active API key found")

    except HTTPException:
        raise
    except Exception as e:
        logger.warning(f"Failed to get API key from ApiKey table, trying legacy Settings: {e}")

        # Fallback to legacy Settings table
        db_settings = db.query(Settings).first()
        if not db_settings or not db_settings.api_key_encrypted:
            raise HTTPException(status_code=400, detail="LLM Settings not configured")

        api_key = security_service.decrypt_key(db_settings.api_key_encrypted)
        model_preference = db_settings.model_preference

        logger.info(f"Using API key from legacy Settings table, provider: {db_settings.provider}")

    model_config = {
        "model": model_preference or "gpt-3.5-turbo",
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
