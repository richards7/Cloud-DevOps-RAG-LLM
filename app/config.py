import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

    VECTORSTORE_DIR = os.getenv("VECTORSTORE_DIR", "vectorstore")
    DATA_DIR = os.getenv("DATA_DIR", "data/raw")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chat_logs.db")

    TOP_K = int(os.getenv("TOP_K", 3))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))


settings = Settings()
