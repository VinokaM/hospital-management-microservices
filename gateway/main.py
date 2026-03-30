# gateway/main.py
from fastapi import FastAPI, HTTPException, Request, Depends, Query, Response
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from typing import Any, Optional, List
from enum import Enum
import httpx
import jwt
import logging
import time
from datetime import datetime, timedelta

# ─── Logging Setup ─────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("hospital-gateway")

# ─── App Setup ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Hospital Management - API Gateway",
    description="Central API Gateway for the Hospital Management System.",
    version="1.0.0"
)

# ─── JWT Config ────────────────────────────────────────────────────────────────
SECRET_KEY = "hospital-secret-key-2026"
ALGORITHM = "HS256"
security = HTTPBearer(auto_error=False)

# ─── Microservice URLs ─────────────────────────────────────────────────────────
SERVICES = {
    "patient":     "http://localhost:8001",
    "doctor":      "http://localhost:8002",
    "appointment": "http://localhost:8003",
    "pharmacy":    "http://localhost:8004",
    "billing":     "http://localhost:8005",
}

# ─── Custom Swagger ────────────────────────────────────────────────────────────
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Hospital Management - API Gateway",
        version="1.0.0",
        description="Central API Gateway for the Hospital Management System.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ==============================================================================
#  REQUEST BODY MODELS FOR SWAGGER UI
# ==============================================================================

