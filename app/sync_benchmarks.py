import os

import httpx
from dotenv import load_dotenv

from app.db import SessionLocal
from app.models import BenchmarkCache, ModelCache

load_dotenv()

OPENROUTER_BENCHMARKS_URL = "https://openrouter.ai/api/v1/benchmarks"
API_KEY = os.getenv("OPENROUTER_API_KEY")

INDEX_TO_TASK_TYPE = {
    "intelligence_index": "intelligence",
    "coding_index": "coding",
    "agentic_index": "agentic",
}

def upsert_benchmark(db, model_id, task_type, score):
    existing = (
        db.query(BenchmarkCache).filter_by(model_id=model_id, task_type=task_type).first()
    )
    if existing:
        existing.score = score
    else:
        db.add(BenchmarkCache(model_id=model_id, task_type=task_type, score=score))
        
def sync_benchmarks():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = httpx.get(
        OPENROUTER_BENCHMARKS_URL,
        headers=headers,
        params={"source": "artificial-analysis"},
        timeout=30,
    )
    response.raise_for_status()
    entries = response.json()["data"]

    db = SessionLocal()
    rows_written = 0
    try:
        for entry in entries:
            matched_models = (
                db.query(ModelCache)
                .filter_by(canonical_slug=entry["model_permaslug"])
                .all()
            )
            if not matched_models:
                continue

            for index_field, task_type in INDEX_TO_TASK_TYPE.items():
                score = entry.get(index_field)
                if score is None:
                    continue
                for model in matched_models:
                    upsert_benchmark(db, model.model_id, task_type, score)
                    rows_written += 1

        db.commit()
        print(f"Synced {rows_written} benchmark rows from {len(entries)} entries.")
    finally:
        db.close()


if __name__ == "__main__":
    sync_benchmarks()