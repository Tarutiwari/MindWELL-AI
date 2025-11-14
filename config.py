# config.py
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

# --- Gemini API ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- PostgreSQL ---
DATABASE_URL = os.getenv("DATABASE_URL")

# --- Redis ---
REDIS_URL = os.getenv("REDIS_URL")
REDIS_EXPIRY = int(os.getenv("REDIS_EXPIRY", 60 * 60 * 48))  # Default: 2 days

# --- Pinecone ---
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")  # e.g., "gcp-starter"
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")     # e.g., "chat-embeddings"
