import sys
import os
# sys.path.append(os.getcwd()) # Explicitly add CWD
print(f"Path: {sys.path}")
try:
    from src.agents.engineer_agent import EngineerAgent
    from src.core.orchestrator import Orchestrator
    print("Imports successful")
except Exception as e:
    print(f"Import Error: {e}")