# ─── Patient Models ────────────────────────────────────────────────────────────
class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class BloodGroupEnum(str, Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    gender: GenderEnum
    blood_group: BloodGroupEnum
    phone: str
    email: str
    address: str
    medical_history: Optional[str] = None

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[GenderEnum] = None
    blood_group: Optional[BloodGroupEnum] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    medical_history: Optional[str] = None

# ─── Doctor Models ─────────────────────────────────────────────────────────────
class SpecializationEnum(str, Enum):
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

class AvailabilityEnum(str, Enum):
    AVAILABLE = "Available"
    UNAVAILABLE = "Unavailable"
    ON_LEAVE = "On Leave"

class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    gender: GenderEnum
    specialization: SpecializationEnum
    phone: str
    email: str
    qualification: str
    experience_years: int
    availability: AvailabilityEnum
    consultation_fee: float

class DoctorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[GenderEnum] = None
    specialization: Optional[SpecializationEnum] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    qualification: Optional[str] = None
    experience_years: Optional[int] = None
    availability: Optional[AvailabilityEnum] = None
    consultation_fee: Optional[float] = None

# ─── Appointment Models ────────────────────────────────────────────────────────
class AppointmentStatusEnum(str, Enum):
    SCHEDULED = "Scheduled"
    CONFIRMED = "Confirmed"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    NO_SHOW = "No Show"

class AppointmentTypeEnum(str, Enum):
    GENERAL_CHECKUP = "General Checkup"
    FOLLOW_UP = "Follow Up"
    EMERGENCY = "Emergency"
    CONSULTATION = "Consultation"
    SURGERY = "Surgery"
    LAB_TEST = "Lab Test"

class AppointmentCreate(BaseModel):
    patient_id: int
    patient_name: str
    doctor_id: int
    doctor_name: str
    appointment_date: str
    appointment_time: str
    appointment_type: AppointmentTypeEnum
    status: AppointmentStatusEnum
    reason: str
    notes: Optional[str] = None

class AppointmentUpdate(BaseModel):
    patient_id: Optional[int] = None
    patient_name: Optional[str] = None
    doctor_id: Optional[int] = None
    doctor_name: Optional[str] = None
    appointment_date: Optional[str] = None
    appointment_time: Optional[str] = None
    appointment_type: Optional[AppointmentTypeEnum] = None
    status: Optional[AppointmentStatusEnum] = None
    reason: Optional[str] = None
    notes: Optional[str] = None

# ─── Pharmacy Models ───────────────────────────────────────────────────────────
class MedicineCategoryEnum(str, Enum):
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

class MedicineStatusEnum(str, Enum):
    IN_STOCK = "In Stock"
    LOW_STOCK = "Low Stock"
    OUT_OF_STOCK = "Out of Stock"
    DISCONTINUED = "Discontinued"

class PrescriptionStatusEnum(str, Enum):
    PENDING = "Pending"
    DISPENSED = "Dispensed"
    CANCELLED = "Cancelled"
    ON_HOLD = "On Hold"

class MedicineCreate(BaseModel):
    name: str
    generic_name: str
    category: MedicineCategoryEnum
    manufacturer: str
    unit_price: float
    stock_quantity: int
    status: MedicineStatusEnum
    description: Optional[str] = None
    expiry_date: str

class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    generic_name: Optional[str] = None
    category: Optional[MedicineCategoryEnum] = None
    manufacturer: Optional[str] = None
    unit_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    status: Optional[MedicineStatusEnum] = None
    description: Optional[str] = None
    expiry_date: Optional[str] = None

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
    status: PrescriptionStatusEnum
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
    status: Optional[PrescriptionStatusEnum] = None
    notes: Optional[str] = None

# ─── Billing Models ────────────────────────────────────────────────────────────
class PaymentStatusEnum(str, Enum):
    PENDING = "Pending"
    PAID = "Paid"
    PARTIALLY_PAID = "Partially Paid"
    OVERDUE = "Overdue"
    CANCELLED = "Cancelled"
    REFUNDED = "Refunded"

class PaymentMethodEnum(str, Enum):
    CASH = "Cash"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    INSURANCE = "Insurance"
    BANK_TRANSFER = "Bank Transfer"
    ONLINE = "Online Payment"

class ServiceTypeEnum(str, Enum):
    CONSULTATION = "Consultation"
    SURGERY = "Surgery"
    LAB_TEST = "Lab Test"
    PHARMACY = "Pharmacy"
    ROOM_CHARGE = "Room Charge"
    NURSING = "Nursing Care"
    RADIOLOGY = "Radiology"
    PHYSIOTHERAPY = "Physiotherapy"

class BillItem(BaseModel):
    service_type: ServiceTypeEnum
    description: str
    quantity: int
    unit_price: float
    total_price: float

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
    payment_status: PaymentStatusEnum
    payment_method: Optional[PaymentMethodEnum] = None
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
    payment_status: Optional[PaymentStatusEnum] = None
    payment_method: Optional[PaymentMethodEnum] = None
    notes: Optional[str] = None

class PaymentCreate(BaseModel):
    bill_id: int
    patient_id: int
    patient_name: str
    amount_paid: float
    payment_method: PaymentMethodEnum
    payment_date: str
    transaction_id: str
    notes: Optional[str] = None

# ==============================================================================
#  JWT + MIDDLEWARE
# ==============================================================================

def create_token(username: str) -> str:
    payload = {"sub": username, "exp": datetime.utcnow() + timedelta(hours=2)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials is None:
        raise HTTPException(status_code=401, detail="No token provided. Please login at POST /auth/login.")
    token = credentials.credentials
    if token.lower().startswith("bearer "):
        token = token[7:]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired. Please login again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token. Please login again.")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"-> {request.method} {request.url.path}")
    response = await call_next(request)
    duration = round((time.time() - start_time) * 1000, 2)
    logger.info(f"<- {response.status_code} | {duration}ms")
    return response

async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail={"error": "Service not found", "service": service})
    url = f"{SERVICES[service]}{path}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "PATCH":
                response = await client.patch(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")

            if response.status_code in (204, 205) or not response.text:
                return Response(status_code=response.status_code)

            if response.status_code == 404:
                raise HTTPException(status_code=404, detail={"error": "Resource not found", "path": path})
            if response.status_code == 422:
                raise HTTPException(status_code=422, detail={"error": "Validation error", "details": response.json()})
            if response.status_code >= 500:
                raise HTTPException(status_code=502, detail={"error": "Upstream service error", "service": service})

            return JSONResponse(content=response.json() if response.text else None, status_code=response.status_code)

        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail={"error": "Service unreachable", "service": service, "hint": f"Make sure {service} service is running"})
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail={"error": "Service timed out", "service": service})

# ==============================================================================
#  AUTH
# ==============================================================================

@app.post("/auth/login", tags=["Authentication"])
def login(username: str, password: str):
    """Login - use username=admin and password=hospital2026"""
    if username == "admin" and password == "hospital2026":
        token = create_token(username)
        return {"access_token": token, "token_type": "bearer", "expires_in": "2 hours"}
    raise HTTPException(status_code=401, detail="Invalid credentials. Use admin / hospital2026")

@app.get("/", tags=["Gateway Info"])
def read_root():
    return {"system": "Hospital Management System", "gateway": "running", "port": 8000, "services": list(SERVICES.keys())}

