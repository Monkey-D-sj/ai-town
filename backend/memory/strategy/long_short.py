from backend.memory.strategy.base import BaseStrategy, MemoryRecord
from backend.storage.persist import PersistStore


class LongShortTerm(BaseStrategy):
    def __init__(self, store: PersistStore):
        self._store = store
      
    def save(self, data: MemoryRecord):
        self._store.save(data)
        
    def load(self, session_id: str) -> list[MemoryRecord]:
        return self._store.load(session_id)
        
