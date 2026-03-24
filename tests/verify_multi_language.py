
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

class TestMultiLanguage(unittest.TestCase):
    def setUp(self):
        self.orchestrator = Orchestrator()
        self.orchestrator.llm = MagicMock()
        self.orchestrator.agents = []
        self.engineer = EngineerAgent()
        self.tester = TesterAgent()
        
        self.orchestrator.register_agent(self.engineer)
        self.orchestrator.register_agent(self.tester)

    def test_java_generation(self):
        print("\n--- Testing Java Generation ---")
        
        # Scenario: User asks for a Java class.
        # 1. Engineer should produce Java code.
        # 2. Tester should produce JUnit tests.
        
        # Mock responses
        # Engineer:
        eng_response = 'public class HelloWorld { public static void main(String[] args) { System.out.println("Hello"); } }'
        # Tester:
        test_response = '{"status": "PASS", "feedback": "Good Java code", "tests": "import org.junit.Test; public class TestHello { @Test public void test() {} }"}'
        
        self.orchestrator.llm.generate.side_effect = [eng_response, test_response]
        
        state = self.orchestrator.run_pipeline("Create a Hello World class in Java")
        
        # Check context
        self.assertEqual(state.context.get("generated_code"), eng_response)
        self.assertIn("junit", state.context.get("tests", "").lower())
        print("Java verification successful!")

    def test_react_generation(self):
        print("\n--- Testing React Generation ---")
        
        # Scenario: User asks for a React component.
        
        eng_response = 'export default function App() { return <div>Hello</div>; }'
        test_response = '{"status": "PASS", "feedback": "Valid React", "tests": "test(\'renders\', () => { render(<App />); });"}'
        
        self.orchestrator.llm.generate.side_effect = [eng_response, test_response]
        
        state = self.orchestrator.run_pipeline("Create a React component")
        
        self.assertEqual(state.context.get("generated_code"), eng_response)
        self.assertIn("render", state.context.get("tests", ""))
        print("React verification successful!")

    def test_js_generation(self):
        print("\n--- Testing JavaScript Generation ---")
        
        # Scenario: User asks for a JS function.
        
        eng_response = 'function sum(a, b) { return a + b; }'
        test_response = '{"status": "PASS", "feedback": "Valid JS", "tests": "const assert = require(\'assert\'); describe(\'sum\', function() { it(\'should return sum\', function() { assert.equal(sum(1, 2), 3); }); });"}'
        
        self.orchestrator.llm.generate.side_effect = [eng_response, test_response]
        
        state = self.orchestrator.run_pipeline("Write a JavaScript sum function")
        
        self.assertEqual(state.context.get("generated_code"), eng_response)
        self.assertIn("describe", state.context.get("tests", ""))
        print("JavaScript verification successful!")

if __name__ == '__main__':
    unittest.main()
