# backend/app/models/audit_log.py
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.connection import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, index=True)
    
    action = Column(String(60), nullable=False)  # APPLICATION_SUBMITTED, STATUS_UPDATE, INSPECTION_COMPLETED, etc.
    performed_by = Column(String(100), nullable=False, default="System")
    old_status = Column(String(40), nullable=True)
    new_status = Column(String(40), nullable=False)
    notes = Column(Text, nullable=True)
    
    timestamp = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    application = relationship("Application", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog(app_id={self.application_id}, action='{self.action}', to='{self.new_status}')>"
