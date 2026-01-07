import pytest
from unittest.mock import MagicMock, patch
from src.agents.engineer_agent import EngineerAgent
from src.core.orchestrator import Orchestrator

@pytest.fixture
def orchestrator():
    # Patch the dependencies of Orchestrator so they don't initialize real heavy objects
    with patch('src.core.orchestrator.LLMEngine') as MockLLM, \
         patch('src.core.orchestrator.MemoryManager') as MockMemory:
        orch = Orchestrator()
        # We can now set custom mocks on the instance
        orch.llm = MagicMock()
        orch.memory = MagicMock()
        orch.state.context = {"requirement": "Test requirement"}
        orch.state.memory_context = []
        return orch

def test_engineer_agent_run(orchestrator):
    agent = EngineerAgent()
    agent.set_orchestrator(orchestrator)
    
    # Setup mock return
    orchestrator.llm.generate.return_value = "def test(): pass"
    
    agent.run()
    
    orchestrator.llm.generate.assert_called_once()
    orchestrator.memory.add_memory.assert_called_once()
