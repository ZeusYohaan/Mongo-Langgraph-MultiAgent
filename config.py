import os
from langchain_groq import ChatGroq
from langgraph.checkpoint.redis import RedisSaver
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

llm = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    temperature=0
)

db = MongoClient(os.environ.get('MONGO_URL')).client[os.environ.get('MONGO_DB')]

redis_checkpoint = RedisSaver.from_conn_string(os.environ.get("REDIS_URL"))
