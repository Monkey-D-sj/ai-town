from dataclasses import dataclass, field
from typing import Callable

from pymilvus import MilvusClient, DataType, FieldSchema, CollectionSchema, Collection
from pymilvus.milvus_client import IndexParams

from backend.memory.store.base import MemoryRecord


@dataclass
class LongMemoryRecord(MemoryRecord):
    vector: list[float] = field(default_factory=list)


class LongMemoryStore:
    def __init__(
        self,
        milvus_client: MilvusClient,
        embedding_func: Callable[[str], list[float]],
        collection_name: str = "long_term",
    ):
        self._milvus_client = milvus_client
        self._collection_name = collection_name
        self._embedding_func = embedding_func
        self._ensure_collection()
        
    def _ensure_collection(self):
        if self._collection_name not in self._milvus_client.list_collections():
            schema: CollectionSchema = CollectionSchema(
                fields=[
                    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                    FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=1024),
                    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=1024),
                    FieldSchema(name="session_id", dtype=DataType.VARCHAR, max_length=1024),
                    FieldSchema(name="timestamp", dtype=DataType.FLOAT),
                    FieldSchema(name="importance", dtype=DataType.FLOAT),
                    FieldSchema(name="meta_data", dtype=DataType.JSON),
                ]
            )
            
            self._milvus_client.create_collection(
                collection_name=self._collection_name,
                schema=schema,
            )
            print(f"Collection {self._collection_name} created")
            
            index_params: IndexParams = IndexParams(
	            metric_type="IP",
                index_type="HNSW",
                params={"M": 16, "efConstruction": 200}
            )
            self._milvus_client.create_index(collection_name=self._collection_name, field_name="vector", index_params=index_params)
            print(f"Index vector created for {self._collection_name}")
            
            



    def add(self, data: MemoryRecord) -> None:
        try:
            self._milvus_client.insert(
                collection_name=self._collection_name,
                data=[{
                    "content": data.content,
                    "vector": self._embedding_func(data.content),
                    "session_id": data.session_id,
                    "timestamp": data.timestamp,
                    "importance": data.importance,
                    "meta_data": data.meta_data,
                }],
            )
            print(f"Added long memory {data} to {self._collection_name}")
        except Exception as e:
            print(f"Error to add {data} to {self._collection_name}: {e}")

    def query(self, query: str, top_k: int = 5) -> list[LongMemoryRecord]:
        try:
            results = self._milvus_client.search(
                collection_name=self._collection_name,
                data=[self._embedding_func(query)],
                output_fields=["content", "session_id", "timestamp", "importance", "meta_data"],
                limit=top_k,
            )
            records = []
            for hit in results[0]:
                entity = hit["entity"]
                records.append(LongMemoryRecord(
                    content=entity["content"],
                    session_id=entity["session_id"],
                    timestamp=entity["timestamp"],
                    importance=entity["importance"],
                    meta_data=entity["meta_data"],
                ))
            return records
        except Exception as e:
            print(f"Error to query {query} from {self._collection_name}: {e}")
            return []
