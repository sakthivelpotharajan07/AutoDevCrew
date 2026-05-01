import sys
import os
from pathlib import Path

# Add project root to sys.path to allow 'src' imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
from src.core.orchestrator import Orchestrator
from src.core.state import PipelineStatus
from src.agents.task_agent import TaskAgent
from src.agents.engineer_agent import EngineerAgent
from src.agents.tester_agent import TesterAgent
from src.agents.devops_agent import DevOpsAgent
from src.agents.summarizer_agent import SummarizerAgent
import uvicorn
import logging

logger = logging.getLogger("API_Server")

orchestrator = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize system resources on startup
    global orchestrator
    logger.info("Initializing Orchestrator...")
    orchestrator = Orchestrator()
    orchestrator.register_agent(TaskAgent())
    orchestrator.register_agent(EngineerAgent())
    orchestrator.register_agent(TesterAgent())
    orchestrator.register_agent(DevOpsAgent())
    orchestrator.register_agent(SummarizerAgent())
    
    # Optionally trigger model load in background or just wait for first request
    # orchestrator.llm.load_model()  
    logger.info("Orchestrator initialized with agents.")
    yield
    # Clean up resources if needed
    logger.info("Shutting down...")

app = FastAPI(title="AutoDevCrew API", description="API for Multi-Agent DevOps System", lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
def root():
    html_file = PROJECT_ROOT / "login_page.html"
    if html_file.exists():
        return html_file.read_text(encoding="utf-8")
    return "<h1>AutoDevCrew Backend is Running</h1><p>No login_page.html found.</p>"
class PipelineRequest(BaseModel):
    requirement: str

@app.post("/run_pipeline")
def run_pipeline(request: PipelineRequest, background_tasks: BackgroundTasks):
    if not orchestrator:
        raise HTTPException(status_code=503, detail="System not initialized")
        
    try:
        # Reset state for a new run
        orchestrator.state.status = PipelineStatus.IDLE
        orchestrator.state.current_step = "Initializing..."
        orchestrator.state.context = {}
        orchestrator.state.errors = []
        orchestrator.state.memory_context = []
        
        # Add the pipeline execution to background tasks
        background_tasks.add_task(orchestrator.run_pipeline, request.requirement)
        
        return {"status": "STARTED"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pipeline_status")
def pipeline_status():
    if not orchestrator:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    return {
        "status": orchestrator.state.status.name,
        "current_step": orchestrator.state.current_step,
        "context": orchestrator.state.context,
        "errors": orchestrator.state.errors
    }

@app.get("/memory/search")
def search_memory(q: str):
    if not orchestrator:
        raise HTTPException(status_code=503, detail="System not initialized")
    results = orchestrator.memory.search_memory(q)
    return results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
