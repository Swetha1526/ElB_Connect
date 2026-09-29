# backend/app/schemas/meter.py
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class MeterBase(BaseModel):
    meter_serial_number: Optional[str] = Field(None, description="Hardware serial number (auto-generated if omitted)")
    meter_type: str = Field("Smart Digital", description="Smart Digital, Prepaid, Solar Net-Meter, Bi-directional")
    phase: str = Field("Single Phase", description="Single Phase, Three Phase")
    initial_reading_kwh: float = Field(0.0, ge=0.0, description="Baseline reading in kWh")
    current_reading_kwh: float = Field(0.0, ge=0.0, description="Current recorded reading in kWh")
    substation_name: str = Field("Central Substation 33/11kV", description="Assigned substation")
    feeder_line: str = Field("Feeder-11kV-01", description="11kV feeder line name")
    status: str = Field("Active", description="Active, Suspended, Disconnected")

class MeterCreate(MeterBase):
    application_id: int

class MeterUpdate(BaseModel):
    meter_type: Optional[str] = None
    current_reading_kwh: Optional[float] = Field(None, ge=0.0)
    substation_name: Optional[str] = None
    feeder_line: Optional[str] = None
    status: Optional[str] = None

class MeterResponse(MeterBase):
    id: int
    application_id: int
    meter_serial_number: str
    installation_date: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
