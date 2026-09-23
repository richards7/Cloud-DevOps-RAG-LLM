from typing import List
from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str


class SourceChunk(BaseModel):
    source: str
    text: str


class ChatResponse(BaseModel):
    answer: str
    provider: str
    sources: List[SourceChunk]
    latency_ms: int
