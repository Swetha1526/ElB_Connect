# backend/app/schemas/stats.py
from pydantic import BaseModel
from typing import Dict, List, Any

class CategoryCount(BaseModel):
    category: str
    count: int
    total_load_kw: float

class StatusCount(BaseModel):
    status: str
    count: int

class SubstationStat(BaseModel):
    substation_name: str
    total_applications: int
    active_meters: int
    total_load_kw: float

class DashboardStatsResponse(BaseModel):
    total_applications: int
    pending_verifications: int
    pending_inspections: int
    pending_payments: int
    active_meters: int
    total_sanctioned_load_kw: float
    total_sanctioned_load_mw: float
    total_grievances: int
    active_grievances: int
    resolved_grievances: int
    estimated_revenue_inr: float
    
    status_distribution: List[StatusCount]
    category_distribution: List[CategoryCount]
    substation_metrics: List[SubstationStat]
    recent_activity: List[Dict[str, Any]]
