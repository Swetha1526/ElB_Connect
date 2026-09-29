# backend/app/routes/stats.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.connection import get_db
from backend.app.schemas.stats import DashboardStatsResponse
from backend.app.services.stats_service import StatsService

router = APIRouter(prefix="/stats", tags=["Dashboard & Analytics"])

@router.get("/dashboard", response_model=DashboardStatsResponse)
def get_dashboard_analytics(db: Session = Depends(get_db)):
    """Retrieve aggregate KPIs, tariff distribution, and live grid activity for the dashboard."""
    return StatsService.get_dashboard_stats(db)
