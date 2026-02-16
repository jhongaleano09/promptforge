from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

# Database will be created in:///backend/database.sqlite to be safe with relative paths.
# For now, let's store it in backend/database.sqlite to be safe with relative imports.

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.sqlite"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import models to register them with Base.metadata AFTER Base is defined
# This avoids circular imports
from app.db.models import Settings, ApiKey
