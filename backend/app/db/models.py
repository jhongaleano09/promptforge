from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, Index, Boolean, Text
from sqlalchemy.sql import func
from app.db.database import Base

class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, default="openai")
    api_key_encrypted = Column(LargeBinary, nullable=False)
    model_preference = Column(String, default="gpt-4-turbo")


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True, index=True)
    provider = Column(String, nullable=False, index=True)
    api_key_encrypted = Column(LargeBinary, nullable=False)
    model_preference = Column(String, default="gpt-4-turbo")
    is_active = Column(Integer, default=1, nullable=False)
    usage_count = Column(Integer, default=0)
    last_used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('idx_provider_active', 'provider', 'is_active'),
    )


class UserPreferences(Base):
    """
    User profile and preferences table.
    Single-user application: should only contain ONE row.

    Stores:
    - language: UI and agent interaction language ('spanish' or 'english')
    - name: User's name (optional)
    - country: User's country (optional)
    - default_provider: Default LLM provider ('openai', 'anthropic', 'ollama')
    - default_model: Default model preference
    - auto_save_preferences: Automatically save preferences changes
    - theme: UI theme ('light' or 'dark')
    """
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String, default="spanish", nullable=False)
    name = Column(String, nullable=True)
    country = Column(String, nullable=True)
    default_provider = Column(String, default="openai", nullable=False)
    default_model = Column(String, default="gpt-4-turbo", nullable=False)
    auto_save_preferences = Column(Boolean, default=True, nullable=False)
    theme = Column(String, default="light", nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class PromptTemplate(Base):
    """
    Prompt templates library table.
    Stores pre-built templates for different prompt types.

    Stores:
    - type: Template type ('system', 'image', 'additional')
    - name: Template name
    - description: Template description
    - template_content: Template content with placeholders
    - category: Template category (e.g., 'customer-service', 'creative-writing')
    - tags: JSON array of tags
    - is_public: Whether template is public (vs private)
    - usage_count: Times template has been used
    """
    __tablename__ = "prompt_templates"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    template_content = Column(Text, nullable=False)
    category = Column(String(50), nullable=True)
    tags = Column(String, nullable=True)
    is_public = Column(Boolean, default=True, nullable=False)
    usage_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('idx_type_category', 'type', 'category'),
    )
