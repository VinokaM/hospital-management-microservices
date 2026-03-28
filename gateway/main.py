# gateway/main.py
from fastapi import FastAPI, HTTPException, Request, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi
import httpx
import jwt
import logging
import time
from datetime import datetime, timedelta
from typing import Any

# ─── Logging Setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("hospital-gateway")

# ─── App Setup ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Hospital Management - API Gateway",
    description="Central API Gateway for the Hospital Management System. Routes requests to all microservices.",
    version="1.0.0"
)

# ─── JWT Config ────────────────────────────────────────────────────────────────
SECRET_KEY = "hospital-secret-key-2026"
ALGORITHM = "HS256"
security = HTTPBearer()

# ─── All Microservice URLs ─────────────────────────────────────────────────────
SERVICES = {
    "patient":     "http://localhost:8001",
    "doctor":      "http://localhost:8002",
    "appointment": "http://localhost:8003",
    "pharmacy":    "http://localhost:8004",
    "billing":     "http://localhost:8005",
}

# ─── Custom Swagger with Authorize Button ──────────────────────────────────────
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
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ─── JWT Helper Functions ──────────────────────────────────────────────────────
def create_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired. Please login again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token. Please login again.")

# ─── Request Logging Middleware ────────────────────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"→ {request.method} {request.url.path}")
    response = await call_next(request)
    duration = round((time.time() - start_time) * 1000, 2)
    logger.info(f"← {response.status_code} | {duration}ms | {request.url.path}")
    return response

# ─── Forward Request Helper ────────────────────────────────────────────────────
async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    if service not in SERVICES:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Service not found",
                "service": service,
                "available_services": list(SERVICES.keys())
            }
        )

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

            if response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "error": "Resource not found",
                        "service": service,
                        "path": path
                    }
                )
            if response.status_code == 422:
                raise HTTPException(
                    status_code=422,
                    detail={
                        "error": "Validation error - check your request body",
                        "service": service,
                        "details": response.json()
                    }
                )
            if response.status_code >= 500:
                raise HTTPException(
                    status_code=502,
                    detail={
                        "error": "Upstream service error",
                        "service": service,
                        "upstream_status": response.status_code
                    }
                )

            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code
            )

        except httpx.ConnectError:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "Service is unreachable",
                    "service": service,
                    "url": url,
                    "hint": f"Make sure the {service} service is running"
                }
            )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail={
                    "error": "Service request timed out",
                    "service": service,
                    "timeout": "10 seconds"
                }
            )

# ==============================================================================
#  AUTH ENDPOINTS
# ==============================================================================

@app.post("/auth/login", tags=["Authentication"])
def login(username: str, password: str):
    """
    Login to get a JWT token.
    Use: username=admin | password=hospital2026
    """
    if username == "admin" and password == "hospital2026":
        token = create_token(username)
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": "2 hours",
            "message": "Login successful. Use the token in the Authorize button above."
        }
    raise HTTPException(
        status_code=401,
        detail={
            "error": "Invalid credentials",
            "hint": "Use username=admin and password=hospital2026"
        }
    )

# ─── Root ──────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Gateway Info"])
def read_root():
    return {
        "system": "Hospital Management System",
        "component": "API Gateway",
        "version": "1.0.0",
        "status": "running",
        "port": 8000,
        "services": {
            "patient-service":     "http://localhost:8001",
            "doctor-service":      "http://localhost:8002",
            "appointment-service": "http://localhost:8003",
            "pharmacy-service":    "http://localhost:8004",
            "billing-service":     "http://localhost:8005",
        },
        "login": "POST /auth/login with username=admin & password=hospital2026"
    }

# ==============================================================================
#  PATIENT SERVICE ROUTES  →  Port 8001
# ==============================================================================

@app.get("/gateway/patients", tags=["Patient Service"])
async def get_all_patients(token: dict = Depends(verify_token)):
    """Get all patients"""
    return await forward_request("patient", "/api/patients", "GET")

@app.get("/gateway/patients/blood-group/{blood_group}", tags=["Patient Service"])
async def get_patients_by_blood_group(blood_group: str, token: dict = Depends(verify_token)):
    """Get patients by blood group (A+, A-, B+, B-, AB+, AB-, O+, O-)"""
    return await forward_request("patient", f"/api/patients/blood-group/{blood_group}", "GET")

