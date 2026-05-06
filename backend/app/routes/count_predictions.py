from fastapi import APIRouter
from app.core.database import SessionLocal
from models.log_models import Log

router = APIRouter()

@router.get("/count_predictions")
def get_counts():
    db = SessionLocal()

    try:
        prediction = db.query(Log.prediction)

        prediction_list = [p[0] for p in prediction]

        return prediction_list

    finally:
        db.close()