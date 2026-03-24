
import sys
import os
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import unittest
from unittest.mock import MagicMock
from src.agents.task_planner_agent import TaskPlannerAgent
from src.core.llm import LLMEngine

class TestTaskPlannerAgent(unittest.TestCase):
    def setUp(self):
        self.agent = TaskPlannerAgent()
        self.mock_orchestrator = MagicMock()
        self.mock_state = MagicMock()
        self.mock_state.context = {}
        
        # Setup Orchestrator mock structure
        self.mock_orchestrator.state = self.mock_state
        self.mock_orchestrator.llm = MagicMock(spec=LLMEngine)
        
        self.agent.set_orchestrator(self.mock_orchestrator)

    def test_run_with_requirement(self):
        # Setup context
        self.mock_state.context = {"requirement": "Build a login system"}
        
        # Mock LLM response
        expected_plan = '["Design API", "Implement Auth"]'
        self.mock_orchestrator.llm.generate.return_value = expected_plan

        # Run agent
        self.agent.run()

        # Check if context was updated
        self.mock_state.update_context.assert_called_with("task_plan", ["Design API", "Implement Auth"])
        print("\nTest passed: Agent correctly parsed standard JSON response.")

    def test_run_with_markdown_json(self):
        # Setup context
        self.mock_state.context = {"requirement": "Fix bugs"}
        
        # Mock LLM response with markdown
        markdown_response = "```json\n[\"Fix Bug A\", \"Fix Bug B\"]\n```"
        self.mock_orchestrator.llm.generate.return_value = markdown_response

        # Run agent
        self.agent.run()

        # Check if context was updated
        self.mock_state.update_context.assert_called_with("task_plan", ["Fix Bug A", "Fix Bug B"])
        print("Test passed: Agent correctly parsed Markdown JSON response.")

if __name__ == '__main__':
    unittest.main()
