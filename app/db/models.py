from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.db.database import Base


class ChatLog(Base):
    """
    Operational log of every chat interaction — separate from the
    vector store. Keeps: what was asked, which source chunks were
    retrieved, which LLM provider answered, the answer, and latency.
    """
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    retrieved_sources = Column(Text)     # JSON-encoded list of filenames
    response = Column(Text)
    provider = Column(String)
    latency_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
