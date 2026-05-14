from abc import abstractmethod
from typing import Any

from backend.storage.base import BaseStore


class CacheStore(BaseStore):
    @abstractmethod
    def get(self, key: str): ...
    
    @abstractmethod
    def set(self, key: str, value: Any): ...

class MemoryCacheStore(CacheStore):
    _dict: dict[str, list[Any]] = {}
        
    def connect(self): ...
    
    def disconnect(self): ...

    def get(self, key: str):
        return self._dict.get(key, None)
    
    def set(self, key: str, value: Any):
        self._dict[key] = value
