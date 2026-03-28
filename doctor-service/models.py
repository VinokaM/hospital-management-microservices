# doctor-service/models.py
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class Specialization(str, Enum):
    CARDIOLOGY = "Cardiology"
    NEUROLOGY = "Neurology"
    ORTHOPEDICS = "Orthopedics"
    PEDIATRICS = "Pediatrics"
    DERMATOLOGY = "Dermatology"
    GENERAL = "General Medicine"
    SURGERY = "Surgery"
    PSYCHIATRY = "Psychiatry"
    RADIOLOGY = "Radiology"
    ONCOLOGY = "Oncology"

class Availability(str, Enum):
    AVAILABLE = "Available"
    UNAVAILABLE = "Unavailable"
    ON_LEAVE = "On Leave"

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class Doctor(BaseModel):
    id: int
    first_name: str
    last_name: str
    age: int
    gender: Gender
    specialization: Specialization
    phone: str
    email: str
    qualification: str
    experience_years: int
    availability: Availability
    consultation_fee: float

class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    gender: Gender
    specialization: Specialization
    phone: str
    email: str
    qualification: str
    experience_years: int
    availability: Availability
    consultation_fee: float

class DoctorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    specialization: Optional[Specialization] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    qualification: Optional[str] = None
    experience_years: Optional[int] = None
    availability: Optional[Availability] = None
    consultation_fee: Optional[float] = None
