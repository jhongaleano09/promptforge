from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class SettingsCreate(BaseModel):
    provider: str
    api_key: str
    model_preference: str = "gpt-4-turbo"

class ValidationRequest(BaseModel):
    provider: str
    api_key: str

# --- Workflow Schemas ---

class WorkflowStartRequest(BaseModel):
    user_input: str

class WorkflowAnswerRequest(BaseModel):
    answer: str

class WorkflowResponse(BaseModel):
    thread_id: str
    status: str
    message: Optional[str] = None # Last generic message
    questions: List[str] = []
    variants: List[Dict[str, Any]] = []
    evaluations: Dict[str, Any] = {}
