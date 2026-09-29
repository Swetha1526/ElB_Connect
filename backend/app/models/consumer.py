# backend/app/models/consumer.py
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from backend.app.database.connection import Base

class Consumer(Base):
    __tablename__ = "consumers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, index=True)
    phone = Column(String(15), nullable=False, index=True)
    national_id = Column(String(20), nullable=False)
    address = Column(Text, nullable=False)
    city = Column(String(80), nullable=False)
    pincode = Column(String(10), nullable=False)
    consumer_category = Column(String(30), nullable=False, default="Domestic")
    
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    applications = relationship("Application", back_populates="consumer", cascade="all, delete-orphan")
    grievances = relationship("Grievance", back_populates="consumer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Consumer(id={self.id}, name='{self.full_name}', phone='{self.phone}')>"
