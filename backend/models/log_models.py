from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.core.database import Base

class Log(Base):
    __tablename__ = "logs"

    id=Column(Integer, primary_key=True, index=True)
    text=Column(String)
    prediction=Column(String)
    model=Column(String)
    negative=Column(Float)
    neutral=Column(Float)
    positive=Column(Float)
    latency=Column(Float)
    timestamp=Column(DateTime, default=datetime.now())