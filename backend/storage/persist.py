import sqlite3
from abc import abstractmethod
from typing import Any

from backend.storage.base import BaseStore


class PersistStore(BaseStore):
    @abstractmethod
    def save(self, data: Any): ...
    
    @abstractmethod
    def load(self, session_id: str) -> list[Any]:
        ...

class SQLitePersistStore(PersistStore):
    _client: sqlite3.Connection = None
    
    def __init__(self, db_path: str):
        self._db_path = db_path

    def connect(self):
        self._client = sqlite3.connect(self._db_path)
    
    def disconnect(self):
        self._client.close()
    
    def save(self, data: Any):
        cursor = self._client.cursor()
        cursor.execute("INSERT INTO data (data) VALUES (?)", (data,))
        self._client.commit()
        cursor.close()
    
    def load(self, session_id: str):
        cursor = self._client.cursor()
        cursor.execute("SELECT data FROM data WHERE session_id = ?", (session_id,))
        data = cursor.fetchall()
        cursor.close()
        return data
