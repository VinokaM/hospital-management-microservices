# billing-service/models.py
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "Pending"
    PAID = "Paid"
    PARTIALLY_PAID = "Partially Paid"
    OVERDUE = "Overdue"
    CANCELLED = "Cancelled"
    REFUNDED = "Refunded"

class PaymentMethod(str, Enum):
    CASH = "Cash"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    INSURANCE = "Insurance"
    BANK_TRANSFER = "Bank Transfer"
    ONLINE = "Online Payment"

class ServiceType(str, Enum):
    CONSULTATION = "Consultation"
    SURGERY = "Surgery"
    LAB_TEST = "Lab Test"
    PHARMACY = "Pharmacy"
    ROOM_CHARGE = "Room Charge"
    NURSING = "Nursing Care"
    RADIOLOGY = "Radiology"
    PHYSIOTHERAPY = "Physiotherapy"

# ─── Bill Item Model ───────────────────────────────────────────────────────────
class BillItem(BaseModel):
    service_type: ServiceType
    description: str
    quantity: int
    unit_price: float
    total_price: float

# ─── Bill Model ────────────────────────────────────────────────────────────────
class Bill(BaseModel):
    id: int
    patient_id: int
    patient_name: str
    doctor_id: int
    doctor_name: str
    appointment_id: int
    bill_date: str
    due_date: str
    items: List[BillItem]
    subtotal: float
    discount: float
    tax: float
    total_amount: float
    paid_amount: float
    balance: float
    payment_status: PaymentStatus
    payment_method: Optional[PaymentMethod] = None
    notes: Optional[str] = None

class BillCreate(BaseModel):
    patient_id: int
    patient_name: str
    doctor_id: int
    doctor_name: str
    appointment_id: int
    bill_date: str
    due_date: str
    items: List[BillItem]
    subtotal: float
    discount: float
    tax: float
    total_amount: float
    paid_amount: float
    balance: float
    payment_status: PaymentStatus
    payment_method: Optional[PaymentMethod] = None
    notes: Optional[str] = None

class BillUpdate(BaseModel):
    patient_id: Optional[int] = None
    patient_name: Optional[str] = None
    doctor_id: Optional[int] = None
    doctor_name: Optional[str] = None
    appointment_id: Optional[int] = None
    bill_date: Optional[str] = None
    due_date: Optional[str] = None
    items: Optional[List[BillItem]] = None
    subtotal: Optional[float] = None
    discount: Optional[float] = None
    tax: Optional[float] = None
    total_amount: Optional[float] = None
    paid_amount: Optional[float] = None
    balance: Optional[float] = None
    payment_status: Optional[PaymentStatus] = None
    payment_method: Optional[PaymentMethod] = None
    notes: Optional[str] = None

# ─── Payment Model ─────────────────────────────────────────────────────────────
class Payment(BaseModel):
    id: int
    bill_id: int
    patient_id: int
    patient_name: str
    amount_paid: float
    payment_method: PaymentMethod
    payment_date: str
    transaction_id: str
    notes: Optional[str] = None

class PaymentCreate(BaseModel):
    bill_id: int
    patient_id: int
    patient_name: str
    amount_paid: float
    payment_method: PaymentMethod
    payment_date: str
    transaction_id: str
    notes: Optional[str] = None
