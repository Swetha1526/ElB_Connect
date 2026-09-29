# backend/app/models/inspection.py
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.connection import Base

class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    inspector_name = Column(String(100), nullable=False)
    feasibility_status = Column(String(40), nullable=False, default="Feasible")  # Feasible, Transformer_Upgrade_Required, Pole_Extension_Needed, Non_Feasible
    pole_distance_meters = Column(Float, nullable=False, default=25.0)
    transformer_id = Column(String(40), nullable=False, default="TR-MAIN-01")
    transformer_capacity_kva = Column(Float, nullable=False, default=100.0)
    meter_box_ready = Column(Boolean, nullable=False, default=True)
    remarks = Column(Text, nullable=True)
    
    scheduled_date = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    application = relationship("Application", back_populates="inspection")

    def __repr__(self):
        return f"<Inspection(app_id={self.application_id}, inspector='{self.inspector_name}', status='{self.feasibility_status}')>"
