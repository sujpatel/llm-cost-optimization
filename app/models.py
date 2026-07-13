from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String

from app.db import Base

class ModelCache(Base):
    __tablename__ = "model_cache"

    model_id = Column(String, primary_key=True)
    canonical_slug = Column(String, nullable=False, index=True)
    is_free = Column(Boolean, nullable=False)
    input_price = Column(Float, nullable=False)
    output_price = Column(Float, nullable=False)
    last_synced = Column(DateTime, default=datetime.utcnow)


class BenchmarkCache(Base):
    __tablename__ = "benchmark_cache"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(String, ForeignKey("model_cache.model_id"), nullable=False)
    task_type = Column(String, nullable=False, index=True)
    score = Column(Float, nullable=False)
    last_synced = Column(DateTime, default=datetime.utcnow)


class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_type = Column(String, nullable=False)
    free_model_used = Column(String, nullable=False)
    paid_model_reference = Column(String, nullable=False)
    free_score = Column(Float, nullable=False)
    paid_score = Column(Float, nullable=False)
    tokens_used = Column(Integer, nullable=False)
    cost_saved = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

