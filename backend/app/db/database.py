from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

# Database will be created in the project root (one level up from backend)
# Or in the backend directory itself. The user requested "carpeta del proyecto".
# Let's put it in backend/ for simplicity of relative paths, or use absolute path.
# For now, let's store it in backend/database.sqlite to be safe with relative imports.

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.sqlite"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Import models to register them with Base.metadata
# This ensures that ApiKey table is created automatically
from app.db.models import Settings, ApiKey

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