@app.get("/gateway/patients/gender/{gender}", tags=["Patient Service"])
async def get_patients_by_gender(gender: str, token: dict = Depends(verify_token)):
    """Get patients by gender (Male, Female, Other)"""
    return await forward_request("patient", f"/api/patients/gender/{gender}", "GET")

@app.get("/gateway/patients/{patient_id}", tags=["Patient Service"])
async def get_patient(patient_id: int, token: dict = Depends(verify_token)):
    """Get a specific patient by ID"""
    return await forward_request("patient", f"/api/patients/{patient_id}", "GET")

@app.post("/gateway/patients", tags=["Patient Service"])
async def create_patient(request: Request, token: dict = Depends(verify_token)):
    """Register a new patient"""
    body = await request.json()
    return await forward_request("patient", "/api/patients", "POST", json=body)

@app.put("/gateway/patients/{patient_id}", tags=["Patient Service"])
async def update_patient(patient_id: int, request: Request, token: dict = Depends(verify_token)):
    """Update an existing patient"""
    body = await request.json()
    return await forward_request("patient", f"/api/patients/{patient_id}", "PUT", json=body)

@app.delete("/gateway/patients/{patient_id}", tags=["Patient Service"])
async def delete_patient(patient_id: int, token: dict = Depends(verify_token)):
    """Delete a patient record"""
    return await forward_request("patient", f"/api/patients/{patient_id}", "DELETE")

# ==============================================================================
#  DOCTOR SERVICE ROUTES  →  Port 8002
# ==============================================================================

@app.get("/gateway/doctors", tags=["Doctor Service"])
async def get_all_doctors(token: dict = Depends(verify_token)):
    """Get all doctors"""
    return await forward_request("doctor", "/api/doctors", "GET")

@app.get("/gateway/doctors/status/available", tags=["Doctor Service"])
async def get_available_doctors(token: dict = Depends(verify_token)):
    """Get all currently available doctors"""
    return await forward_request("doctor", "/api/doctors/status/available", "GET")

@app.get("/gateway/doctors/specialization/{specialization}", tags=["Doctor Service"])
async def get_doctors_by_specialization(specialization: str, token: dict = Depends(verify_token)):
    """Get doctors by specialization"""
    return await forward_request("doctor", f"/api/doctors/specialization/{specialization}", "GET")

@app.get("/gateway/doctors/availability/{availability}", tags=["Doctor Service"])
async def get_doctors_by_availability(availability: str, token: dict = Depends(verify_token)):
    """Get doctors by availability (Available, Unavailable, On Leave)"""
    return await forward_request("doctor", f"/api/doctors/availability/{availability}", "GET")

@app.get("/gateway/doctors/{doctor_id}", tags=["Doctor Service"])
async def get_doctor(doctor_id: int, token: dict = Depends(verify_token)):
    """Get a specific doctor by ID"""
    return await forward_request("doctor", f"/api/doctors/{doctor_id}", "GET")

@app.post("/gateway/doctors", tags=["Doctor Service"])
async def create_doctor(request: Request, token: dict = Depends(verify_token)):
    """Register a new doctor"""
    body = await request.json()
    return await forward_request("doctor", "/api/doctors", "POST", json=body)

@app.put("/gateway/doctors/{doctor_id}", tags=["Doctor Service"])
async def update_doctor(doctor_id: int, request: Request, token: dict = Depends(verify_token)):
    """Update an existing doctor"""
    body = await request.json()
    return await forward_request("doctor", f"/api/doctors/{doctor_id}", "PUT", json=body)

@app.delete("/gateway/doctors/{doctor_id}", tags=["Doctor Service"])
async def delete_doctor(doctor_id: int, token: dict = Depends(verify_token)):
    """Delete a doctor record"""
    return await forward_request("doctor", f"/api/doctors/{doctor_id}", "DELETE")

# ==============================================================================
#  APPOINTMENT SERVICE ROUTES  →  Port 8003
# ==============================================================================

@app.get("/gateway/appointments", tags=["Appointment Service"])
async def get_all_appointments(token: dict = Depends(verify_token)):
    """Get all appointments"""
    return await forward_request("appointment", "/api/appointments", "GET")

@app.get("/gateway/appointments/patient/{patient_id}", tags=["Appointment Service"])
async def get_appointments_by_patient(patient_id: int, token: dict = Depends(verify_token)):
    """Get all appointments for a specific patient"""
    return await forward_request("appointment", f"/api/appointments/patient/{patient_id}", "GET")

