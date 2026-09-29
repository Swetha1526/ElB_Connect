# backend/app/schemas/__init__.py
from backend.app.schemas.consumer import ConsumerBase, ConsumerCreate, ConsumerUpdate, ConsumerResponse
from backend.app.schemas.inspection import InspectionBase, InspectionCreate, InspectionUpdate, InspectionResponse
from backend.app.schemas.meter import MeterBase, MeterCreate, MeterUpdate, MeterResponse
from backend.app.schemas.grievance import GrievanceBase, GrievanceCreate, GrievanceCreatePublic, GrievanceUpdate, GrievanceResponse
from backend.app.schemas.application import (
    ApplicationBase,
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    PaginatedApplicationResponse,
    AuditLogResponse
)
from backend.app.schemas.stats import DashboardStatsResponse, CategoryCount, StatusCount, SubstationStat

__all__ = [
    "ConsumerBase",
    "ConsumerCreate",
    "ConsumerUpdate",
    "ConsumerResponse",
    "InspectionBase",
    "InspectionCreate",
    "InspectionUpdate",
    "InspectionResponse",
    "MeterBase",
    "MeterCreate",
    "MeterUpdate",
    "MeterResponse",
    "GrievanceBase",
    "GrievanceCreate",
    "GrievanceCreatePublic",
    "GrievanceUpdate",
    "GrievanceResponse",
    "ApplicationBase",
    "ApplicationCreate",
    "ApplicationUpdate",
    "ApplicationResponse",
    "PaginatedApplicationResponse",
    "AuditLogResponse",
    "DashboardStatsResponse",
    "CategoryCount",
    "StatusCount",
    "SubstationStat"
]
