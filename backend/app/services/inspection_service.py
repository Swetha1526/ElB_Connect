# backend/app/services/inspection_service.py
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Session

from backend.app.models.inspection import Inspection
from backend.app.models.application import Application
from backend.app.models.audit_log import AuditLog
from backend.app.schemas.inspection import InspectionCreate, InspectionUpdate

class InspectionService:
    @staticmethod
    def get_all(db: Session) -> List[Inspection]:
        return db.query(Inspection).order_by(Inspection.created_at.desc()).all()

    @staticmethod
    def get_by_id(db: Session, inspection_id: int) -> Optional[Inspection]:
        return db.query(Inspection).filter(Inspection.id == inspection_id).first()

    @staticmethod
    def get_by_application_id(db: Session, application_id: int) -> Optional[Inspection]:
        return db.query(Inspection).filter(Inspection.application_id == application_id).first()

    @staticmethod
    def create_or_schedule(db: Session, insp_in: InspectionCreate) -> Inspection:
        """Schedule or register inspection for an application."""
        app = db.query(Application).filter(Application.id == insp_in.application_id).first()
        if not app:
            raise ValueError(f"Application with ID {insp_in.application_id} does not exist.")

        existing = db.query(Inspection).filter(Inspection.application_id == insp_in.application_id).first()
        if existing:
            # Update existing inspection
            for k, v in insp_in.model_dump().items():
                setattr(existing, k, v)
            db.commit()
            db.refresh(existing)
            return existing

        inspection = Inspection(
            application_id=insp_in.application_id,
            inspector_name=insp_in.inspector_name,
            feasibility_status=insp_in.feasibility_status,
            pole_distance_meters=insp_in.pole_distance_meters,
            transformer_id=insp_in.transformer_id,
            transformer_capacity_kva=insp_in.transformer_capacity_kva,
            meter_box_ready=insp_in.meter_box_ready,
            remarks=insp_in.remarks,
            scheduled_date=insp_in.scheduled_date or datetime.now(timezone.utc)
        )
        db.add(inspection)

        # Update application state
        app.status = "Field_Inspection_Scheduled"
        audit = AuditLog(
            application_id=app.id,
            action="INSPECTION_SCHEDULED",
            performed_by=insp_in.inspector_name,
            old_status=app.status,
            new_status="Field_Inspection_Scheduled",
            notes=f"Field inspection assigned to {insp_in.inspector_name}."
        )
        db.add(audit)
        db.commit()
        db.refresh(inspection)
        return inspection

    @staticmethod
    def complete_inspection(db: Session, inspection_id: int, insp_up: InspectionUpdate) -> Optional[Inspection]:
        """Record survey findings, feasibility status and automatically transition application state."""
        inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()
        if not inspection:
            return None

        update_data = insp_up.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(inspection, k, v)

        if not inspection.completed_at:
            inspection.completed_at = datetime.now(timezone.utc)

        # Update corresponding application
        app = db.query(Application).filter(Application.id == inspection.application_id).first()
        if app:
            old_status = app.status
            if inspection.feasibility_status == "Feasible":
                app.status = "Inspection_Approved"
                app.sanctioned_load_kw = app.requested_load_kw
                note = f"Feasibility passed. Pole distance: {inspection.pole_distance_meters}m, Transformer: {inspection.transformer_id}."
            elif inspection.feasibility_status == "Non_Feasible":
                app.status = "Rejected"
                note = f"Inspection failed: Technical constraints - {inspection.remarks or 'Grid capacity saturated'}."
            else:
                app.status = "Field_Inspection_Scheduled"
                note = f"Inspection marked: {inspection.feasibility_status}. Special approvals required."

            audit = AuditLog(
                application_id=app.id,
                action="INSPECTION_RECORDED",
                performed_by=inspection.inspector_name,
                old_status=old_status,
                new_status=app.status,
                notes=note
            )
            db.add(audit)

        db.commit()
        db.refresh(inspection)
        return inspection
