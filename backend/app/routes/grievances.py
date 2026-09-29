# backend/app/routes/grievances.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.database.connection import get_db
from backend.app.schemas.grievance import (
    GrievanceCreate,
    GrievanceCreatePublic,
    GrievanceUpdate,
    GrievanceResponse
)
from backend.app.services.grievance_service import GrievanceService

router = APIRouter(prefix="/grievances", tags=["Outage & Service Grievances"])

@router.get("", response_model=List[GrievanceResponse])
def list_grievances(
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    search: Optional[str] = Query(None, description="Search term across grievance number, category, description"),
    db: Session = Depends(get_db)
):
    """List all outage and power breakdown grievances."""
    return GrievanceService.get_all(db, status=status, priority=priority, search=search)

@router.get("/{grievance_id}", response_model=GrievanceResponse)
def get_grievance(grievance_id: int, db: Session = Depends(get_db)):
    """Retrieve grievance ticket details."""
    grv = GrievanceService.get_by_id(db, grievance_id)
    if not grv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Grievance with ID {grievance_id} not found."
        )
    return grv

@router.post("", response_model=GrievanceResponse, status_code=status.HTTP_201_CREATED)
def create_grievance(grv_in: GrievanceCreate, db: Session = Depends(get_db)):
    """Log an internal outage/service grievance."""
    try:
        return GrievanceService.create_grievance(db, grv_in)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/public", response_model=GrievanceResponse, status_code=status.HTTP_201_CREATED)
def create_public_grievance(grv_in: GrievanceCreatePublic, db: Session = Depends(get_db)):
    """Self-service complaint registration for electricity consumers."""
    try:
        return GrievanceService.create_public_grievance(db, grv_in)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{grievance_id}", response_model=GrievanceResponse)
def update_grievance(
    grievance_id: int,
    grv_in: GrievanceUpdate,
    db: Session = Depends(get_db)
):
    """Assign lineman, update status, or resolve power breakdown."""
    updated = GrievanceService.update_grievance(db, grievance_id, grv_in)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Grievance with ID {grievance_id} not found."
        )
    return updated
