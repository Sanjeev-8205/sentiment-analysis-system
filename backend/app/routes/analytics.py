from fastapi import APIRouter
from sqlalchemy import func
from app.core.database import SessionLocal
from models.log_models import Log

router = APIRouter()

@router.get("/analytics")
def get_analytics():
    db = SessionLocal()

    try:
        avg_negative = db.query(func.avg(Log.negative)).scalar()
        avg_neutral = db.query(func.avg(Log.neutral)).scalar()
        avg_positive = db.query(func.avg(Log.positive)).scalar()

        avg_scores={
            "Negative": float(avg_negative or 0),
            "Neutral": float(avg_neutral or 0),
            "Positive": float(avg_positive or 0)
        }

        return avg_scores
    
    finally:
        db.close()