@app.get("/gateway/appointments/doctor/{doctor_id}", tags=["Appointment Service"])
async def get_appointments_by_doctor(doctor_id: int, token: dict = Depends(verify_token)):
    """Get all appointments for a specific doctor"""
    return await forward_request("appointment", f"/api/appointments/doctor/{doctor_id}", "GET")

@app.get("/gateway/appointments/status/{status}", tags=["Appointment Service"])
async def get_appointments_by_status(status: str, token: dict = Depends(verify_token)):
    """Get appointments by status (Scheduled, Confirmed, Completed, Cancelled, No Show)"""
    return await forward_request("appointment", f"/api/appointments/status/{status}", "GET")

@app.get("/gateway/appointments/date/{date}", tags=["Appointment Service"])
async def get_appointments_by_date(date: str, token: dict = Depends(verify_token)):
    """Get appointments by date (format: YYYY-MM-DD)"""
    return await forward_request("appointment", f"/api/appointments/date/{date}", "GET")

@app.get("/gateway/appointments/type/{appointment_type}", tags=["Appointment Service"])
async def get_appointments_by_type(appointment_type: str, token: dict = Depends(verify_token)):
    """Get appointments by type"""
    return await forward_request("appointment", f"/api/appointments/type/{appointment_type}", "GET")

@app.get("/gateway/appointments/{appointment_id}", tags=["Appointment Service"])
async def get_appointment(appointment_id: int, token: dict = Depends(verify_token)):
    """Get a specific appointment by ID"""
    return await forward_request("appointment", f"/api/appointments/{appointment_id}", "GET")

@app.post("/gateway/appointments", tags=["Appointment Service"])
async def create_appointment(request: Request, token: dict = Depends(verify_token)):
    """Schedule a new appointment"""
    body = await request.json()
    return await forward_request("appointment", "/api/appointments", "POST", json=body)

@app.put("/gateway/appointments/{appointment_id}", tags=["Appointment Service"])
async def update_appointment(appointment_id: int, request: Request, token: dict = Depends(verify_token)):
    """Update an existing appointment"""
    body = await request.json()
    return await forward_request("appointment", f"/api/appointments/{appointment_id}", "PUT", json=body)

@app.patch("/gateway/appointments/{appointment_id}/cancel", tags=["Appointment Service"])
async def cancel_appointment(appointment_id: int, token: dict = Depends(verify_token)):
    """Cancel a specific appointment"""
    return await forward_request("appointment", f"/api/appointments/{appointment_id}/cancel", "PATCH")

@app.delete("/gateway/appointments/{appointment_id}", tags=["Appointment Service"])
async def delete_appointment(appointment_id: int, token: dict = Depends(verify_token)):
    """Delete an appointment record"""
    return await forward_request("appointment", f"/api/appointments/{appointment_id}", "DELETE")

# ==============================================================================
#  PHARMACY SERVICE ROUTES  →  Port 8004
# ==============================================================================

# ── Medicines ──────────────────────────────────────────────────────────────────
@app.get("/gateway/medicines", tags=["Pharmacy Service"])
async def get_all_medicines(token: dict = Depends(verify_token)):
    """Get all medicines in the pharmacy"""
    return await forward_request("pharmacy", "/api/medicines", "GET")

@app.get("/gateway/medicines/available/instock", tags=["Pharmacy Service"])
async def get_instock_medicines(token: dict = Depends(verify_token)):
    """Get all medicines currently in stock"""
    return await forward_request("pharmacy", "/api/medicines/available/instock", "GET")

@app.get("/gateway/medicines/category/{category}", tags=["Pharmacy Service"])
async def get_medicines_by_category(category: str, token: dict = Depends(verify_token)):
    """Get medicines by category"""
    return await forward_request("pharmacy", f"/api/medicines/category/{category}", "GET")

@app.get("/gateway/medicines/stock/{status}", tags=["Pharmacy Service"])
async def get_medicines_by_stock_status(status: str, token: dict = Depends(verify_token)):
    """Get medicines by stock status (In Stock, Low Stock, Out of Stock)"""
    return await forward_request("pharmacy", f"/api/medicines/stock/{status}", "GET")

@app.get("/gateway/medicines/{medicine_id}", tags=["Pharmacy Service"])
async def get_medicine(medicine_id: int, token: dict = Depends(verify_token)):
    """Get a specific medicine by ID"""
    return await forward_request("pharmacy", f"/api/medicines/{medicine_id}", "GET")

