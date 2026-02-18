"""
Migration: Add new fields to user_preferences table

This migration adds the following fields to the user_preferences table:
- default_provider: Default LLM provider ('openai', 'anthropic', 'ollama')
- default_model: Default model preference
- auto_save_preferences: Automatically save preferences changes
- theme: UI theme ('light' or 'dark')

Run this script to apply the migration:
    python backend/migrations/add_preferences_fields.py
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import text
from app.db.database import engine, Base, get_db
from app.db.models import UserPreferences
import logging

logger = logging.getLogger(__name__)


def add_preferences_fields():
    """
    Add new fields to user_preferences table.

    The script will:
    1. Check if new fields already exist
    2. Add ALTER TABLE statements for missing fields
    3. Set default values for existing rows
    """
    try:
        # Check existing columns
        with engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(user_preferences)"))
            columns = {row[1] for row in result.fetchall()}

            logger.info(f"Existing columns in user_preferences: {columns}")

            # SQL statements to add new columns
            migrations = []

            if 'default_provider' not in columns:
                migrations.append(text(
                    "ALTER TABLE user_preferences ADD COLUMN default_provider VARCHAR NOT NULL DEFAULT 'openai'"
                ))
                logger.info("Adding column: default_provider")

            if 'default_model' not in columns:
                migrations.append(text(
                    "ALTER TABLE user_preferences ADD COLUMN default_model VARCHAR NOT NULL DEFAULT 'gpt-4-turbo'"
                ))
                logger.info("Adding column: default_model")

            if 'auto_save_preferences' not in columns:
                migrations.append(text(
                    "ALTER TABLE user_preferences ADD COLUMN auto_save_preferences BOOLEAN NOT NULL DEFAULT 1"
                ))
                logger.info("Adding column: auto_save_preferences")

            if 'theme' not in columns:
                migrations.append(text(
                    "ALTER TABLE user_preferences ADD COLUMN theme VARCHAR NOT NULL DEFAULT 'light'"
                ))
                logger.info("Adding column: theme")

            # Execute migrations
            for migration in migrations:
                conn.execute(migration)
                conn.commit()

            if not migrations:
                logger.info("All columns already exist. No migration needed.")
            else:
                logger.info(f"Successfully added {len(migrations)} new columns to user_preferences table")

            # Verify migration
            result = conn.execute(text("PRAGMA table_info(user_preferences)"))
            new_columns = {row[1] for row in result.fetchall()}
            logger.info(f"Columns after migration: {new_columns}")

            # Check if row exists and has default values
            prefs = conn.execute(text("SELECT * FROM user_preferences LIMIT 1")).fetchone()

            if prefs:
                logger.info(f"Existing user preferences found: {prefs}")
                # Update NULL values with defaults
                updates = []
                if prefs[4] is None:  # default_provider (index 4)
                    updates.append("default_provider = 'openai'")
                if prefs[5] is None:  # default_model (index 5)
                    updates.append("default_model = 'gpt-4-turbo'")
                if prefs[6] is None:  # auto_save_preferences (index 6)
                    updates.append("auto_save_preferences = 1")
                if prefs[7] is None:  # theme (index 7)
                    updates.append("theme = 'light'")

                if updates:
                    update_sql = f"UPDATE user_preferences SET {', '.join(updates)} WHERE id = {prefs[0]}"
                    conn.execute(text(update_sql))
                    conn.commit()
                    logger.info("Updated existing row with default values")
            else:
                # Create default row if none exists
                conn.execute(text("""
                    INSERT INTO user_preferences (
                        language, name, country,
                        default_provider, default_model,
                        auto_save_preferences, theme
                    ) VALUES ('spanish', NULL, NULL, 'openai', 'gpt-4-turbo', 1, 'light')
                """))
                conn.commit()
                logger.info("Created default user preferences row")

        logger.info("✅ Migration completed successfully")
        return True

    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False


def verify_migration():
    """
    Verify that the migration was successful.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(user_preferences)"))
            columns = {row[1] for row in result.fetchall()}

            required_columns = {
                'id', 'language', 'name', 'country',
                'default_provider', 'default_model',
                'auto_save_preferences', 'theme',
                'created_at', 'updated_at'
            }

            missing = required_columns - columns

            if missing:
                logger.error(f"❌ Missing columns: {missing}")
                return False
            else:
                logger.info("✅ All required columns present")
                return True

    except Exception as e:
        logger.error(f"❌ Verification failed: {e}")
        return False


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("\n" + "="*60)
    print("Migration: Add new fields to user_preferences table")
    print("="*60 + "\n")

    print("Step 1: Adding new columns...")
    success = add_preferences_fields()

    if success:
        print("\nStep 2: Verifying migration...")
        if verify_migration():
            print("\n" + "="*60)
            print("✅ Migration completed and verified successfully!")
            print("="*60 + "\n")
            sys.exit(0)
        else:
            print("\n" + "="*60)
            print("❌ Migration verification failed!")
            print("="*60 + "\n")
            sys.exit(1)
    else:
        print("\n" + "="*60)
        print("❌ Migration failed!")
        print("="*60 + "\n")
        sys.exit(1)
