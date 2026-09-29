# backend/app/models/application.py
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.connection import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    application_number = Column(String(30), unique=True, nullable=False, index=True)
    consumer_id = Column(Integer, ForeignKey("consumers.id", ondelete="CASCADE"), nullable=False)
    
    connection_type = Column(String(40), nullable=False, default="New Connection")  # New Connection, Load Enhancement, Tariff Change
    category = Column(String(30), nullable=False)  # Domestic, Commercial, Industrial, Agricultural
    requested_load_kw = Column(Float, nullable=False)
    phase = Column(String(20), nullable=False, default="Single Phase")  # Single Phase, Three Phase
    premises_type = Column(String(20), nullable=False, default="Owned")  # Owned, Rented, Leased
    substation_name = Column(String(100), nullable=False, default="Central Substation 33/11kV")
    
    status = Column(
        String(40),
        nullable=False,
        default="Submitted"
    )  # Submitted, Document_Verified, Field_Inspection_Scheduled, Inspection_Approved, Payment_Pending, Meter_Assigned_Active, Rejected
    
    sanctioned_load_kw = Column(Float, nullable=True)
    quotation_amount = Column(Float, nullable=False, default=0.0)
    payment_status = Column(String(20), nullable=False, default="Pending")  # Pending, Paid, Waived
    remarks = Column(Text, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    consumer = relationship("Consumer", back_populates="applications")
    inspection = relationship("Inspection", back_populates="application", uselist=False, cascade="all, delete-orphan")
    meter = relationship("Meter", back_populates="application", uselist=False, cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="application", cascade="all, delete-orphan", order_by="AuditLog.timestamp.desc()")

    def __repr__(self):
        return f"<Application(num='{self.application_number}', status='{self.status}', load={self.requested_load_kw}kW)>"