# ==============================================================================
#  PATIENT SERVICE  ->  Port 8001
# ==============================================================================

@app.get("/gateway/patients", tags=["Patient Service"])
async def get_all_patients(token: dict = Depends(verify_token)):
    """Get all patients"""
    return await forward_request("patient", "/api/patients", "GET")

@app.get("/gateway/patients/blood-group/{blood_group}", tags=["Patient Service"])
async def get_patients_by_blood_group(blood_group: str, token: dict = Depends(verify_token)):
    """Get patients by blood group"""
    return await forward_request("patient", f"/api/patients/blood-group/{blood_group}", "GET")

@app.get("/gateway/patients/gender/{gender}", tags=["Patient Service"])
async def get_patients_by_gender(gender: str, token: dict = Depends(verify_token)):
    """Get patients by gender"""
    return await forward_request("patient", f"/api/patients/gender/{gender}", "GET")

@app.get("/gateway/patients/{patient_id}", tags=["Patient Service"])
async def get_patient(patient_id: int, token: dict = Depends(verify_token)):
    """Get patient by ID"""
    return await forward_request("patient", f"/api/patients/{patient_id}", "GET")

@app.post("/gateway/patients", tags=["Patient Service"])
async def create_patient(patient: PatientCreate, token: dict = Depends(verify_token)):
    """Add a new patient"""
    return await forward_request("patient", "/api/patients", "POST", json=patient.dict())

@app.put("/gateway/patients/{patient_id}", tags=["Patient Service"])
async def update_patient(patient_id: int, patient: PatientUpdate, token: dict = Depends(verify_token)):
    """Update a patient"""
    return await forward_request("patient", f"/api/patients/{patient_id}", "PUT", json=patient.dict())

@app.delete("/gateway/patients/{patient_id}", tags=["Patient Service"])
async def delete_patient(patient_id: int, token: dict = Depends(verify_token)):
    """Delete a patient"""
    return await forward_request("patient", f"/api/patients/{patient_id}", "DELETE")

# ==============================================================================
#  DOCTOR SERVICE  ->  Port 8002
# ==============================================================================

@app.get("/gateway/doctors", tags=["Doctor Service"])
async def get_all_doctors(token: dict = Depends(verify_token)):
    """Get all doctors"""
    return await forward_request("doctor", "/api/doctors", "GET")

@app.get("/gateway/doctors/status/available", tags=["Doctor Service"])
async def get_available_doctors(token: dict = Depends(verify_token)):
    """Get all available doctors"""
    return await forward_request("doctor", "/api/doctors/status/available", "GET")

@app.get("/gateway/doctors/specialization/{specialization}", tags=["Doctor Service"])
async def get_doctors_by_specialization(specialization: str, token: dict = Depends(verify_token)):
    """Get doctors by specialization"""
    return await forward_request("doctor", f"/api/doctors/specialization/{specialization}", "GET")

@app.get("/gateway/doctors/availability/{availability}", tags=["Doctor Service"])
async def get_doctors_by_availability(availability: str, token: dict = Depends(verify_token)):
    """Get doctors by availability"""
    return await forward_request("doctor", f"/api/doctors/availability/{availability}", "GET")

@app.get("/gateway/doctors/{doctor_id}", tags=["Doctor Service"])
async def get_doctor(doctor_id: int, token: dict = Depends(verify_token)):
    """Get doctor by ID"""
    return await forward_request("doctor", f"/api/doctors/{doctor_id}", "GET")

@app.post("/gateway/doctors", tags=["Doctor Service"])
async def create_doctor(doctor: DoctorCreate, token: dict = Depends(verify_token)):
    """Add a new doctor"""
    return await forward_request("doctor", "/api/doctors", "POST", json=doctor.dict())

@app.put("/gateway/doctors/{doctor_id}", tags=["Doctor Service"])
async def update_doctor(doctor_id: int, doctor: DoctorUpdate, token: dict = Depends(verify_token)):
    """Update a doctor"""
    return await forward_request("doctor", f"/api/doctors/{doctor_id}", "PUT", json=doctor.dict())

@app.delete("/gateway/doctors/{doctor_id}", tags=["Doctor Service"])
async def delete_doctor(doctor_id: int, token: dict = Depends(verify_token)):
    """Delete a doctor"""
    return await forward_request("doctor", f"/api/doctors/{doctor_id}", "DELETE")

