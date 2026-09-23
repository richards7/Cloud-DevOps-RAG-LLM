"""
Wraps a persistent Chroma vector store. Uses Chroma's built-in
default embedding function (a small local ONNX model) so no
embedding API key is required.
"""
import chromadb
from chromadb.utils import embedding_functions
from app.config import settings

_client = None
_collection = None

COLLECTION_NAME = "cloud_devops_kb"


def get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=settings.VECTORSTORE_DIR)
        ef = embedding_functions.DefaultEmbeddingFunction()
        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=ef,
        )
    return _collection


def add_chunks(chunks):
    if not chunks:
        return
    collection = get_collection()
    collection.add(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[{"source": c["source"]} for c in chunks],
    )


def reset_collection():
    """Deletes and recreates the collection — call before a fresh ingest."""
    global _client, _collection
    _client = chromadb.PersistentClient(path=settings.VECTORSTORE_DIR)
    try:
        _client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    _collection = None
