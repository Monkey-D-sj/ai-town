import os

from dotenv import load_dotenv
from openai import OpenAI

from backend.memory.store.base import MemoryRecord
from backend.memory.store.long_memory import LongMemoryStore, LongMemoryRecord
from backend.memory.store.short_memory import ShortMemoryStore, ShortMemoryRecord
from backend.common.db.redis_db import redis_client
from backend.common.db.milvus_db import milvus_client

load_dotenv()

class MemoryManager:
	def __init__(
		self,
		long_memory_store: LongMemoryStore,
		short_memory_store: ShortMemoryStore,
	):
		self.long_memory_store = long_memory_store
		self.short_memory_store = short_memory_store

	def add_memory(self, memory: MemoryRecord):
		self.short_memory_store.add(ShortMemoryRecord(**memory.__dict__))
		if memory.importance >= 0.7:
			self.long_memory_store.add(memory)

	def retrieve(self, query: str, top_k: int = 5) -> list[LongMemoryRecord]:
		return self.long_memory_store.query(query, top_k)

	def get_recent(self, session_id: str) -> list[ShortMemoryRecord]:
		return self.short_memory_store.get(session_id)


def generate_embeddings(text: str) -> list[float]:
	client = OpenAI(
		api_key=os.getenv("QWEN_API_KEY"),  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
		base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
	)
	rsp = client.embeddings.create(
        model="text-embedding-v4",
		input=text,
        dimensions=1024,
		encoding_format="float"
	)
	return rsp.data[0].embedding


def get_memory_manager() -> MemoryManager:
	return MemoryManager(
		long_memory_store=LongMemoryStore(milvus_client, generate_embeddings),
		short_memory_store=ShortMemoryStore(redis_client),
	)
