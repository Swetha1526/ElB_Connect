# backend/app/schemas/consumer.py
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ConsumerBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120, description="Applicant full name")
    email: str = Field(..., min_length=5, max_length=120, description="Valid contact email address")
    phone: str = Field(..., min_length=10, max_length=15, description="10-15 digit phone number")
    national_id: str = Field(..., min_length=4, max_length=20, description="Aadhaar / National ID / PAN")
    address: str = Field(..., min_length=5, description="Complete street address")
    city: str = Field(..., min_length=2, max_length=80, description="City / Town")
    pincode: str = Field(..., min_length=5, max_length=10, description="Postal PIN code")
    consumer_category: str = Field("Domestic", description="Domestic, Commercial, Industrial, Agricultural")

class ConsumerCreate(ConsumerBase):
    pass

class ConsumerUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=120)
    email: Optional[str] = Field(None, min_length=5, max_length=120)
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    address: Optional[str] = Field(None, min_length=5)
    city: Optional[str] = None
    pincode: Optional[str] = None
    consumer_category: Optional[str] = None

class ConsumerResponse(ConsumerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
