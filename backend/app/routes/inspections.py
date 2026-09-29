# backend/app/routes/inspections.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database.connection import get_db
from backend.app.schemas.inspection import InspectionCreate, InspectionUpdate, InspectionResponse
from backend.app.services.inspection_service import InspectionService

router = APIRouter(prefix="/inspections", tags=["Field Inspections"])

@router.get("", response_model=List[InspectionResponse])
def list_inspections(db: Session = Depends(get_db)):
    """List all field inspections."""
    return InspectionService.get_all(db)

@router.get("/{inspection_id}", response_model=InspectionResponse)
def get_inspection(inspection_id: int, db: Session = Depends(get_db)):
    """Get inspection details by ID."""
    insp = InspectionService.get_by_id(db, inspection_id)
    if not insp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inspection with ID {inspection_id} not found."
        )
    return insp

@router.get("/application/{application_id}", response_model=InspectionResponse)
def get_inspection_by_app(application_id: int, db: Session = Depends(get_db)):
    """Get inspection details for an application."""
    insp = InspectionService.get_by_application_id(db, application_id)
    if not insp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No inspection found for application {application_id}."
        )
    return insp

@router.post("", response_model=InspectionResponse, status_code=status.HTTP_201_CREATED)
def schedule_inspection(insp_in: InspectionCreate, db: Session = Depends(get_db)):
    """Schedule a field feasibility survey for an application."""
    try:
        return InspectionService.create_or_schedule(db, insp_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{inspection_id}", response_model=InspectionResponse)
def complete_inspection(
    inspection_id: int,
    insp_up: InspectionUpdate,
    db: Session = Depends(get_db)
):
    """Record site measurements (pole distance, transformer capacity) and complete inspection."""
    insp = InspectionService.complete_inspection(db, inspection_id, insp_up)
    if not insp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inspection with ID {inspection_id} not found."
        )
    return insp
