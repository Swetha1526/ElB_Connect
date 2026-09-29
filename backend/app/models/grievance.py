# backend/app/models/grievance.py
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.connection import Base

class Grievance(Base):
    __tablename__ = "grievances"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    grievance_number = Column(String(30), unique=True, nullable=False, index=True)
    consumer_id = Column(Integer, ForeignKey("consumers.id", ondelete="CASCADE"), nullable=False)
    meter_id = Column(Integer, ForeignKey("meters.id", ondelete="SET NULL"), nullable=True)
    
    category = Column(String(40), nullable=False)  # Power Outage, Voltage Fluctuation, Meter Defect, Hazardous Sparking, Billing Inquiry
    priority = Column(String(20), nullable=False, default="Medium")  # Low, Medium, High, Critical
    description = Column(Text, nullable=False)
    status = Column(String(30), nullable=False, default="Registered")  # Registered, Assigned, In_Progress, Resolved, Closed
    assigned_lineman = Column(String(100), nullable=True)
    resolution_notes = Column(Text, nullable=True)
    
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    consumer = relationship("Consumer", back_populates="grievances")
    meter = relationship("Meter", back_populates="grievances")

    def __repr__(self):
        return f"<Grievance(num='{self.grievance_number}', category='{self.category}', priority='{self.priority}', status='{self.status}')>"
