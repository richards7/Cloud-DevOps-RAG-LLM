"""
Retrieves the top-k most relevant chunks from the vector store
for a given query.
"""
from app.ingestion.embed_store import get_collection
from app.config import settings


def retrieve(query: str, top_k: int = None):
    top_k = top_k or settings.TOP_K
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=top_k)

    docs = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    return [
        {"text": doc, "source": meta.get("source", "unknown")}
        for doc, meta in zip(docs, metadatas)
    ]
