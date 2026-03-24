import sys
import logging
from src.core.orchestrator import Orchestrator

# Setup logging to see detailed output
logging.basicConfig(level=logging.INFO)

def debug_pipeline():
    print("Initializing Orchestrator...")
    try:
        orchestrator = Orchestrator()
    except Exception as e:
        print(f"Failed to initialize Orchestrator: {e}")
        return

    objective = "build login page in python function"
    print(f"Running pipeline with objective: {objective}")
    
    try:
        state = orchestrator.run_pipeline(objective)
        
        print("\n=== Pipeline Result ===")
        print(f"Status: {state.status}")
        print(f"Errors: {state.errors}")
        
        print("\n=== Conversation History ===")
        for line in orchestrator.conversation_history:
            print(line)
            
    except Exception as e:
        print(f"Exception during pipeline execution: {e}")
        # Print history even if it crashed
        if hasattr(orchestrator, 'conversation_history'):
             print("\n=== Partial Conversation History ===")
             for line in orchestrator.conversation_history:
                print(line)

if __name__ == "__main__":
    debug_pipeline()
