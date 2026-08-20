from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db import get_db
from app.matching import find_best_models
from app.completion import get_completion
from app.cost import calculate_cost_saved, categorize_quality_gap
from app.models import Query
from app.scheduler import start_scheduler

app = FastAPI()


@app.on_event("startup")
def on_startup():
    start_scheduler()


class AskRequest(BaseModel):
    prompt: str
    task_type: str
    max_price_per_million: float = 0


@app.post("/v1/ask")
def ask(request: AskRequest, db: Session = Depends(get_db)):
    budget_pick, paid_reference = find_best_models(db, request.task_type, request.max_price_per_million)

    if not budget_pick:
        return {"error": f"No model found within budget for task_type '{request.task_type}'"}

    free_bench, free_model = budget_pick
    paid_bench, paid_model = paid_reference

    result = get_completion(free_model.model_id, request.prompt)

    cost_saved = calculate_cost_saved(
        result["prompt_tokens"],
        result["completion_tokens"],
        paid_model.input_price,
        paid_model.output_price,
    )
    quality_gap = categorize_quality_gap(free_bench.score, paid_bench.score)

    db.add(Query(
        task_type=request.task_type,
        free_model_used=free_model.model_id,
        paid_model_reference=paid_model.model_id,
        free_score=free_bench.score,
        paid_score=paid_bench.score,
        tokens_used=result["prompt_tokens"] + result["completion_tokens"],
        cost_saved=cost_saved,
    ))
    db.commit()

    return {
        "answer": result["answer"],
        "model_used": free_model.model_id,
        "cost_saved": cost_saved,
        "quality_gap": quality_gap,
    }


@app.get("/v1/savings")
def savings(db: Session = Depends(get_db)):
    total_saved = db.query(func.sum(Query.cost_saved)).scalar() or 0
    query_count = db.query(func.count(Query.id)).scalar() or 0
    avg_gap = db.query(func.avg(Query.paid_score - Query.free_score)).scalar() or 0

    return {
        "total_cost_saved": total_saved,
        "query_count": query_count,
        "average_quality_gap": avg_gap,
    }