@app.post("/gateway/medicines", tags=["Pharmacy Service"])
async def create_medicine(request: Request, token: dict = Depends(verify_token)):
    """Add a new medicine to inventory"""
    body = await request.json()
    return await forward_request("pharmacy", "/api/medicines", "POST", json=body)

@app.put("/gateway/medicines/{medicine_id}", tags=["Pharmacy Service"])
async def update_medicine(medicine_id: int, request: Request, token: dict = Depends(verify_token)):
    """Update a medicine record"""
    body = await request.json()
    return await forward_request("pharmacy", f"/api/medicines/{medicine_id}", "PUT", json=body)

@app.delete("/gateway/medicines/{medicine_id}", tags=["Pharmacy Service"])
async def delete_medicine(medicine_id: int, token: dict = Depends(verify_token)):
    """Delete a medicine from inventory"""
    return await forward_request("pharmacy", f"/api/medicines/{medicine_id}", "DELETE")

# ── Prescriptions ──────────────────────────────────────────────────────────────
@app.get("/gateway/prescriptions", tags=["Pharmacy Service"])
async def get_all_prescriptions(token: dict = Depends(verify_token)):
    """Get all prescriptions"""
    return await forward_request("pharmacy", "/api/prescriptions", "GET")

@app.get("/gateway/prescriptions/patient/{patient_id}", tags=["Pharmacy Service"])
async def get_prescriptions_by_patient(patient_id: int, token: dict = Depends(verify_token)):
    """Get all prescriptions for a specific patient"""
    return await forward_request("pharmacy", f"/api/prescriptions/patient/{patient_id}", "GET")

@app.get("/gateway/prescriptions/doctor/{doctor_id}", tags=["Pharmacy Service"])
async def get_prescriptions_by_doctor(doctor_id: int, token: dict = Depends(verify_token)):
    """Get all prescriptions issued by a specific doctor"""
    return await forward_request("pharmacy", f"/api/prescriptions/doctor/{doctor_id}", "GET")

@app.get("/gateway/prescriptions/status/{status}", tags=["Pharmacy Service"])
async def get_prescriptions_by_status(status: str, token: dict = Depends(verify_token)):
    """Get prescriptions by status (Pending, Dispensed, Cancelled, On Hold)"""
    return await forward_request("pharmacy", f"/api/prescriptions/status/{status}", "GET")

@app.get("/gateway/prescriptions/{prescription_id}", tags=["Pharmacy Service"])
async def get_prescription(prescription_id: int, token: dict = Depends(verify_token)):
    """Get a specific prescription by ID"""
    return await forward_request("pharmacy", f"/api/prescriptions/{prescription_id}", "GET")

@app.post("/gateway/prescriptions", tags=["Pharmacy Service"])
async def create_prescription(request: Request, token: dict = Depends(verify_token)):
    """Create a new prescription"""
    body = await request.json()
    return await forward_request("pharmacy", "/api/prescriptions", "POST", json=body)

@app.put("/gateway/prescriptions/{prescription_id}", tags=["Pharmacy Service"])
async def update_prescription(prescription_id: int, request: Request, token: dict = Depends(verify_token)):
    """Update an existing prescription"""
    body = await request.json()
    return await forward_request("pharmacy", f"/api/prescriptions/{prescription_id}", "PUT", json=body)

@app.patch("/gateway/prescriptions/{prescription_id}/dispense", tags=["Pharmacy Service"])
async def dispense_prescription(prescription_id: int, token: dict = Depends(verify_token)):
    """Mark a prescription as dispensed"""
    return await forward_request("pharmacy", f"/api/prescriptions/{prescription_id}/dispense", "PATCH")

@app.delete("/gateway/prescriptions/{prescription_id}", tags=["Pharmacy Service"])
async def delete_prescription(prescription_id: int, token: dict = Depends(verify_token)):
    """Delete a prescription record"""
    return await forward_request("pharmacy", f"/api/prescriptions/{prescription_id}", "DELETE")

# ==============================================================================
#  BILLING SERVICE ROUTES  →  Port 8005
# ==============================================================================

# ── Bills ──────────────────────────────────────────────────────────────────────
@app.get("/gateway/bills", tags=["Billing Service"])
async def get_all_bills(token: dict = Depends(verify_token)):
    """Get all bills"""
    return await forward_request("billing", "/api/bills", "GET")

