from fastapi import APIRouter
from app.core.database import SessionLocal
from models.log_models import Log
import pandas as pd

router = APIRouter()

@router.get("/logs")
def get_logs():
    db = SessionLocal()

    try:
        logs = db.query(
            Log.text,
            Log.prediction,
            Log.model,
            Log.negative,
            Log.neutral,
            Log.positive,
            Log.latency,
            Log.timestamp
        ).order_by(Log.timestamp.desc()).limit(10).all()
    
        analytics = [
            {
                "text":row[0],
                "prediction":row[1],
                "model":row[2],
                "negative":row[3],
                "neutral":row[4],
                "positive":row[5],
                "latency":row[6],
                "timestamp":row[7]
            }
            for row in logs
        ]

        return analytics
    
    finally:
        db.close()