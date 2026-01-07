import pytest
from unittest.mock import MagicMock, patch
from src.agents.tester_agent import TesterAgent
from src.core.orchestrator import Orchestrator

@pytest.fixture
def orchestrator():
    with patch('src.core.orchestrator.LLMEngine') as MockLLM, \
         patch('src.core.orchestrator.MemoryManager') as MockMemory:
        orch = Orchestrator()
        orch.llm = MagicMock()
        orch.memory = MagicMock()
        orch.state.context = {"generated_code": "def test(): pass"}
        return orch

def test_tester_agent_run(orchestrator):
    agent = TesterAgent()
    agent.set_orchestrator(orchestrator)
    
    orchestrator.llm.generate.return_value = "def test_unit(): assert True"
    
    agent.run()
    
    orchestrator.llm.generate.assert_called_once()
