from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import endpoints, workflow
from app.db.database import engine, Base
from app.core.workflow_manager import workflow_manager
import logging

logger = logging.getLogger(__name__)

# Create tables on startup
Base.metadata.create_all(bind=engine)

def run_migration_if_needed():
    """Run migration from settings to api_keys if needed."""
    try:
        import sys
        import os

        migration_path = os.path.join(os.path.dirname(__file__), "migrations", "002_migrate_to_api_keys.py")

        if not os.path.exists(migration_path):
            logger.warning(f"Migration script not found at {migration_path}")
            return

        sys.path.insert(0, os.path.dirname(migration_path))
        from migrations import migrate_to_api_keys

        logger.info("Checking if migration from settings to api_keys is needed...")
        success = migrate_to_api_keys.upgrade()

        if success:
            logger.info("✅ Migration check completed successfully")
        else:
            logger.warning("⚠️ Migration encountered issues but will continue")

    except Exception as e:
        logger.error(f"Migration error: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Starting PromptForge API...")
    run_migration_if_needed()
    logger.info("PromptForge API startup completed")
    yield
    # Shutdown actions
    logger.info("Shutting down PromptForge API...")
    await workflow_manager.close()
    logger.info("Shutdown complete")

app = FastAPI(title="PromptForge API", lifespan=lifespan)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/api")
app.include_router(workflow.router, prefix="/api/workflow")

@app.get("/")
def read_root():
    return {"message": "PromptForge Backend is running"}
