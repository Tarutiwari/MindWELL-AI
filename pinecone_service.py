# pinecone_service.py
from pinecone import Pinecone, ServerlessSpec
from config import PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME
from sentence_transformers import SentenceTransformer

pc=Pinecone(api_key=PINECONE_API_KEY)
#index_name = "stress-analyse"
index= pc.Index("stress-analyse")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def embed_and_store(chat_id: str, message: str, metadata: dict):
    vector = embedder.encode(message).tolist()
    index.upsert([(chat_id, vector, metadata)])


print("✅ Connected to Pinecone index:", index)