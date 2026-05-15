import json
from typing import Any


# 简单的 Redis 封装（基于内存）
class RedisDB:
	"""简单直接的 Redis 存储"""
	
	_client: dict = {}
	
	def set(self, key: str, value: Any):
		"""存储字典数据"""
		data = json.dumps(value, ensure_ascii=False)
		self._client[key] = data
	
	def get(self, key: str) -> Any | None:
		"""获取字典数据"""
		result = self._client.get(key, None)
		return json.loads(result) if result else None
	
	def delete(self, key: str):
		"""删除"""
		self._client.pop(key, None)

redis_client = RedisDB()
