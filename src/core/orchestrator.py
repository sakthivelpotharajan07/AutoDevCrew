from src.core.event_bus import EventBus
from src.core.state import SharedState, PipelineStatus
from src.core.memory_manager import MemoryManager
from src.core.llm import LLMEngine
from src.core.utils import setup_logging
import time

logger = setup_logging("Orchestrator")

class Orchestrator:
    def __init__(self):
        self.event_bus = EventBus()
        self.state = SharedState()
        self.memory = MemoryManager()
        self.llm = LLMEngine()
        self.agents = []

    def register_agent(self, agent):
        self.agents.append(agent)
        agent.set_orchestrator(self)

    def run_pipeline(self, requirement: str):
        logger.info(f"Starting pipeline with requirement: {requirement}")
        self.state.status = PipelineStatus.RUNNING
        self.state.update_context("requirement", requirement)
        
        # 1. Retrieve context
        memories = self.memory.search_memory(requirement)
        self.state.memory_context = memories.get('documents', [])
        
        try:
            for agent in self.agents:
                logger.info(f"Running agent: {agent.name}")
                self.state.current_step = agent.name
                agent.run()
                
            self.state.status = PipelineStatus.SUCCESS
            logger.info("Pipeline completed successfully.")
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            self.state.status = PipelineStatus.FAILED
            self.state.errors.append(str(e))

        return self.state
