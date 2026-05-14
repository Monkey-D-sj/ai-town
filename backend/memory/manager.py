from backend.memory.strategy.base import MemoryRecord
from backend.storage.cache import CacheStore
from backend.storage.persist import PersistStore

class MemoryManager:
    def __init__(
      self,
      persist_store: PersistStore,
      cache_store: CacheStore
    ):
        self._persist_store = persist_store
        self._cache_store = cache_store

    def connect(self):
        self._persist_store.connect()
        self._cache_store.connect()
        
    def disconnect(self):
        self._persist_store.disconnect()
        self._cache_store.disconnect()
        
    def add_memory(self, data: MemoryRecord):
        self._cache_store.set(data.session_id, data)
        if data.importance > 0.7:
            self._persist_store.save(data)
        
    def load(self, session_id: str):
        data = self._persist_store.load(session_id) + self._cache_store.get(session_id)
        return data
