# patient-service/models.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class BloodGroup(str, Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class Patient(BaseModel):
    id: int
    first_name: str
    last_name: str
    age: int
    gender: Gender
    blood_group: BloodGroup
    phone: str
    email: str
    address: str
    medical_history: Optional[str] = None

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    gender: Gender
    blood_group: BloodGroup
    phone: str
    email: str
    address: str
    medical_history: Optional[str] = None

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    blood_group: Optional[BloodGroup] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    medical_history: Optional[str] = None