# ==============================================================================
#  APPOINTMENT SERVICE  ->  Port 8003
# ==============================================================================

@app.get("/gateway/appointments", tags=["Appointment Service"])
async def get_all_appointments(token: dict = Depends(verify_token)):
    """Get all appointments"""
    return await forward_request("appointment", "/api/appointments", "GET")

@app.get("/gateway/appointments/patient/{patient_id}", tags=["Appointment Service"])
async def get_appointments_by_patient(patient_id: int, token: dict = Depends(verify_token)):
    """Get appointments by patient"""
    return await forward_request("appointment", f"/api/appointments/patient/{patient_id}", "GET")

@app.get("/gateway/appointments/doctor/{doctor_id}", tags=["Appointment Service"])
async def get_appointments_by_doctor(doctor_id: int, token: dict = Depends(verify_token)):
    """Get appointments by doctor"""
    return await forward_request("appointment", f"/api/appointments/doctor/{doctor_id}", "GET")

@app.get("/gateway/appointments/status/{status}", tags=["Appointment Service"])
async def get_appointments_by_status(status: str, token: dict = Depends(verify_token)):
    """Get appointments by status"""
    return await forward_request("appointment", f"/api/appointments/status/{status}", "GET")

@app.get("/gateway/appointments/date/{date}", tags=["Appointment Service"])
async def get_appointments_by_date(date: str, token: dict = Depends(verify_token)):
    """Get appointments by date (YYYY-MM-DD)"""
    return await forward_request("appointment", f"/api/appointments/date/{date}", "GET")

@app.get("/gateway/appointments/type/{appointment_type}", tags=["Appointment Service"])
async def get_appointments_by_type(appointment_type: str, token: dict = Depends(verify_token)):
    """Get appointments by type"""
    return await forward_request("appointment", f"/api/appointments/type/{appointment_type}", "GET")

@app.get("/gateway/appointments/{appointment_id}", tags=["Appointment Service"])
async def get_appointment(appointment_id: int, token: dict = Depends(verify_token)):
    """Get appointment by ID"""
    return await forward_request("appointment", f"/api/appointments/{appointment_id}", "GET")

@app.post("/gateway/appointments", tags=["Appointment Service"])
async def create_appointment(appointment: AppointmentCreate, token: dict = Depends(verify_token)):
    """Schedule a new appointment"""
    return await forward_request("appointment", "/api/appointments", "POST", json=appointment.dict())

@app.put("/gateway/appointments/{appointment_id}", tags=["Appointment Service"])
async def update_appointment(appointment_id: int, appointment: AppointmentUpdate, token: dict = Depends(verify_token)):
    """Update an appointment"""
    return await forward_request("appointment", f"/api/appointments/{appointment_id}", "PUT", json=appointment.dict())

@app.patch("/gateway/appointments/{appointment_id}/cancel", tags=["Appointment Service"])
async def cancel_appointment(appointment_id: int, token: dict = Depends(verify_token)):
    """Cancel an appointment"""
    return await forward_request("appointment", f"/api/appointments/{appointment_id}/cancel", "PATCH")

@app.delete("/gateway/appointments/{appointment_id}", tags=["Appointment Service"])
async def delete_appointment(appointment_id: int, token: dict = Depends(verify_token)):
    """Delete an appointment"""
    return await forward_request("appointment", f"/api/appointments/{appointment_id}", "DELETE")

# ==============================================================================
#  PHARMACY SERVICE  ->  Port 8004
# ==============================================================================

@app.get("/gateway/medicines", tags=["Pharmacy Service"])
async def get_all_medicines(token: dict = Depends(verify_token)):
    """Get all medicines"""
    return await forward_request("pharmacy", "/api/medicines", "GET")

@app.get("/gateway/medicines/available/instock", tags=["Pharmacy Service"])
async def get_instock_medicines(token: dict = Depends(verify_token)):
    """Get all in-stock medicines"""
    return await forward_request("pharmacy", "/api/medicines/available/instock", "GET")

@app.get("/gateway/medicines/category/{category}", tags=["Pharmacy Service"])
async def get_medicines_by_category(category: str, token: dict = Depends(verify_token)):
    """Get medicines by category"""
    return await forward_request("pharmacy", f"/api/medicines/category/{category}", "GET")

@app.get("/gateway/medicines/stock/{status}", tags=["Pharmacy Service"])
async def get_medicines_by_stock(status: str, token: dict = Depends(verify_token)):
    """Get medicines by stock status"""
    return await forward_request("pharmacy", f"/api/medicines/stock/{status}", "GET")

