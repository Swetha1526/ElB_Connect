# backend/app/models/__init__.py
from backend.app.models.consumer import Consumer
from backend.app.models.application import Application
from backend.app.models.inspection import Inspection
from backend.app.models.meter import Meter
from backend.app.models.grievance import Grievance
from backend.app.models.audit_log import AuditLog

__all__ = [
    "Consumer",
    "Application",
    "Inspection",
    "Meter",
    "Grievance",
    "AuditLog"
]
