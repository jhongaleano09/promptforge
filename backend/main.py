from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import endpoints, workflow
from app.db.database import engine, Base
from app.core.workflow_manager import workflow_manager

# Create tables on startup
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    yield
    # Shutdown actions
    await workflow_manager.close()

app = FastAPI(title="PromptForge API", lifespan=lifespan)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
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
