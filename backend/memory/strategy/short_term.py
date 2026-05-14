from backend.memory.strategy.base import BaseStrategy, MemoryRecord
from backend.storage.cache import CacheStore


class ShortTermStrategy(BaseStrategy):
    def __init__(self, store: CacheStore):
        self._store = store
        
    def save(self, data: MemoryRecord):
        self._store.set(data.session_id, data)
        
    def load(self, session_id: str) -> list[MemoryRecord]:
        return self._store.get(session_id, [])
