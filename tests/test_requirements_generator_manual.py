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
    print("Testing Rule-Based Requirements...")
    orchestrator = Orchestrator()
    task_agent = TaskAgent()
    engineer_agent = EngineerAgent()
    
    orchestrator.register_agent(task_agent)
    orchestrator.register_agent(engineer_agent)
    
    # Set a mock requirement
    req = "Build a FastAPI app using pandas and database sqlite."
    orchestrator.state.context["requirement"] = req
    
    # Run task agent (mock the LLM response)
    # Orchestrator's LLM is initialized, let's mock generate for this test
    # Actually, we can just patch it here
    from unittest.mock import patch
    with patch('src.core.llm.LLMEngine.generate') as mock_generate:
        mock_generate.return_value = '[{"path": "main.py", "description": "Entry point"}]'
        
        task_agent.run()
        
    print(f"File structure: {orchestrator.state.context.get('file_structure')}")
    print(f"Rule-based reqs: {orchestrator.state.context.get('rule_based_requirements')}")
    
    # Run engineer agent (mock again)
    with patch('src.core.llm.LLMEngine.generate') as mock_generate_eng:
        mock_generate_eng.return_value = 'print("Hello World")'
        
        engineer_agent.run()
        
    generated = orchestrator.state.context.get('generated_code', {})
    print("\nGenerated Code Dictionary:")
    for path, code in generated.items():
        print(f"--- {path} ---")
        print(code)
        
if __name__ == "__main__":
    main()
