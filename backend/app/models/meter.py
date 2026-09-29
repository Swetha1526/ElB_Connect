# backend/app/models/meter.py
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.connection import Base

class Meter(Base):
    __tablename__ = "meters"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    meter_serial_number = Column(String(40), unique=True, nullable=False, index=True)
    meter_type = Column(String(40), nullable=False, default="Smart Digital")  # Smart Digital, Prepaid, Solar Net-Meter, Bi-directional
    phase = Column(String(20), nullable=False, default="Single Phase")
    initial_reading_kwh = Column(Float, nullable=False, default=0.0)
    current_reading_kwh = Column(Float, nullable=False, default=0.0)
    substation_name = Column(String(100), nullable=False, default="Central Substation 33/11kV")
    feeder_line = Column(String(100), nullable=False, default="Feeder-11kV-01")
    status = Column(String(20), nullable=False, default="Active")  # Active, Suspended, Disconnected
    
    installation_date = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    application = relationship("Application", back_populates="meter")
    grievances = relationship("Grievance", back_populates="meter")

    def __repr__(self):
        return f"<Meter(serial='{self.meter_serial_number}', status='{self.status}')>"