@app.get("/gateway/bills/patient/{patient_id}", tags=["Billing Service"])
async def get_bills_by_patient(patient_id: int, token: dict = Depends(verify_token)):
    """Get all bills for a specific patient"""
    return await forward_request("billing", f"/api/bills/patient/{patient_id}", "GET")

@app.get("/gateway/bills/doctor/{doctor_id}", tags=["Billing Service"])
async def get_bills_by_doctor(doctor_id: int, token: dict = Depends(verify_token)):
    """Get all bills associated with a specific doctor"""
    return await forward_request("billing", f"/api/bills/doctor/{doctor_id}", "GET")

@app.get("/gateway/bills/status/{payment_status}", tags=["Billing Service"])
async def get_bills_by_status(payment_status: str, token: dict = Depends(verify_token)):
    """Get bills by payment status (Pending, Paid, Partially Paid, Overdue, Cancelled, Refunded)"""
    return await forward_request("billing", f"/api/bills/status/{payment_status}", "GET")

@app.get("/gateway/bills/date/{date}", tags=["Billing Service"])
async def get_bills_by_date(date: str, token: dict = Depends(verify_token)):
    """Get bills by date (format: YYYY-MM-DD)"""
    return await forward_request("billing", f"/api/bills/date/{date}", "GET")

@app.get("/gateway/bills/{bill_id}", tags=["Billing Service"])
async def get_bill(bill_id: int, token: dict = Depends(verify_token)):
    """Get a specific bill by ID"""
    return await forward_request("billing", f"/api/bills/{bill_id}", "GET")

@app.post("/gateway/bills", tags=["Billing Service"])
async def create_bill(request: Request, token: dict = Depends(verify_token)):
    """Generate a new bill for a patient"""
    body = await request.json()
    return await forward_request("billing", "/api/bills", "POST", json=body)

@app.put("/gateway/bills/{bill_id}", tags=["Billing Service"])
async def update_bill(bill_id: int, request: Request, token: dict = Depends(verify_token)):
    """Update an existing bill"""
    body = await request.json()
    return await forward_request("billing", f"/api/bills/{bill_id}", "PUT", json=body)

@app.patch("/gateway/bills/{bill_id}/pay", tags=["Billing Service"])
async def mark_bill_paid(bill_id: int, payment_method: str = Query(..., description="Payment method: Cash, Credit Card, Debit Card, Insurance, Bank Transfer, Online Payment"), token: dict = Depends(verify_token)):
    """Mark a bill as fully paid"""
    return await forward_request("billing", f"/api/bills/{bill_id}/pay?payment_method={payment_method}", "PATCH")

@app.delete("/gateway/bills/{bill_id}", tags=["Billing Service"])
async def delete_bill(bill_id: int, token: dict = Depends(verify_token)):
    """Delete a bill record"""
    return await forward_request("billing", f"/api/bills/{bill_id}", "DELETE")

# ── Payments ───────────────────────────────────────────────────────────────────
@app.get("/gateway/payments", tags=["Billing Service"])
async def get_all_payments(token: dict = Depends(verify_token)):
    """Get all payment records"""
    return await forward_request("billing", "/api/payments", "GET")

@app.get("/gateway/payments/bill/{bill_id}", tags=["Billing Service"])
async def get_payments_by_bill(bill_id: int, token: dict = Depends(verify_token)):
    """Get all payments made for a specific bill"""
    return await forward_request("billing", f"/api/payments/bill/{bill_id}", "GET")

@app.get("/gateway/payments/patient/{patient_id}", tags=["Billing Service"])
async def get_payments_by_patient(patient_id: int, token: dict = Depends(verify_token)):
    """Get all payments made by a specific patient"""
    return await forward_request("billing", f"/api/payments/patient/{patient_id}", "GET")

@app.get("/gateway/payments/{payment_id}", tags=["Billing Service"])
async def get_payment(payment_id: int, token: dict = Depends(verify_token)):
    """Get a specific payment by ID"""
    return await forward_request("billing", f"/api/payments/{payment_id}", "GET")

@app.post("/gateway/payments", tags=["Billing Service"])
async def create_payment(request: Request, token: dict = Depends(verify_token)):
    """Record a new payment transaction"""
    body = await request.json()
    return await forward_request("billing", "/api/payments", "POST", json=body)

@app.delete("/gateway/payments/{payment_id}", tags=["Billing Service"])
async def delete_payment(payment_id: int, token: dict = Depends(verify_token)):
    """Delete a payment record"""
    return await forward_request("billing", f"/api/payments/{payment_id}", "DELETE")
