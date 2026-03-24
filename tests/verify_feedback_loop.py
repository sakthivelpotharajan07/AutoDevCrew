
import sys
import os
from pathlib import Path
import unittest
from unittest.mock import MagicMock, call

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.core.orchestrator import Orchestrator
from src.agents.engineer_agent import EngineerAgent
from src.agents.tester_agent import TesterAgent

class TestFeedbackLoop(unittest.TestCase):
    def setUp(self):
        self.orchestrator = Orchestrator()
        
        # Mock LLM to control responses
        self.orchestrator.llm = MagicMock()
        
        # Clear default agents (if any) and register ours
        self.orchestrator.agents = []
        self.engineer = EngineerAgent()
        self.tester = TesterAgent()
        
        self.orchestrator.register_agent(self.engineer)
        self.orchestrator.register_agent(self.tester)

    def test_retry_logic(self):
        print("\n--- Testing Feedback Loop (Fail -> Pass) ---")
        
        # Define the sequence of LLM responses
        # 1. Engineer: Generates "Bad Code"
        # 2. Tester: Rejects "Bad Code" (FAIL)
        # 3. Engineer: Generates "Good Code" (after feedback)
        # 4. Tester: Accepts "Good Code" (PASS)
        
        response_sequence = [
            "def bad_code(): pass",  # Engineer 1
            '{"status": "FAIL", "feedback": "Function is empty"}', # Tester 1
            "def good_code(): return True", # Engineer 2
            '{"status": "PASS", "feedback": "Looks good", "tests": "def test_good(): assert good_code()"}' # Tester 2
        ]
        
        self.orchestrator.llm.generate.side_effect = response_sequence
        
        # Run pipeline
        state = self.orchestrator.run_pipeline("Build a function")
        
        # Assertions
        # 1. State should be SUCCESS
        self.assertEqual(state.status.name, "SUCCESS")
        
        # 2. LLM should have been called 4 times
        self.assertEqual(self.orchestrator.llm.generate.call_count, 4)
        
        # 3. Context should have the final code and tests
        self.assertEqual(state.context.get("generated_code"), "def good_code(): return True")
        self.assertIn("def test_good()", state.context.get("tests", ""))
        
        print("Feedback loop verified successfully!")

    def test_max_retries_exceeded(self):
        print("\n--- Testing Max Retries Exceeded ---")
        
        # Always fail
        # Sequence: Eng -> Test(Fail) -> Eng -> Test(Fail) -> Eng -> Test(Fail)
        # Total 3 iterations = 6 calls
        
        response_sequence = [
            "code", '{"status": "FAIL", "feedback": "error"}'
        ] * 4 # More than enough
        
        self.orchestrator.llm.generate.side_effect = response_sequence
        
        state = self.orchestrator.run_pipeline("Impossible task")
        
        # Should be FAILED
        self.assertEqual(state.status.name, "FAILED")
        
        # Should have run 3 iterations (Engineer+Tester each time = 2 calls/iter * 3 = 6 calls)
        self.assertEqual(self.orchestrator.llm.generate.call_count, 6)
        
        print("Max retries enforcement verified!")

if __name__ == '__main__':
    unittest.main()
