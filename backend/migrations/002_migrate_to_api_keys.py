"""
Migration 002: Migrate from settings to api_keys table

This script migrates existing API keys from the legacy 'settings' table 
to the new 'api_keys' table structure with enhanced features.

The 'settings' table will be preserved until v2.0 for backwards compatibility.
"""

import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.db.database import DATABASE_URL
from app.db.models import Base, ApiKey, Settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_tables_exist(db_session):
    """Check which tables exist in the database."""
    inspector = db_session.bind.dialect.get_inspector(db_session.bind)
    existing_tables = inspector.get_table_names()
    
    has_settings = 'settings' in existing_tables
    has_api_keys = 'api_keys' in existing_tables
    
    logger.info(f"Existing tables: {existing_tables}")
    logger.info(f"Has 'settings' table: {has_settings}")
    logger.info(f"Has 'api_keys' table: {has_api_keys}")
    
    return has_settings, has_api_keys


def create_api_keys_table(engine):
    """Create the new api_keys table."""
    try:
        logger.info("Creating api_keys table...")
        Base.metadata.create_all(bind=engine, tables=[ApiKey.__table__])
        logger.info("✅ api_keys table created successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create api_keys table: {e}")
        return False


def migrate_settings_to_api_keys(db_session):
    """Migrate data from settings to api_keys table."""
    try:
        logger.info("Starting migration from settings to api_keys...")
        
        # Query all existing settings
        settings_records = db_session.query(Settings).all()
        
        if not settings_records:
            logger.info("No settings records found, nothing to migrate")
            return True
        
        logger.info(f"Found {len(settings_records)} settings record(s) to migrate")
        
        migrated_count = 0
        for setting in settings_records:
            # Check if this provider/user combination already exists in api_keys
            existing_key = db_session.query(ApiKey).filter(
                ApiKey.provider == setting.provider
            ).first()
            
            if existing_key:
                logger.info(f"Skipping migration for provider '{setting.provider}' - already exists in api_keys")
                continue
            
            # Create new ApiKey record
            new_key = ApiKey(
                user_id=None,
                provider=setting.provider,
                api_key_encrypted=setting.api_key_encrypted,
                model_preference=setting.model_preference,
                is_active=1,
                usage_count=0,
                last_used_at=None
            )
            
            db_session.add(new_key)
            migrated_count += 1
            logger.info(f"Migrated provider '{setting.provider}' to api_keys table")
        
        # Commit the transaction
        db_session.commit()
        logger.info(f"✅ Successfully migrated {migrated_count} API key(s)")
        return True
        
    except Exception as e:
        db_session.rollback()
        logger.error(f"❌ Migration failed: {e}")
        return False


def verify_migration(db_session):
    """Verify that migration was successful."""
    try:
        settings_count = db_session.query(Settings).count()
        api_keys_count = db_session.query(ApiKey).count()
        
        logger.info(f"Settings records: {settings_count}")
        logger.info(f"ApiKeys records: {api_keys_count}")
        
        if api_keys_count > 0:
            logger.info("✅ Migration verification: SUCCESS")
            return True
        else:
            logger.warning("⚠️  Migration verification: No API keys found in new table")
            return False
            
    except Exception as e:
        logger.error(f"❌ Verification failed: {e}")
        return False


def upgrade():
    """Run the migration upgrade."""
    try:
        logger.info("=" * 60)
        logger.info("Starting Migration 002: settings → api_keys")
        logger.info("=" * 60)
        
        # Create database engine and session
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db_session = SessionLocal()
        
        # Check which tables exist
        has_settings, has_api_keys = check_tables_exist(db_session)
        
        # Migration logic
        if not has_settings and not has_api_keys:
            logger.info("No settings or api_keys table exists. Creating api_keys table...")
            success = create_api_keys_table(engine)
            
        elif has_settings and not has_api_keys:
            logger.info("Settings table exists but api_keys does not. Running migration...")
            success = create_api_keys_table(engine)
            if success:
                success = migrate_settings_to_api_keys(db_session)
                if success:
                    verify_migration(db_session)
                    
        elif has_settings and has_api_keys:
            logger.info("Both tables exist. Checking if migration is needed...")
            settings_count = db_session.query(Settings).count()
            api_keys_count = db_session.query(ApiKey).count()
            
            if settings_count > 0 and api_keys_count == 0:
                logger.info("Found settings but no api_keys. Running migration...")
                success = migrate_settings_to_api_keys(db_session)
                if success:
                    verify_migration(db_session)
            else:
                logger.info("Migration appears to have already been completed")
                success = True
                
        elif not has_settings and has_api_keys:
            logger.info("Only api_keys table exists. Migration already completed")
            success = True
        
        # Cleanup
        db_session.close()
        engine.dispose()
        
        logger.info("=" * 60)
        if success:
            logger.info("✅ Migration completed successfully")
        else:
            logger.error("❌ Migration failed")
        logger.info("=" * 60)
        
        return success
        
    except Exception as e:
        logger.error(f"❌ Fatal error during migration: {e}")
        return False


def downgrade():
    """Rollback the migration (not recommended)."""
    try:
        logger.warning("=" * 60)
        logger.warning("⚠️  DOWNGRADE NOT SUPPORTED")
        logger.warning("The 'settings' table is preserved until v2.0 for backwards compatibility")
        logger.warning("No action taken")
        logger.warning("=" * 60)
        return True
        
    except Exception as e:
        logger.error(f"❌ Error during downgrade: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migration 002: settings → api_keys")
    parser.add_argument('--downgrade', action='store_true', help='Rollback migration (not recommended)')
    
    args = parser.parse_args()
    
    if args.downgrade:
        success = downgrade()
    else:
        success = upgrade()
    
    sys.exit(0 if success else 1)
