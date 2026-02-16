from pydantic import BaseModel, Field, model_validator
from typing import List, Dict, Any, Optional
from datetime import datetime
import warnings
import os

# Desactivar TODAS las advertencias de Pydantic que causan que el proceso se detenga
warnings.filterwarnings("ignore")
os.environ['PYTHONWARNINGS'] = 'ignore'

class SettingsCreate(BaseModel):
    provider: str
    api_key: str
    model_preference: str = "gpt-4-turbo"

class ValidationRequest(BaseModel):
    provider: str
    api_key: str

# --- API Keys Schemas (New) ---

class ApiKeyCreate(BaseModel):
    provider: str
    api_key: str
    model_preference: str

class ApiKeyResponse(BaseModel):
    id: int
    provider: str
    model_preference: str
    is_active: bool
    usage_count: int
    created_at: str
    updated_at: Optional[str] = None

    model_config = {"protected_namespaces": ()}

class ApiKeysListResponse(BaseModel):
    keys: List[ApiKeyResponse]

class ValidationActiveResponse(BaseModel):
    has_active_key: bool
    active_providers: List[str]
    all_providers: List[str]
    warning: Optional[str] = None

# --- Workflow Schemas ---

class WorkflowStartRequest(BaseModel):
    user_input: str
    provider: Optional[str] = None  # Proveedor seleccionado por el usuario

class WorkflowAnswerRequest(BaseModel):
    answer: str

class WorkflowResponse(BaseModel):
    thread_id: str
    status: str
    message: Optional[str] = None # Last generic message
    questions: List[str] = []
    variants: List[Dict[str, Any]] = []
    evaluations: Dict[str, Any] = {}
