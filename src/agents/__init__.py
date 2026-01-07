from abc import ABC, abstractmethod

class Agent(ABC):
    def __init__(self, name):
        self.name = name
        self.orchestrator = None

    def set_orchestrator(self, orchestrator):
        self.orchestrator = orchestrator

    @abstractmethod
    def run(self):
        pass
