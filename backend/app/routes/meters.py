# backend/app/routes/meters.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.database.connection import get_db
from backend.app.schemas.meter import MeterCreate, MeterUpdate, MeterResponse
from backend.app.services.meter_service import MeterService

router = APIRouter(prefix="/meters", tags=["Smart Meters & Grid Registry"])

@router.get("", response_model=List[MeterResponse])
def list_meters(
    status: Optional[str] = Query(None, description="Filter by meter status (Active, Suspended, Disconnected)"),
    db: Session = Depends(get_db)
):
    """Retrieve all smart energy meters in the grid registry."""
    return MeterService.get_all(db, status=status)

@router.get("/{id_or_serial}", response_model=MeterResponse)
def get_meter(id_or_serial: str, db: Session = Depends(get_db)):
    """Retrieve meter details by integer ID or serial number (e.g. MTR-2026-8801)."""
    if id_or_serial.isdigit():
        meter = MeterService.get_by_id(db, int(id_or_serial))
    else:
        meter = MeterService.get_by_serial(db, id_or_serial)

    if not meter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Smart meter '{id_or_serial}' not found."
        )
    return meter

@router.post("", response_model=MeterResponse, status_code=status.HTTP_201_CREATED)
def allocate_meter(meter_in: MeterCreate, db: Session = Depends(get_db)):
    """Provision, allocate, and energize a new meter for an approved application."""
    try:
        return MeterService.allocate_meter(db, meter_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{meter_id}", response_model=MeterResponse)
def update_meter(
    meter_id: int,
    meter_in: MeterUpdate,
    db: Session = Depends(get_db)
):
    """Update meter reading, status, or feeder line assignment."""
    updated = MeterService.update_meter(db, meter_id, meter_in)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meter with ID {meter_id} not found."
        )
    return updated
