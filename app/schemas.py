from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# -------- USER & AUTH --------
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=5)
    role: Optional[str] = "patient" # Default to patient if not specified

class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True # Tells Pydantic to read data even if it's an ORM object

class Token(BaseModel):
    access_token: str
    token_type: str

# -------- DOCTOR --------
class DoctorCreate(BaseModel):
    name: str
    specialization: str

class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str

    class Config:
        from_attributes = True

# -------- SCHEDULE --------
class ScheduleCreate(BaseModel):
    day_of_week: str = Field(..., example="Monday")
    start_time: str = Field(..., example="09:00")
    end_time: str = Field(..., example="17:00")

class ScheduleResponse(ScheduleCreate):
    id: int
    doctor_id: int

    class Config:
        from_attributes = True

# -------- APPOINTMENT --------
class AppointmentCreate(BaseModel):
    doctor_id: int
    appointment_time: datetime # Format: 2026-05-10T10:00:00

class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    appointment_time: datetime
    status: str

    class Config:
        from_attributes = True

# --- SEARCH ---
class DoctorSearchResponse(DoctorResponse):
    pass