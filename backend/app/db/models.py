from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, Index
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