@app.get("/gateway/medicines/{medicine_id}", tags=["Pharmacy Service"])
async def get_medicine(medicine_id: int, token: dict = Depends(verify_token)):
    """Get medicine by ID"""
    return await forward_request("pharmacy", f"/api/medicines/{medicine_id}", "GET")

@app.post("/gateway/medicines", tags=["Pharmacy Service"])
async def create_medicine(medicine: MedicineCreate, token: dict = Depends(verify_token)):
    """Add a new medicine"""
    return await forward_request("pharmacy", "/api/medicines", "POST", json=medicine.dict())

@app.put("/gateway/medicines/{medicine_id}", tags=["Pharmacy Service"])
async def update_medicine(medicine_id: int, medicine: MedicineUpdate, token: dict = Depends(verify_token)):
    """Update a medicine"""
    return await forward_request("pharmacy", f"/api/medicines/{medicine_id}", "PUT", json=medicine.dict())

@app.delete("/gateway/medicines/{medicine_id}", tags=["Pharmacy Service"])
async def delete_medicine(medicine_id: int, token: dict = Depends(verify_token)):
    """Delete a medicine"""
    return await forward_request("pharmacy", f"/api/medicines/{medicine_id}", "DELETE")

@app.get("/gateway/prescriptions", tags=["Pharmacy Service"])
async def get_all_prescriptions(token: dict = Depends(verify_token)):
    """Get all prescriptions"""
    return await forward_request("pharmacy", "/api/prescriptions", "GET")

@app.get("/gateway/prescriptions/patient/{patient_id}", tags=["Pharmacy Service"])
async def get_prescriptions_by_patient(patient_id: int, token: dict = Depends(verify_token)):
    """Get prescriptions by patient"""
    return await forward_request("pharmacy", f"/api/prescriptions/patient/{patient_id}", "GET")

@app.get("/gateway/prescriptions/doctor/{doctor_id}", tags=["Pharmacy Service"])
async def get_prescriptions_by_doctor(doctor_id: int, token: dict = Depends(verify_token)):
    """Get prescriptions by doctor"""
    return await forward_request("pharmacy", f"/api/prescriptions/doctor/{doctor_id}", "GET")

@app.get("/gateway/prescriptions/status/{status}", tags=["Pharmacy Service"])
async def get_prescriptions_by_status(status: str, token: dict = Depends(verify_token)):
    """Get prescriptions by status"""
    return await forward_request("pharmacy", f"/api/prescriptions/status/{status}", "GET")

@app.get("/gateway/prescriptions/{prescription_id}", tags=["Pharmacy Service"])
async def get_prescription(prescription_id: int, token: dict = Depends(verify_token)):
    """Get prescription by ID"""
    return await forward_request("pharmacy", f"/api/prescriptions/{prescription_id}", "GET")

@app.post("/gateway/prescriptions", tags=["Pharmacy Service"])
async def create_prescription(prescription: PrescriptionCreate, token: dict = Depends(verify_token)):
    """Create a new prescription"""
    return await forward_request("pharmacy", "/api/prescriptions", "POST", json=prescription.dict())

@app.put("/gateway/prescriptions/{prescription_id}", tags=["Pharmacy Service"])
async def update_prescription(prescription_id: int, prescription: PrescriptionUpdate, token: dict = Depends(verify_token)):
    """Update a prescription"""
    return await forward_request("pharmacy", f"/api/prescriptions/{prescription_id}", "PUT", json=prescription.dict())

@app.patch("/gateway/prescriptions/{prescription_id}/dispense", tags=["Pharmacy Service"])
async def dispense_prescription(prescription_id: int, token: dict = Depends(verify_token)):
    """Mark prescription as dispensed"""
    return await forward_request("pharmacy", f"/api/prescriptions/{prescription_id}/dispense", "PATCH")

@app.delete("/gateway/prescriptions/{prescription_id}", tags=["Pharmacy Service"])
async def delete_prescription(prescription_id: int, token: dict = Depends(verify_token)):
    """Delete a prescription"""
    return await forward_request("pharmacy", f"/api/prescriptions/{prescription_id}", "DELETE")

# ==============================================================================
#  BILLING SERVICE  ->  Port 8005
# ==============================================================================

