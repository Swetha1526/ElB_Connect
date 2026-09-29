# backend/app/routes/applications.py
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.database.connection import get_db
from backend.app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    PaginatedApplicationResponse
)
from backend.app.services.application_service import ApplicationService

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.get("", response_model=PaginatedApplicationResponse)
def list_applications(
    search: Optional[str] = Query(None, description="Search across application number, applicant name, phone, address"),
    status: Optional[str] = Query(None, description="Filter by application status"),
    category: Optional[str] = Query(None, description="Filter by consumer tariff category"),
    substation: Optional[str] = Query(None, description="Filter by grid substation"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", description="Sort direction (asc or desc)"),
    db: Session = Depends(get_db)
):
    """List connection applications with multi-field search, status filtering, and pagination."""
    items, total_count = ApplicationService.get_applications(
        db=db,
        search=search,
        status=status,
        category=category,
        substation=substation,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order
    )
    total_pages = (total_count + page_size - 1) // page_size if total_count > 0 else 1
    return PaginatedApplicationResponse(
        total=total_count,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=items
    )

@router.get("/{id_or_number}", response_model=ApplicationResponse)
def get_application(id_or_number: str, db: Session = Depends(get_db)):
    """Retrieve full application dossier by integer ID or application number string (e.g., APP-2026-1001)."""
    if id_or_number.isdigit():
        app = ApplicationService.get_by_id(db, int(id_or_number))
    else:
        app = ApplicationService.get_by_number(db, id_or_number)

    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Electricity connection application '{id_or_number}' not found."
        )
    return app

@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(app_in: ApplicationCreate, db: Session = Depends(get_db)):
    """Submit a new electricity connection request with auto-quotation calculation."""
    try:
        new_app = ApplicationService.create_application(db, app_in)
        return new_app
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create application: {str(e)}")

@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int,
    app_in: ApplicationUpdate,
    db: Session = Depends(get_db)
):
    """Update application details, sanction load, update payment or advance lifecycle state."""
    updated = ApplicationService.update_application(db, application_id, app_in)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found."
        )
    return updated

@router.delete("/{application_id}", status_code=status.HTTP_200_OK)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    """Cancel and delete an electricity connection application."""
    success = ApplicationService.delete_application(db, application_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with ID {application_id} not found."
        )
    return {"success": True, "message": f"Application {application_id} deleted successfully."}
