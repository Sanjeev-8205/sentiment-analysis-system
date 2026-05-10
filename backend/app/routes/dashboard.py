from fastapi import APIRouter
from app.services.metrics_service.dashboard_metrics_service import dashboard_metrics_aggregator
from app.schemas.request_schema import InputData

router = APIRouter()

@router.get("/dashboard")
def get_dashboard_metrics():
    return dashboard_metrics_aggregator()