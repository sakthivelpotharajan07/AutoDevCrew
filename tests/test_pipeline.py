import pytest
from unittest.mock import MagicMock, patch
from src.core.orchestrator import Orchestrator
from src.core.state import PipelineStatus

def test_pipeline_run():
    # Patch dependencies to mock them out
    with patch('src.core.orchestrator.LLMEngine') as MockLLM, \
         patch('src.core.orchestrator.MemoryManager') as MockMemory:
        orch = Orchestrator()
        
        # Configure mocks
        orch.memory.search_memory.return_value = {'documents': []}
        orch.llm.generate.return_value = "Mocked Response"
        
        mock_agent = MagicMock()
        mock_agent.name = "MockAgent"
        orch.register_agent(mock_agent)
        
        state = orch.run_pipeline("Test requirement")
        
        assert state.status == PipelineStatus.SUCCESS
        mock_agent.run.assert_called_once()
