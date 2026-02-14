from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from litellm import completion, AuthenticationError, RateLimitError
import litellm
from app.db.database import get_db
from app.db.models import Settings
from app.core.security import security_service
from app.api.schemas import SettingsCreate, ValidationRequest

router = APIRouter()

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
    # 1. Validate (Internal call logic or trust the frontend? Safer to re-validate or just save)
    # The requirement says: "Llama a validate internamente"
    
    # We can reuse the validation logic or call the function.
    # Let's just do the try/except block again to be safe and simple
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
    # In a real app, we might query the provider API using the stored key
    # or a key provided in headers.
    # For now, we return static lists based on provider.
    
    if provider == "openai":
        return ["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
    elif provider == "anthropic":
        return ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
    elif provider == "ollama":
        return ["llama3", "mistral", "gemma"]
    else:
        return ["default-model"]
