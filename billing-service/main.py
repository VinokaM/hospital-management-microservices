# billing-service/main.py
from fastapi import FastAPI, HTTPException, status, Query
from models import (
    Bill, BillCreate, BillUpdate,
    Payment, PaymentCreate,
    PaymentStatus, PaymentMethod
)
from service import BillingService
from typing import List

app = FastAPI(
    title="Billing Microservice",
    description="Manages all bills and payments for the Hospital Management System",
    version="1.0.0"
)

# Initialize service
billing_service = BillingService()

# ─── Root ─────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health Check"])
def read_root():
    return {
        "service": "Billing Microservice",
        "status": "running",
        "version": "1.0.0",
        "port": 8005
    }

# ==============================================================================
#  BILL ENDPOINTS
# ==============================================================================

# ─── GET All Bills ────────────────────────────────────────────────────────────
@app.get("/api/bills", response_model=List[Bill], tags=["Bills"])
def get_all_bills():
    """Retrieve all bills in the hospital system"""
    return billing_service.get_all_bills()

# ─── GET Bill by ID ───────────────────────────────────────────────────────────
@app.get("/api/bills/{bill_id}", response_model=Bill, tags=["Bills"])
def get_bill(bill_id: int):
    """Retrieve a specific bill by its ID"""
    bill = billing_service.get_bill_by_id(bill_id)
    if not bill:
        raise HTTPException(
            status_code=404,
            detail=f"Bill with ID {bill_id} not found"
        )
    return bill

# ─── GET Bills by Patient ─────────────────────────────────────────────────────
@app.get("/api/bills/patient/{patient_id}", response_model=List[Bill], tags=["Bills"])
def get_bills_by_patient(patient_id: int):
    """Retrieve all bills for a specific patient"""
    bills = billing_service.get_bills_by_patient(patient_id)
    if not bills:
        raise HTTPException(
            status_code=404,
            detail=f"No bills found for patient ID {patient_id}"
        )
    return bills

# ─── GET Bills by Doctor ──────────────────────────────────────────────────────
@app.get("/api/bills/doctor/{doctor_id}", response_model=List[Bill], tags=["Bills"])
def get_bills_by_doctor(doctor_id: int):
    """Retrieve all bills associated with a specific doctor"""
    bills = billing_service.get_bills_by_doctor(doctor_id)
    if not bills:
        raise HTTPException(
            status_code=404,
            detail=f"No bills found for doctor ID {doctor_id}"
        )
    return bills

# ─── GET Bills by Payment Status ──────────────────────────────────────────────
@app.get("/api/bills/status/{payment_status}", response_model=List[Bill], tags=["Bills"])
def get_bills_by_status(payment_status: PaymentStatus):
    """Retrieve all bills filtered by payment status"""
    bills = billing_service.get_bills_by_status(payment_status)
    if not bills:
        raise HTTPException(
            status_code=404,
            detail=f"No bills found with status {payment_status}"
        )
    return bills

# ─── GET Bills by Date ────────────────────────────────────────────────────────
@app.get("/api/bills/date/{date}", response_model=List[Bill], tags=["Bills"])
def get_bills_by_date(date: str):
    """Retrieve all bills for a specific date (format: YYYY-MM-DD)"""
    bills = billing_service.get_bills_by_date(date)
    if not bills:
        raise HTTPException(
            status_code=404,
            detail=f"No bills found for date {date}"
        )
    return bills

# ─── POST Create Bill ─────────────────────────────────────────────────────────
@app.post("/api/bills", response_model=Bill, status_code=status.HTTP_201_CREATED, tags=["Bills"])
def create_bill(bill: BillCreate):
    """Generate a new bill for a patient"""
    return billing_service.create_bill(bill)

# ─── PUT Update Bill ──────────────────────────────────────────────────────────
@app.put("/api/bills/{bill_id}", response_model=Bill, tags=["Bills"])
def update_bill(bill_id: int, bill: BillUpdate):
    """Update an existing bill's details"""
    updated_bill = billing_service.update_bill(bill_id, bill)
    if not updated_bill:
        raise HTTPException(
            status_code=404,
            detail=f"Bill with ID {bill_id} not found"
        )
    return updated_bill

# ─── PATCH Mark Bill as Paid ──────────────────────────────────────────────────
@app.patch("/api/bills/{bill_id}/pay", response_model=Bill, tags=["Bills"])
def mark_bill_paid(bill_id: int, payment_method: PaymentMethod = Query(..., description="Payment method used")):
    """Mark a bill as fully paid"""
    paid_bill = billing_service.mark_bill_paid(bill_id, payment_method)
    if not paid_bill:
        raise HTTPException(
            status_code=404,
            detail=f"Bill with ID {bill_id} not found"
        )
    return paid_bill

# ─── DELETE Bill ──────────────────────────────────────────────────────────────
@app.delete("/api/bills/{bill_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Bills"])
def delete_bill(bill_id: int):
    """Remove a bill from the system"""
    success = billing_service.delete_bill(bill_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Bill with ID {bill_id} not found"
        )
    return None

# ==============================================================================
#  PAYMENT ENDPOINTS
# ==============================================================================

# ─── GET All Payments ─────────────────────────────────────────────────────────
@app.get("/api/payments", response_model=List[Payment], tags=["Payments"])
def get_all_payments():
    """Retrieve all payment records in the system"""
    return billing_service.get_all_payments()

# ─── GET Payment by ID ────────────────────────────────────────────────────────
@app.get("/api/payments/{payment_id}", response_model=Payment, tags=["Payments"])
def get_payment(payment_id: int):
    """Retrieve a specific payment record by its ID"""
    payment = billing_service.get_payment_by_id(payment_id)
    if not payment:
        raise HTTPException(
            status_code=404,
            detail=f"Payment with ID {payment_id} not found"
        )
    return payment

# ─── GET Payments by Bill ─────────────────────────────────────────────────────
@app.get("/api/payments/bill/{bill_id}", response_model=List[Payment], tags=["Payments"])
def get_payments_by_bill(bill_id: int):
    """Retrieve all payments made for a specific bill"""
    payments = billing_service.get_payments_by_bill(bill_id)
    if not payments:
        raise HTTPException(
            status_code=404,
            detail=f"No payments found for bill ID {bill_id}"
        )
    return payments

# ─── GET Payments by Patient ──────────────────────────────────────────────────
@app.get("/api/payments/patient/{patient_id}", response_model=List[Payment], tags=["Payments"])
def get_payments_by_patient(patient_id: int):
    """Retrieve all payments made by a specific patient"""
    payments = billing_service.get_payments_by_patient(patient_id)
    if not payments:
        raise HTTPException(
            status_code=404,
            detail=f"No payments found for patient ID {patient_id}"
        )
    return payments

# ─── POST Create Payment ──────────────────────────────────────────────────────
@app.post("/api/payments", response_model=Payment, status_code=status.HTTP_201_CREATED, tags=["Payments"])
def create_payment(payment: PaymentCreate):
    """Record a new payment transaction"""
    return billing_service.create_payment(payment)

# ─── DELETE Payment ───────────────────────────────────────────────────────────
@app.delete("/api/payments/{payment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Payments"])
def delete_payment(payment_id: int):
    """Remove a payment record from the system"""
    success = billing_service.delete_payment(payment_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Payment with ID {payment_id} not found"
        )
    return None
