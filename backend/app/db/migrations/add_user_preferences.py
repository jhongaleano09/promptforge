"""
Migration: Add user_preferences table

This migration creates the user_preferences table and inserts
an initial row with default values for the single-user application.

Run this script directly or import and call run_migration()
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.db.database import Base, engine as db_engine
from app.db.models import UserPreferences
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_migration():
    """
    Execute the migration to add user_preferences table.
    
    Steps:
    1. Create all tables (if not exist)
    2. Check if user_preferences is empty
    3. Insert initial row with default values
    """
    # Use the engine from database.py
    engine = db_engine
    
    logger.info("=" * 60)
    logger.info("Starting migration: add_user_preferences")
    logger.info("=" * 60)
    
    # Create all tables defined in models
    logger.info("Creating tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    logger.info("✓ Tables created successfully")
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if user_preferences table has data
        existing_count = db.query(UserPreferences).count()
        logger.info(f"Found {existing_count} rows in user_preferences table")
        
        if existing_count == 0:
            # Insert initial row with default values
            logger.info("Inserting initial user preferences row...")
            initial_prefs = UserPreferences(
                language="spanish",  # Default language
                name=None,
                country=None
            )
            db.add(initial_prefs)
            db.commit()
            logger.info("✓ Initial preferences row created successfully")
            logger.info(f"  - ID: {initial_prefs.id}")
            logger.info(f"  - Language: {initial_prefs.language}")
        else:
            logger.info("User preferences already exist, skipping insert")
        
        # Validate: ensure only one row exists (single-user constraint)
        final_count = db.query(UserPreferences).count()
        if final_count > 1:
            logger.warning(f"⚠ WARNING: Found {final_count} rows in user_preferences. Expected 1.")
            logger.warning("  This is a single-user application. Consider cleaning extra rows.")
        else:
            logger.info(f"✓ Validation passed: {final_count} row in user_preferences")
        
        logger.info("=" * 60)
        logger.info("Migration completed successfully!")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"✗ Migration failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_migration()
