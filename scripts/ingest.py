"""
Run this once (and again whenever you add/change files in data/raw/)
to (re)build the vector store that powers the RAG pipeline.

Usage:
    python scripts/ingest.py
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ingestion.loader import load_and_chunk
from app.ingestion.embed_store import add_chunks, reset_collection


def main():
    print("Resetting existing vector store collection...")
    reset_collection()

    print("Loading and chunking documents from data/raw ...")
    chunks = load_and_chunk()
    print(f"Loaded {len(chunks)} chunks from {len(set(c['source'] for c in chunks))} files.")

    if not chunks:
        print("No documents found in data/raw/. Add .md or .txt files and re-run.")
        return

    print("Embedding and storing in Chroma (this may take a moment on first run)...")
    add_chunks(chunks)

    print("Ingestion complete. Vector store is ready at ./vectorstore")


if __name__ == "__main__":
    main()