@app.get("/gateway/bills", tags=["Billing Service"])
async def get_all_bills(token: dict = Depends(verify_token)):
    """Get all bills"""
    return await forward_request("billing", "/api/bills", "GET")

@app.get("/gateway/bills/patient/{patient_id}", tags=["Billing Service"])
async def get_bills_by_patient(patient_id: int, token: dict = Depends(verify_token)):
    """Get bills by patient"""
    return await forward_request("billing", f"/api/bills/patient/{patient_id}", "GET")

@app.get("/gateway/bills/doctor/{doctor_id}", tags=["Billing Service"])
async def get_bills_by_doctor(doctor_id: int, token: dict = Depends(verify_token)):
    """Get bills by doctor"""
    return await forward_request("billing", f"/api/bills/doctor/{doctor_id}", "GET")

@app.get("/gateway/bills/status/{payment_status}", tags=["Billing Service"])
async def get_bills_by_status(payment_status: str, token: dict = Depends(verify_token)):
    """Get bills by payment status"""
    return await forward_request("billing", f"/api/bills/status/{payment_status}", "GET")

@app.get("/gateway/bills/date/{date}", tags=["Billing Service"])
async def get_bills_by_date(date: str, token: dict = Depends(verify_token)):
    """Get bills by date (YYYY-MM-DD)"""
    return await forward_request("billing", f"/api/bills/date/{date}", "GET")

@app.get("/gateway/bills/{bill_id}", tags=["Billing Service"])
async def get_bill(bill_id: int, token: dict = Depends(verify_token)):
    """Get bill by ID"""
    return await forward_request("billing", f"/api/bills/{bill_id}", "GET")

@app.post("/gateway/bills", tags=["Billing Service"])
async def create_bill(bill: BillCreate, token: dict = Depends(verify_token)):
    """Create a new bill"""
    return await forward_request("billing", "/api/bills", "POST", json=bill.dict())

@app.put("/gateway/bills/{bill_id}", tags=["Billing Service"])
async def update_bill(bill_id: int, bill: BillUpdate, token: dict = Depends(verify_token)):
    """Update a bill"""
    return await forward_request("billing", f"/api/bills/{bill_id}", "PUT", json=bill.dict())

@app.patch("/gateway/bills/{bill_id}/pay", tags=["Billing Service"])
async def mark_bill_paid(bill_id: int, payment_method: PaymentMethodEnum = Query(...), token: dict = Depends(verify_token)):
    """Mark a bill as paid"""
    return await forward_request("billing", f"/api/bills/{bill_id}/pay?payment_method={payment_method}", "PATCH")

@app.delete("/gateway/bills/{bill_id}", tags=["Billing Service"])
async def delete_bill(bill_id: int, token: dict = Depends(verify_token)):
    """Delete a bill"""
    return await forward_request("billing", f"/api/bills/{bill_id}", "DELETE")

@app.get("/gateway/payments", tags=["Billing Service"])
async def get_all_payments(token: dict = Depends(verify_token)):
    """Get all payments"""
    return await forward_request("billing", "/api/payments", "GET")

@app.get("/gateway/payments/bill/{bill_id}", tags=["Billing Service"])
async def get_payments_by_bill(bill_id: int, token: dict = Depends(verify_token)):
    """Get payments by bill"""
    return await forward_request("billing", f"/api/payments/bill/{bill_id}", "GET")

@app.get("/gateway/payments/patient/{patient_id}", tags=["Billing Service"])
async def get_payments_by_patient(patient_id: int, token: dict = Depends(verify_token)):
    """Get payments by patient"""
    return await forward_request("billing", f"/api/payments/patient/{patient_id}", "GET")

@app.get("/gateway/payments/{payment_id}", tags=["Billing Service"])
async def get_payment(payment_id: int, token: dict = Depends(verify_token)):
    """Get payment by ID"""
    return await forward_request("billing", f"/api/payments/{payment_id}", "GET")

@app.post("/gateway/payments", tags=["Billing Service"])
async def create_payment(payment: PaymentCreate, token: dict = Depends(verify_token)):
    """Record a new payment"""
    return await forward_request("billing", "/api/payments", "POST", json=payment.dict())

@app.delete("/gateway/payments/{payment_id}", tags=["Billing Service"])
async def delete_payment(payment_id: int, token: dict = Depends(verify_token)):
    """Delete a payment"""
    return await forward_request("billing", f"/api/payments/{payment_id}", "DELETE")