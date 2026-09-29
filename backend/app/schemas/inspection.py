# backend/app/schemas/inspection.py
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class InspectionBase(BaseModel):
    inspector_name: str = Field(..., min_length=2, max_length=100, description="Assigned Junior Engineer / Officer")
    feasibility_status: str = Field("Feasible", description="Feasible, Transformer_Upgrade_Required, Pole_Extension_Needed, Non_Feasible")
    pole_distance_meters: float = Field(25.0, ge=1.0, le=500.0, description="Distance from nearest distribution pole in meters")
    transformer_id: str = Field("TR-MAIN-01", description="Transformer unit ID")
    transformer_capacity_kva: float = Field(100.0, ge=10.0, description="Transformer rated kVA capacity")
    meter_box_ready: bool = Field(True, description="Premises meter board readiness")
    remarks: Optional[str] = Field(None, description="Inspector technical notes")
    scheduled_date: Optional[datetime] = Field(None, description="Date for field visit")

class InspectionCreate(InspectionBase):
    application_id: int

class InspectionUpdate(BaseModel):
    inspector_name: Optional[str] = None
    feasibility_status: Optional[str] = None
    pole_distance_meters: Optional[float] = Field(None, ge=1.0, le=500.0)
    transformer_id: Optional[str] = None
    transformer_capacity_kva: Optional[float] = None
    meter_box_ready: Optional[bool] = None
    remarks: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class InspectionResponse(InspectionBase):
    id: int
    application_id: int
    completed_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
