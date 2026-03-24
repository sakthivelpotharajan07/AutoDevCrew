from src.core.event_bus import EventBus
from src.core.state import SharedState, PipelineStatus
from src.core.memory_manager import MemoryManager
from src.core.llm import LLMEngine
from src.core.utils import setup_logging
import time
from src.agents.docker_agent import generate_dockerfile, generate_requirements
from src.deploy.auto_run import run_and_deploy

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
        
        MAX_ITERATIONS = 3
        iteration_count = 0
        
        try:
            # Main workflow loop
            while iteration_count < MAX_ITERATIONS:
                logger.info(f"--- Iteration {iteration_count + 1}/{MAX_ITERATIONS} ---")
                
                # Execute all agents in sequence
                for agent in self.agents:
                    logger.info(f"Running agent: {agent.name}")
                    self.state.current_step = agent.name
                    agent.run()
                    
                    # Check for early failure if an agent explicitly marks context as failed
                    # (Optional enhancement, but sticking to basic loop for now)

                # Post-pipeline check (after TesterAgent runs)
                validation_status = self.state.context.get("validation_status", "UNKNOWN")
                
                if validation_status == "PASS":
                    logger.info("Validation PASSED. Pipeline successful.")
                    self.state.status = PipelineStatus.SUCCESS
                    break
                elif validation_status == "FAIL":
                    logger.warning("Validation FAILED. Retrying...")
                    feedback = self.state.context.get("feedback", "No feedback provided.")
                    logger.info(f"Feedback: {feedback}")
                    iteration_count += 1
                else:
                    # If no valid status, assume linear pass or first run without validation
                    logger.info("No validation status found. Assuming linear execution complete.")
                    self.state.status = PipelineStatus.SUCCESS
                    
                    # --- Docker Generation Step ---
                    # Assuming generated project is in specific path, or just use a default "generated_project"
                    # The prompt suggests: generate_requirements(project_path="generated_project", framework="fastapi")
                    # We might need to detect framework dynamically, but for now we follow the prompt.
                    try:
                        req_msg = generate_requirements(project_path="generated_project", framework="fastapi")
                        docker_msg = generate_dockerfile(project_path="generated_project", framework="fastapi")
                        logger.info(req_msg)
                        logger.info(docker_msg)
                    except Exception as e:
                        logger.error(f"Docker generation failed: {e}")
                    # ------------------------------
                    
                    # --- Live Demo Link ---
                    try:
                        logger.info("Starting auto-runner to install dependencies and deploy...")
                        live_url = run_and_deploy()
                        self.state.update_context("live_url", live_url)
                        logger.info(f"Live link created: {live_url}")
                    except Exception as e:
                        logger.error(f"Failed to run and deploy: {e}")
                    # ----------------------
                    
                    break
            
            if iteration_count >= MAX_ITERATIONS:
                logger.error("Max iterations reached. Pipeline FAILED.")
                self.state.status = PipelineStatus.FAILED

            if self.state.status == PipelineStatus.SUCCESS:
                logger.info("Pipeline completed successfully.")

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            self.state.status = PipelineStatus.FAILED
            self.state.errors.append(str(e))

        return self.state
