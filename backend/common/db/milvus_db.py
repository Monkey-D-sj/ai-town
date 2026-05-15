import os

from pymilvus import MilvusClient

MILVUS_URI = os.getenv("MILVUS_URI", "http://localhost:19530")

milvus_client = MilvusClient(uri=MILVUS_URI, db_name="default")

