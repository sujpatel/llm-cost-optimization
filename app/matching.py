from app.models import BenchmarkCache, ModelCache

def find_best_models(db, task_type, max_price_per_million=0):
    max_price = max_price_per_million / 1_000_000

    results = (
        db.query(BenchmarkCache, ModelCache)
        .join(ModelCache, BenchmarkCache.model_id == ModelCache.model_id)
        .filter(BenchmarkCache.task_type == task_type)
        .order_by(BenchmarkCache.score.desc())
        .all()
    )

    if not results:
        return None, None

    paid_reference = results[0]

    budget_pick = next(
        (r for r in results if r[1].input_price <= max_price and r[1].output_price <= max_price),
        None,
    )

    return budget_pick, paid_reference
