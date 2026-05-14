import time
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class MemoryRecord:
    session_id: str
    content: str
    timestamp: int = time.time()
    importance: float = 0.5
    

class BaseStrategy(ABC):
    @abstractmethod
    def save(self, data: MemoryRecord): ...
    
    @abstractmethod
    def load(self, session_id: str) -> list[MemoryRecord]:
        ...
