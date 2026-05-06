from app.core.database import SessionLocal
from models.log_models import Log

def log_predictions(text, prediction, prob, model, latency):
    db=SessionLocal()

    try:
        logs=Log(
            text=text,
            prediction=prediction,
            model=model,
            negative=prob[0],
            neutral=prob[1],
            positive=prob[2],
            latency=latency
        )

        db.add(logs)
        db.commit()

    finally:
        db.close()