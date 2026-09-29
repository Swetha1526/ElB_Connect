# backend/app/schemas/application.py
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from backend.app.schemas.consumer import ConsumerCreate, ConsumerResponse
from backend.app.schemas.inspection import InspectionResponse
from backend.app.schemas.meter import MeterResponse

class AuditLogResponse(BaseModel):
    id: int
    application_id: int
    action: str
    performed_by: str
    old_status: Optional[str] = None
    new_status: str
    notes: Optional[str] = None
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class ApplicationBase(BaseModel):
    connection_type: str = Field("New Connection", description="New Connection, Load Enhancement, Tariff Change")
    category: str = Field(..., description="Domestic, Commercial, Industrial, Agricultural")
    requested_load_kw: float = Field(..., gt=0, le=500.0, description="Load in kW (0.5 to 500.0)")
    phase: str = Field("Single Phase", description="Single Phase, Three Phase")
    premises_type: str = Field("Owned", description="Owned, Rented, Leased")
    substation_name: str = Field("Central Substation 33/11kV", description="Assigned distribution substation")
    remarks: Optional[str] = Field(None, description="Additional consumer notes or premises description")

class ApplicationCreate(ApplicationBase):
    """Create application with either consumer details or existing consumer_id."""
    consumer_id: Optional[int] = None
    consumer: Optional[ConsumerCreate] = None

class ApplicationUpdate(BaseModel):
    connection_type: Optional[str] = None
    category: Optional[str] = None
    requested_load_kw: Optional[float] = Field(None, gt=0, le=500.0)
    phase: Optional[str] = None
    premises_type: Optional[str] = None
    substation_name: Optional[str] = None
    status: Optional[str] = None  # Submitted, Document_Verified, Field_Inspection_Scheduled, Inspection_Approved, Payment_Pending, Meter_Assigned_Active, Rejected
    sanctioned_load_kw: Optional[float] = Field(None, ge=0)
    quotation_amount: Optional[float] = Field(None, ge=0)
    payment_status: Optional[str] = None  # Pending, Paid, Waived
    remarks: Optional[str] = None
    action_note: Optional[str] = Field(None, description="Audit note describing reasons for modification")
    performed_by: Optional[str] = Field("Officer", description="Officer name for audit logging")

class ApplicationResponse(ApplicationBase):
    id: int
    application_number: str
    consumer_id: int
    status: str
    sanctioned_load_kw: Optional[float] = None
    quotation_amount: float
    payment_status: str
    created_at: datetime
    updated_at: datetime
    
    consumer: Optional[ConsumerResponse] = None
    inspection: Optional[InspectionResponse] = None
    meter: Optional[MeterResponse] = None
    audit_logs: Optional[List[AuditLogResponse]] = []

    model_config = ConfigDict(from_attributes=True)

class PaginatedApplicationResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[ApplicationResponse]
