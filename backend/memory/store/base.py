import time
from dataclasses import dataclass, field

@dataclass
class MemoryRecord:
	content: str
	session_id: str
	timestamp: int = field(default_factory=lambda: int(time.time()))
	importance: float = 0.7
	meta_data: dict = field(default_factory=lambda: {})