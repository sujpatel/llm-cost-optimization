import httpx

from app.db import SessionLocal
from app.models import ModelCache

OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"

def sync_models():
    response = httpx.get(OPENROUTER_MODELS_URL, timeout=30)
    response.raise_for_status()
    models = response.json()["data"]
    
    db = SessionLocal()
    try:
        for model in models:
            input_price = float(model["pricing"]["prompt"])
            output_price = float(model["pricing"]["completion"])
            is_free = input_price == 0 and output_price == 0
            
            existing = db.get(ModelCache, model["id"])
            if existing:
                existing.canonical_slug = model["canonical_slug"]
                existing.is_free = is_free
                existing.input_price = input_price
                existing.output_price = output_price
            else:
                db.add(
                    ModelCache(
                        model_id=model["id"],
                        canonical_slug=model["canonical_slug"],
                        is_free=is_free,
                        input_price=input_price,
                        output_price=output_price,
                    )
                )
        db.commit()
        print(f"Synced {len(models)} models.")
    finally:
        db.close()

if __name__=="__main__":
    sync_models()
                