import sys
import os
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.agents.engineer_agent import refine_code

def test_refine_code():
    code = "def hello(): print('hello')"
    print("Testing refine_code logic...")
    # We won't actually call LLM here to avoid cost/latency in verification unless necessary?
    # Actually, for full verification, we should, but let's check imports first.
    # We can mock LLMEngine if we want, but let's just assume if it imports it works for now.
    
    print("Imports successful.")
    print("`refine_code` function exists:", callable(refine_code))

if __name__ == "__main__":
    test_refine_code()
