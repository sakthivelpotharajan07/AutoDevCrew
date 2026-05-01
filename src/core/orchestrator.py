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
                
                if validation_status == "PASS" or validation_status not in ["PASS", "FAIL"]:
                    if validation_status == "PASS":
                        logger.info("Validation PASSED. Pipeline successful.")
                    else:
                        logger.info("No validation status found. Assuming linear execution complete.")
                    
                    # Instead of setting status to SUCCESS early, update current step
                    self.state.current_step = "Saving Generated Codes..."
                    
                    # --- Save generated files to disk ---
                    try:
                        import os
                        project_dir = "generated_project"
                        os.makedirs(project_dir, exist_ok=True)
                        gen_code = self.state.context.get("generated_code", {})
                        if isinstance(gen_code, dict):
                            for filepath, content in gen_code.items():
                                full_path = os.path.join(project_dir, filepath)
                                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                                with open(full_path, "w", encoding="utf-8") as f:
                                    f.write(content)
                        elif isinstance(gen_code, str):
                            with open(os.path.join(project_dir, "main.py"), "w", encoding="utf-8") as f:
                                f.write(gen_code)
                        logger.info(f"Saved generated code to {project_dir}/")
                    except Exception as e:
                        logger.error(f"Failed to save generated code: {e}")
                    # ------------------------------------
                    
                    # --- Docker Generation Step ---
                    try:
                        self.state.current_step = "Generating Docker and Req files..."
                        req_msg = generate_requirements(project_path="generated_project", framework="fastapi")
                        docker_msg = generate_dockerfile(project_path="generated_project", framework="fastapi")
                        logger.info(req_msg)
                        logger.info(docker_msg)
                    except Exception as e:
                        logger.error(f"Docker generation failed: {e}")
                    # ------------------------------
                    
                    # --- Live Demo Link ---
                    try:
                        self.state.current_step = "Deploying Live Application..."
                        logger.info("Starting auto-runner to install dependencies and deploy...")
                        live_url = run_and_deploy()
                        self.state.update_context("live_url", live_url)
                        logger.info(f"Live link created: {live_url}")
                    except Exception as e:
                        logger.error(f"Failed to run and deploy: {e}")
                    # ----------------------
                    
                    # Mark pipeline as finally SUCCESS after everything including deployment is done
                    self.state.status = PipelineStatus.SUCCESS
                    break
                elif validation_status == "FAIL":
                    logger.warning("Validation FAILED. Retrying...")
                    feedback = self.state.context.get("feedback", "No feedback provided.")
                    logger.info(f"Feedback: {feedback}")
                    iteration_count += 1
                    
            if iteration_count >= MAX_ITERATIONS:
                logger.error("Max iterations reached. Pipeline FAILED.")
                self.state.status = PipelineStatus.FAILED
                
                # Retrieve the last feedback to give a descriptive error
                final_feedback = self.state.context.get("feedback", "No specific feedback.")
                self.state.errors.append(f"Validation FAILED after 3 attempts. Final feedback: {final_feedback}")

            if self.state.status == PipelineStatus.SUCCESS:
                logger.info("Pipeline completed successfully.")

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            self.state.status = PipelineStatus.FAILED
            self.state.errors.append(str(e))

        return self.state
