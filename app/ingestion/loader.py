"""
Reads raw documents from the data/ folder and splits them into
overlapping text chunks ready for embedding.

This is the ingestion entry point: drop new .md or .txt files into
data/raw/ and re-run scripts/ingest.py to feed the RAG pipeline.
"""
import os
from app.config import settings


def load_documents(data_dir: str = None):
    data_dir = data_dir or settings.DATA_DIR
    docs = []
    for fname in sorted(os.listdir(data_dir)):
        if fname.endswith((".md", ".txt")):
            path = os.path.join(data_dir, fname)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            docs.append({"source": fname, "text": text})
    return docs


def chunk_text(text: str, chunk_size: int = None, overlap: int = None):
    chunk_size = chunk_size or settings.CHUNK_SIZE
    overlap = overlap or settings.CHUNK_OVERLAP
    chunks = []
    start = 0
    text = text.strip()
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def load_and_chunk(data_dir: str = None):
    docs = load_documents(data_dir)
    all_chunks = []
    for doc in docs:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{doc['source']}_{i}",
                "text": chunk,
                "source": doc["source"],
            })
    return all_chunks
