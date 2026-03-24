import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.core.orchestrator import Orchestrator
from src.agents.task_agent import TaskAgent
from src.agents.engineer_agent import EngineerAgent

def main():
    print("Testing Database requirements logic...")
    orchestrator = Orchestrator()
    task_agent = TaskAgent()
    engineer_agent = EngineerAgent()
    
    orchestrator.register_agent(task_agent)
    orchestrator.register_agent(engineer_agent)
    
    # Set a mock requirement
    req = "Build a login page"
    orchestrator.state.context["requirement"] = req
    
    # Run task agent (mock the LLM response)
    from unittest.mock import patch
    with patch('src.core.llm.LLMEngine.generate') as mock_generate:
        mock_generate.return_value = '[\n{"path": "main.py", "description": "Entry point"}\n]'
        task_agent.run()
        
    print(f"File structure: {orchestrator.state.context.get('file_structure')}")
    print(f"Rule-based reqs: {orchestrator.state.context.get('rule_based_requirements')}")
    
    # Check EngineerAgent outputs
    print("\nEngineer Prompt For main.py:")
    print(engineer_agent._build_prompt(req, "main.py", "Main Application File"))
    
    print("\nEngineer Prompt For database.py:")
    print(engineer_agent._build_prompt(req, "database.py", "Database file"))
    
    print("\nEngineer Prompt For models.py:")
    print(engineer_agent._build_prompt(req, "models.py", "Models file"))

if __name__ == "__main__":
    main()
