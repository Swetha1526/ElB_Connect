# backend/app/services/application_service.py
from datetime import datetime, timezone
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, desc, asc

from backend.app.models.application import Application
from backend.app.models.consumer import Consumer
from backend.app.models.audit_log import AuditLog
from backend.app.schemas.application import ApplicationCreate, ApplicationUpdate
from backend.app.utils.helpers import calculate_quotation, generate_application_number

class ApplicationService:
    @staticmethod
    def get_applications(
        db: Session,
        search: Optional[str] = None,
        status: Optional[str] = None,
        category: Optional[str] = None,
        substation: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> Tuple[List[Application], int]:
        """Fetch paginated, filtered, and searched electricity connection applications."""
        query = db.query(Application).join(Consumer).options(
            joinedload(Application.consumer),
            joinedload(Application.inspection),
            joinedload(Application.meter),
            joinedload(Application.audit_logs)
        )

        # Filters
        if status and status != "All":
            query = query.filter(Application.status == status)
        if category and category != "All":
            query = query.filter(Application.category == category)
        if substation and substation != "All":
            query = query.filter(Application.substation_name == substation)

        # Full-text search
        if search and search.strip():
            term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Application.application_number.ilike(term),
                    Consumer.full_name.ilike(term),
                    Consumer.phone.ilike(term),
                    Consumer.email.ilike(term),
                    Consumer.address.ilike(term),
                    Application.substation_name.ilike(term)
                )
            )

        total_count = query.count()

        # Sorting
        sort_column = getattr(Application, sort_by, Application.created_at)
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))

        # Pagination
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return items, total_count

    @staticmethod
    def get_by_id(db: Session, application_id: int) -> Optional[Application]:
        """Get single application by integer primary key."""
        return db.query(Application).options(
            joinedload(Application.consumer),
            joinedload(Application.inspection),
            joinedload(Application.meter),
            joinedload(Application.audit_logs)
        ).filter(Application.id == application_id).first()

    @staticmethod
    def get_by_number(db: Session, application_number: str) -> Optional[Application]:
        """Get single application by unique string identifier e.g. APP-2026-1001."""
        return db.query(Application).options(
            joinedload(Application.consumer),
            joinedload(Application.inspection),
            joinedload(Application.meter),
            joinedload(Application.audit_logs)
        ).filter(Application.application_number == application_number.strip().upper()).first()

    @staticmethod
    def create_application(db: Session, app_in: ApplicationCreate) -> Application:
        """Create new consumer (if not existing) and new connection application."""
        consumer_id = app_in.consumer_id

        # If consumer details passed, create new consumer record
        if not consumer_id and app_in.consumer:
            consumer = Consumer(
                full_name=app_in.consumer.full_name,
                email=app_in.consumer.email,
                phone=app_in.consumer.phone,
                national_id=app_in.consumer.national_id,
                address=app_in.consumer.address,
                city=app_in.consumer.city,
                pincode=app_in.consumer.pincode,
                consumer_category=app_in.consumer.consumer_category or app_in.category
            )
            db.add(consumer)
            db.flush()
            consumer_id = consumer.id
        elif not consumer_id:
            raise ValueError("Either consumer_id or full consumer details must be provided.")

        # Compute initial quotation
        quotation = calculate_quotation(app_in.category, app_in.requested_load_kw, app_in.phase)

        # Generate unique Application Number
        app_num = generate_application_number()
        # Verify uniqueness
        while db.query(Application).filter(Application.application_number == app_num).first():
            app_num = generate_application_number()

        new_app = Application(
            application_number=app_num,
            consumer_id=consumer_id,
            connection_type=app_in.connection_type,
            category=app_in.category,
            requested_load_kw=app_in.requested_load_kw,
            phase=app_in.phase,
            premises_type=app_in.premises_type,
            substation_name=app_in.substation_name,
            status="Submitted",
            sanctioned_load_kw=None,
            quotation_amount=quotation,
            payment_status="Pending",
            remarks=app_in.remarks
        )
        db.add(new_app)
        db.flush()

        # Create Initial Audit Log
        audit = AuditLog(
            application_id=new_app.id,
            action="APPLICATION_SUBMITTED",
            performed_by=app_in.consumer.full_name if app_in.consumer else "Consumer Portal",
            old_status=None,
            new_status="Submitted",
            notes=f"Application registered for {app_in.requested_load_kw} kW {app_in.category} connection."
        )
        db.add(audit)
        db.commit()
        db.refresh(new_app)
        return ApplicationService.get_by_id(db, new_app.id)

    @staticmethod
    def update_application(db: Session, application_id: int, app_in: ApplicationUpdate) -> Optional[Application]:
        """Update application attributes, manage lifecycle transitions and log audit history."""
        app = db.query(Application).filter(Application.id == application_id).first()
        if not app:
            return None

        old_status = app.status
        update_data = app_in.model_dump(exclude_unset=True, exclude={"action_note", "performed_by"})

        # Recalculate quotation if load/category/phase changes and quotation not explicitly overridden
        recalc_needed = any(k in update_data for k in ["category", "requested_load_kw", "phase"])
        if recalc_needed and "quotation_amount" not in update_data:
            cat = update_data.get("category", app.category)
            load = update_data.get("requested_load_kw", app.requested_load_kw)
            ph = update_data.get("phase", app.phase)
            update_data["quotation_amount"] = calculate_quotation(cat, load, ph)

        for field, value in update_data.items():
            setattr(app, field, value)

        app.updated_at = datetime.now(timezone.utc)

        # Audit Log on status change or note
        new_status = app.status
        action_note = app_in.action_note or f"Updated application details."
        performed_by = app_in.performed_by or "Officer"

        if old_status != new_status or app_in.action_note:
            audit = AuditLog(
                application_id=app.id,
                action="STATUS_UPDATE" if old_status != new_status else "APPLICATION_UPDATED",
                performed_by=performed_by,
                old_status=old_status if old_status != new_status else None,
                new_status=new_status,
                notes=action_note
            )
            db.add(audit)

        db.commit()
        return ApplicationService.get_by_id(db, app.id)

    @staticmethod
    def delete_application(db: Session, application_id: int) -> bool:
        """Delete / Cancel an application."""
        app = db.query(Application).filter(Application.id == application_id).first()
        if not app:
            return False
        db.delete(app)
        db.commit()
        return True
