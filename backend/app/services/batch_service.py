from sqlalchemy.orm import Session
from sqlalchemy import insert
from app.core.database import SessionLocal
from models.batch_job_model import BatchJob
from models.batch_result_model import BatchResult
from app.services.ml_service import predict_batch

import pandas as pd
import time
from datetime import datetime, UTC

def process_batch_job(job_id: int, file_path: str, model:str):
    db = SessionLocal()

    try:
        job = db.query(BatchJob).filter(BatchJob.id == job_id).all()

        if not job:
            return
    
        #mark processing
        job.status = "Processing"
        db.commit()

        #Read CSV
        df = pd.read_csv(file_path)

        total_rows = len(df)
        
        start_time = time.perf_counter()

        start = time.perf_counter()
        preds, probs = predict_batch(df["text"], model)
        inference_time = time.perf_counter() - start

        job.inference_time = inference_time
        job.throughput = total_rows/inference_time

        BUFFER = 20
        results_buffer=[]
        for index, (text, pred, prob) in enumerate(zip(df["text"], preds, probs)):
            results_buffer.append({
                "job_id": job.id,
                "text": text,
                "prediction": pred,
                "confidence": float(max(prob)),
                "model_used": job.model_name
            })

            
            if (index+1) % BUFFER == 0:
                job.processed_rows = index + 1
                job.progress = round(
                    ((index+1)/total_rows)*100, 2
                )

                if len(results_buffer) >= BUFFER:
                    stmt = insert(BatchResult).values(results_buffer)
                    db.execute(stmt)
                    db.commit()

                    results_buffer.clear()

        if results_buffer:
            stmt = insert(BatchResult).values(results_buffer)
            db.execute(stmt)
            db.commit()

        end_time = time.perf_counter()

        job.status = "completed"

        job.processing_time = round(end_time - start_time, 4)
        job.completed_at = datetime.now(UTC)
        job.processed_rows = total_rows
        job.progress = 100

        db.commit()

    except Exception as e:
        job.status = "failed"
        job.error_message = str(e)
        db.commit()

    finally:
        db.close()
