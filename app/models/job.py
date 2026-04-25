from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime, UTC
from app.db.base import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    correlation_id = Column(String(500), nullable=True)
    url = Column(Text, nullable=False)
    status = Column(String(50), default="pending")
    attempts = Column(Integer, default=0)
    http_status_code = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    title = Column(String(500), nullable=True)
    word_count = Column(Integer, nullable=True)
    top_words = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )