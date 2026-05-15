import time
from dataclasses import field, dataclass

from backend.common.db.redis_db import RedisDB
from backend.memory.store.base import MemoryRecord


@dataclass
class ShortMemoryRecord(MemoryRecord):
    pass

class ShortMemoryStore:
    def __init__(self, redis_store: RedisDB, max_retain: int = 5):
        self._redis_store = redis_store
        self._max_retain = max_retain

    def add(self, record: ShortMemoryRecord):
        records = self._redis_store.get(record.session_id) or []
        records.append({
            "content": record.content,
            "session_id": record.session_id,
            "timestamp": record.timestamp,
            "importance": record.importance,
            "meta_data": record.meta_data,
        })
        if len(records) > self._max_retain:
            records.pop(0)
        self._redis_store.set(record.session_id, records)
        print(f"Add {record.content} to {record.session_id}")

    def get(self, session_id: str) -> list[ShortMemoryRecord]:
        records = self._redis_store.get(session_id)
        print("get memory")
        if not records:
            return []
        return [ShortMemoryRecord(**r) for r in records]

    def delete(self, session_id: str):
        self._redis_store.delete(session_id)
        print(f"Delete {session_id}")
