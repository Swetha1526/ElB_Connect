# backend/app/services/meter_service.py
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Session

from backend.app.models.meter import Meter
from backend.app.models.application import Application
from backend.app.models.audit_log import AuditLog
from backend.app.schemas.meter import MeterCreate, MeterUpdate
from backend.app.utils.helpers import generate_meter_serial

class MeterService:
    @staticmethod
    def get_all(db: Session, status: Optional[str] = None) -> List[Meter]:
        query = db.query(Meter)
        if status and status != "All":
            query = query.filter(Meter.status == status)
        return query.order_by(Meter.installation_date.desc()).all()

    @staticmethod
    def get_by_id(db: Session, meter_id: int) -> Optional[Meter]:
        return db.query(Meter).filter(Meter.id == meter_id).first()

    @staticmethod
    def get_by_serial(db: Session, serial: str) -> Optional[Meter]:
        return db.query(Meter).filter(Meter.meter_serial_number == serial.strip().upper()).first()

    @staticmethod
    def allocate_meter(db: Session, meter_in: MeterCreate) -> Meter:
        """Provision and energize a new electric meter for an approved application."""
        app = db.query(Application).filter(Application.id == meter_in.application_id).first()
        if not app:
            raise ValueError(f"Application {meter_in.application_id} does not exist.")

        existing = db.query(Meter).filter(Meter.application_id == meter_in.application_id).first()
        if existing:
            raise ValueError(f"Application already has assigned meter: {existing.meter_serial_number}")

        # Serial generation if omitted
        serial = meter_in.meter_serial_number or generate_meter_serial()
        while db.query(Meter).filter(Meter.meter_serial_number == serial).first():
            serial = generate_meter_serial()

        meter = Meter(
            application_id=meter_in.application_id,
            meter_serial_number=serial,
            meter_type=meter_in.meter_type,
            phase=meter_in.phase or app.phase,
            initial_reading_kwh=meter_in.initial_reading_kwh,
            current_reading_kwh=meter_in.current_reading_kwh or meter_in.initial_reading_kwh,
            substation_name=meter_in.substation_name or app.substation_name,
            feeder_line=meter_in.feeder_line,
            status=meter_in.status or "Active",
            installation_date=datetime.now(timezone.utc)
        )
        db.add(meter)

        # Update application state
        old_status = app.status
        app.status = "Meter_Assigned_Active"
        app.payment_status = "Paid"
        if not app.sanctioned_load_kw:
            app.sanctioned_load_kw = app.requested_load_kw

        audit = AuditLog(
            application_id=app.id,
            action="METER_ALLOCATED_ACTIVE",
            performed_by="Meter Allocation Officer",
            old_status=old_status,
            new_status="Meter_Assigned_Active",
            notes=f"Meter serial {meter.meter_serial_number} ({meter.meter_type}) commissioned and energized."
        )
        db.add(audit)
        db.commit()
        db.refresh(meter)
        return meter

    @staticmethod
    def update_meter(db: Session, meter_id: int, meter_in: MeterUpdate) -> Optional[Meter]:
        meter = db.query(Meter).filter(Meter.id == meter_id).first()
        if not meter:
            return None

        update_data = meter_in.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(meter, k, v)

        meter.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(meter)
        return meter
