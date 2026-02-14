from pydantic import BaseModel

class SettingsCreate(BaseModel):
    provider: str
    api_key: str
    model_preference: str = "gpt-4-turbo"

class ValidationRequest(BaseModel):
    provider: str
    api_key: str
