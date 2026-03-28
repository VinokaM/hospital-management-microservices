# appointment-service/models.py
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class AppointmentStatus(str, Enum):
    SCHEDULED = "Scheduled"
    CONFIRMED = "Confirmed"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    NO_SHOW = "No Show"

class AppointmentType(str, Enum):
    GENERAL_CHECKUP = "General Checkup"
    FOLLOW_UP = "Follow Up"
    EMERGENCY = "Emergency"
    CONSULTATION = "Consultation"
    SURGERY = "Surgery"
    LAB_TEST = "Lab Test"

class Appointment(BaseModel):
    id: int
    patient_id: int
    patient_name: str
    doctor_id: int
    doctor_name: str
    appointment_date: str
    appointment_time: str
    appointment_type: AppointmentType
    status: AppointmentStatus
    reason: str
    notes: Optional[str] = None

class AppointmentCreate(BaseModel):
    patient_id: int
    patient_name: str
    doctor_id: int
    doctor_name: str
    appointment_date: str
    appointment_time: str
    appointment_type: AppointmentType
    status: AppointmentStatus
    reason: str
    notes: Optional[str] = None

class AppointmentUpdate(BaseModel):
    patient_id: Optional[int] = None
    patient_name: Optional[str] = None
    doctor_id: Optional[int] = None
    doctor_name: Optional[str] = None
    appointment_date: Optional[str] = None
    appointment_time: Optional[str] = None
    appointment_type: Optional[AppointmentType] = None
    status: Optional[AppointmentStatus] = None
    reason: Optional[str] = None
    notes: Optional[str] = None
