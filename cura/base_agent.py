from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    def generate(self, task: str) -> str:
        """Generate a solution for the given task."""
        pass
