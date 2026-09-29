# backend/app/services/grievance_service.py
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from backend.app.models.grievance import Grievance
from backend.app.models.consumer import Consumer
from backend.app.models.meter import Meter
from backend.app.schemas.grievance import GrievanceCreate, GrievanceCreatePublic, GrievanceUpdate
from backend.app.utils.helpers import generate_grievance_number

class GrievanceService:
    @staticmethod
    def get_all(
        db: Session,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Grievance]:
        query = db.query(Grievance).options(
            joinedload(Grievance.consumer),
            joinedload(Grievance.meter)
        )

        if status and status != "All":
            query = query.filter(Grievance.status == status)
        if priority and priority != "All":
            query = query.filter(Grievance.priority == priority)

        if search and search.strip():
            term = f"%{search.strip()}%"
            query = query.join(Consumer).filter(
                or_(
                    Grievance.grievance_number.ilike(term),
                    Grievance.category.ilike(term),
                    Grievance.description.ilike(term),
                    Consumer.full_name.ilike(term),
                    Consumer.phone.ilike(term)
                )
            )

        return query.order_by(Grievance.created_at.desc()).all()

    @staticmethod
    def get_by_id(db: Session, grievance_id: int) -> Optional[Grievance]:
        return db.query(Grievance).options(
            joinedload(Grievance.consumer),
            joinedload(Grievance.meter)
        ).filter(Grievance.id == grievance_id).first()

    @staticmethod
    def create_grievance(db: Session, grv_in: GrievanceCreate) -> Grievance:
        grv_num = generate_grievance_number()
        while db.query(Grievance).filter(Grievance.grievance_number == grv_num).first():
            grv_num = generate_grievance_number()

        grievance = Grievance(
            grievance_number=grv_num,
            consumer_id=grv_in.consumer_id,
            meter_id=grv_in.meter_id,
            category=grv_in.category,
            priority=grv_in.priority,
            description=grv_in.description,
            status="Registered",
            assigned_lineman=grv_in.assigned_lineman,
            resolution_notes=grv_in.resolution_notes
        )
        db.add(grievance)
        db.commit()
        db.refresh(grievance)
        return GrievanceService.get_by_id(db, grievance.id)

    @staticmethod
    def create_public_grievance(db: Session, grv_in: GrievanceCreatePublic) -> Grievance:
        """Register public complaint; create or lookup consumer and optionally resolve meter."""
        # Find or create consumer
        consumer = db.query(Consumer).filter(
            or_(Consumer.phone == grv_in.phone, Consumer.email == grv_in.email)
        ).first()

        if not consumer:
            consumer = Consumer(
                full_name=grv_in.full_name,
                email=grv_in.email or f"{grv_in.phone}@consumer.voltflow.in",
                phone=grv_in.phone,
                national_id="TEMP-GRIEVANCE",
                address=grv_in.address,
                city="Metro City",
                pincode="110001",
                consumer_category="Domestic"
            )
            db.add(consumer)
            db.flush()

        meter_id = None
        if grv_in.meter_serial_number:
            meter = db.query(Meter).filter(Meter.meter_serial_number == grv_in.meter_serial_number.strip()).first()
            if meter:
                meter_id = meter.id

        grv_num = generate_grievance_number()
        grievance = Grievance(
            grievance_number=grv_num,
            consumer_id=consumer.id,
            meter_id=meter_id,
            category=grv_in.category,
            priority=grv_in.priority,
            description=grv_in.description,
            status="Registered"
        )
        db.add(grievance)
        db.commit()
        db.refresh(grievance)
        return GrievanceService.get_by_id(db, grievance.id)

    @staticmethod
    def update_grievance(db: Session, grievance_id: int, grv_in: GrievanceUpdate) -> Optional[Grievance]:
        grievance = db.query(Grievance).filter(Grievance.id == grievance_id).first()
        if not grievance:
            return None

        update_data = grv_in.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(grievance, k, v)

        if grv_in.status == "Resolved" and not grievance.resolved_at:
            grievance.resolved_at = datetime.now(timezone.utc)

        grievance.updated_at = datetime.now(timezone.utc)
        db.commit()
        return GrievanceService.get_by_id(db, grievance.id)
