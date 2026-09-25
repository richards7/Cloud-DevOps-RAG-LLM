import json
import time
import logging

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.schemas import ChatRequest, ChatResponse, SourceChunk
from app.rag.retriever import retrieve
from app.rag.prompt_builder import build_prompt
from app.llm.router import get_router
from app.db.database import init_db, get_db
from app.db.models import ChatLog

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Cloud & DevOps RAG Assistant",
    description="A RAG-powered chatbot answering cloud/DevOps questions.",
    version="1.0.0",
)

# Add CORS middleware for frontend decoupling
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    start = time.time()

    chunks = retrieve(request.query)
    prompt = build_prompt(request.query, chunks)

    router = get_router()
    result = router.generate(prompt)

    latency_ms = int((time.time() - start) * 1000)

    log_entry = ChatLog(
        query=request.query,
        retrieved_sources=json.dumps([c["source"] for c in chunks]),
        response=result["text"],
        provider=result["provider"],
        latency_ms=latency_ms,
    )
    db.add(log_entry)
    db.commit()

    return ChatResponse(
        answer=result["text"],
        provider=result["provider"],
        sources=[SourceChunk(**c) for c in chunks],
        latency_ms=latency_ms,
    )
