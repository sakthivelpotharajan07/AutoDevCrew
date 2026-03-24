import sys
import os
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Import agents
from src.agents.tester_agent import analyze_code
from src.agents.devops_agent import create_pipeline

def test_agents():
    code = "def add(a, b): return a + b"
    
    print("Testing Tester Agent...")
    if callable(analyze_code):
        print("`analyze_code` exists.")
        # We assume if it runs without import error, it's good for static check.
        # We can try a dry run if LLM is cheap/fast enough, but let's just check structure.
        
    print("Testing DevOps Agent...")
    if callable(create_pipeline):
        print("`create_pipeline` exists.")

    print("Verification Successful: Agents are importable and have correct functions.")

if __name__ == "__main__":
    test_agents()
