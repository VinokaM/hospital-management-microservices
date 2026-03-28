# pharmacy-service/models.py
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class MedicineCategory(str, Enum):
    ANTIBIOTIC = "Antibiotic"
    PAINKILLER = "Painkiller"
    ANTIVIRAL = "Antiviral"
    ANTIFUNGAL = "Antifungal"
    CARDIOVASCULAR = "Cardiovascular"
    DIABETES = "Diabetes"
    VITAMIN = "Vitamin & Supplement"
    ANTIALLERGIC = "Antiallergic"
    PSYCHIATRIC = "Psychiatric"
    GASTROINTESTINAL = "Gastrointestinal"

class MedicineStatus(str, Enum):
    IN_STOCK = "In Stock"
    LOW_STOCK = "Low Stock"
    OUT_OF_STOCK = "Out of Stock"
    DISCONTINUED = "Discontinued"

class PrescriptionStatus(str, Enum):
    PENDING = "Pending"
    DISPENSED = "Dispensed"
    CANCELLED = "Cancelled"
    ON_HOLD = "On Hold"

# ─── Medicine Model ────────────────────────────────────────────────────────────
class Medicine(BaseModel):
    id: int
    name: str
    generic_name: str
    category: MedicineCategory
    manufacturer: str
    unit_price: float
    stock_quantity: int
    status: MedicineStatus
    description: Optional[str] = None
    expiry_date: str

class MedicineCreate(BaseModel):
    name: str
    generic_name: str
    category: MedicineCategory
    manufacturer: str
    unit_price: float
    stock_quantity: int
    status: MedicineStatus
    description: Optional[str] = None
    expiry_date: str

class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    generic_name: Optional[str] = None
    category: Optional[MedicineCategory] = None
    manufacturer: Optional[str] = None
    unit_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    status: Optional[MedicineStatus] = None
    description: Optional[str] = None
    expiry_date: Optional[str] = None

# ─── Prescription Model ────────────────────────────────────────────────────────
class Prescription(BaseModel):
    id: int
    patient_id: int
    patient_name: str
    doctor_id: int
    doctor_name: str
    medicine_id: int
    medicine_name: str
    dosage: str
    duration_days: int
    quantity: int
    total_price: float
    prescribed_date: str
    status: PrescriptionStatus
    notes: Optional[str] = None

class PrescriptionCreate(BaseModel):
    patient_id: int
    patient_name: str
    doctor_id: int
    doctor_name: str
    medicine_id: int
    medicine_name: str
    dosage: str
    duration_days: int
    quantity: int
    total_price: float
    prescribed_date: str
    status: PrescriptionStatus
    notes: Optional[str] = None

class PrescriptionUpdate(BaseModel):
    patient_id: Optional[int] = None
    patient_name: Optional[str] = None
    doctor_id: Optional[int] = None
    doctor_name: Optional[str] = None
    medicine_id: Optional[int] = None
    medicine_name: Optional[str] = None
    dosage: Optional[str] = None
    duration_days: Optional[int] = None
    quantity: Optional[int] = None
    total_price: Optional[float] = None
    prescribed_date: Optional[str] = None
    status: Optional[PrescriptionStatus] = None
    notes: Optional[str] = None
