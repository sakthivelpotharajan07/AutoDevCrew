from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

class AgentState(Enum):
    IDLE = auto()
    WORKING = auto()
    WAITING = auto()
    ERROR = auto()
    COMPLETED = auto()

class PipelineStatus(Enum):
    IDLE = auto()
    RUNNING = auto()
    SUCCESS = auto()
    FAILED = auto()

@dataclass
class Task:
    id: str
    description: str
    status: str = "PENDING"
    result: Optional[str] = None
    artifacts: List[str] = field(default_factory=list)

@dataclass
class SharedState:
    status: PipelineStatus = PipelineStatus.IDLE
    current_step: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    memory_context: List[str] = field(default_factory=list)

    def update_context(self, key: str, value: Any):
        self.context[key] = value
