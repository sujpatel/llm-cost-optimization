from app.db import SessionLocal
from app.matching import find_best_models

db = SessionLocal()
try:
    for task_type in ["coding", "intelligence", "agentic"]:
        budget_pick, paid_reference = find_best_models(db, task_type)

        print(f"--- {task_type} ---")
        if budget_pick:
            b_bench, b_model = budget_pick
            print(f"Free pick: {b_model.model_id} (score={b_bench.score}, free={b_model.is_free})")
        else:
            print("Free pick: none found")

        p_bench, p_model = paid_reference
        print(f"Paid reference: {p_model.model_id} (score={p_bench.score}, free={p_model.is_free})")
        print()
finally:
    db.close()
