# backend/app/schemas/grievance.py
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from backend.app.schemas.consumer import ConsumerResponse

class GrievanceBase(BaseModel):
    category: str = Field(..., description="Power Outage, Voltage Fluctuation, Meter Defect, Hazardous Sparking, Billing Inquiry")
    priority: str = Field("Medium", description="Low, Medium, High, Critical")
    description: str = Field(..., min_length=5, description="Details of grievance/fault")
    assigned_lineman: Optional[str] = Field(None, description="Assigned lineman or maintenance crew")
    resolution_notes: Optional[str] = Field(None, description="Resolution notes")

class GrievanceCreate(GrievanceBase):
    consumer_id: int
    meter_id: Optional[int] = None

class GrievanceCreatePublic(BaseModel):
    """Consumer self-service complaint registration."""
    full_name: str = Field(..., min_length=2)
    phone: str = Field(..., min_length=10, max_length=15)
    email: Optional[str] = None
    address: str = Field(..., min_length=5)
    category: str = Field(...)
    priority: str = Field("Medium")
    description: str = Field(..., min_length=5)
    meter_serial_number: Optional[str] = None

class GrievanceUpdate(BaseModel):
    category: Optional[str] = None
    priority: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None  # Registered, Assigned, In_Progress, Resolved, Closed
    assigned_lineman: Optional[str] = None
    resolution_notes: Optional[str] = None

class GrievanceResponse(GrievanceBase):
    id: int
    grievance_number: str
    consumer_id: int
    meter_id: Optional[int] = None
    status: str
    resolved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    consumer: Optional[ConsumerResponse] = None

    model_config = ConfigDict(from_attributes=True)
