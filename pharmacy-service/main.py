# pharmacy-service/main.py
from fastapi import FastAPI, HTTPException, status
from models import (
    Medicine, MedicineCreate, MedicineUpdate, MedicineCategory, MedicineStatus,
    Prescription, PrescriptionCreate, PrescriptionUpdate, PrescriptionStatus
)
from service import PharmacyService
from typing import List

app = FastAPI(
    title="Pharmacy Microservice",
    description="Manages all medicines and prescriptions for the Hospital Management System",
    version="1.0.0"
)

# Initialize service
pharmacy_service = PharmacyService()

# ─── Root ─────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health Check"])
def read_root():
    return {
        "service": "Pharmacy Microservice",
        "status": "running",
        "version": "1.0.0",
        "port": 8004
    }

# ==============================================================================
#  MEDICINE ENDPOINTS
# ==============================================================================

# ─── GET All Medicines ────────────────────────────────────────────────────────
@app.get("/api/medicines", response_model=List[Medicine], tags=["Medicines"])
def get_all_medicines():
    """Retrieve all medicines available in the pharmacy"""
    return pharmacy_service.get_all_medicines()

# ─── GET Medicine by ID ───────────────────────────────────────────────────────
@app.get("/api/medicines/{medicine_id}", response_model=Medicine, tags=["Medicines"])
def get_medicine(medicine_id: int):
    """Retrieve a specific medicine by its ID"""
    medicine = pharmacy_service.get_medicine_by_id(medicine_id)
    if not medicine:
        raise HTTPException(
            status_code=404,
            detail=f"Medicine with ID {medicine_id} not found"
        )
    return medicine

# ─── GET Medicines by Category ────────────────────────────────────────────────
@app.get("/api/medicines/category/{category}", response_model=List[Medicine], tags=["Medicines"])
def get_medicines_by_category(category: MedicineCategory):
    """Retrieve all medicines filtered by category"""
    medicines = pharmacy_service.get_medicines_by_category(category)
    if not medicines:
        raise HTTPException(
            status_code=404,
            detail=f"No medicines found in category {category}"
        )
    return medicines

# ─── GET Medicines by Stock Status ────────────────────────────────────────────
@app.get("/api/medicines/stock/{status}", response_model=List[Medicine], tags=["Medicines"])
def get_medicines_by_status(status: MedicineStatus):
    """Retrieve all medicines filtered by stock status"""
    medicines = pharmacy_service.get_medicines_by_status(status)
    if not medicines:
        raise HTTPException(
            status_code=404,
            detail=f"No medicines found with status {status}"
        )
    return medicines

# ─── GET All In Stock Medicines ───────────────────────────────────────────────
@app.get("/api/medicines/available/instock", response_model=List[Medicine], tags=["Medicines"])
def get_in_stock_medicines():
    """Retrieve all medicines currently in stock"""
    medicines = pharmacy_service.get_in_stock_medicines()
    if not medicines:
        raise HTTPException(
            status_code=404,
            detail="No medicines currently in stock"
        )
    return medicines

# ─── POST Create Medicine ─────────────────────────────────────────────────────
@app.post("/api/medicines", response_model=Medicine, status_code=status.HTTP_201_CREATED, tags=["Medicines"])
def create_medicine(medicine: MedicineCreate):
    """Add a new medicine to the pharmacy inventory"""
    return pharmacy_service.create_medicine(medicine)

# ─── PUT Update Medicine ──────────────────────────────────────────────────────
@app.put("/api/medicines/{medicine_id}", response_model=Medicine, tags=["Medicines"])
def update_medicine(medicine_id: int, medicine: MedicineUpdate):
    """Update an existing medicine's details"""
    updated_medicine = pharmacy_service.update_medicine(medicine_id, medicine)
    if not updated_medicine:
        raise HTTPException(
            status_code=404,
            detail=f"Medicine with ID {medicine_id} not found"
        )
    return updated_medicine

# ─── DELETE Medicine ──────────────────────────────────────────────────────────
@app.delete("/api/medicines/{medicine_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Medicines"])
def delete_medicine(medicine_id: int):
    """Remove a medicine from the pharmacy inventory"""
    success = pharmacy_service.delete_medicine(medicine_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Medicine with ID {medicine_id} not found"
        )
    return None

# ==============================================================================
#  PRESCRIPTION ENDPOINTS
# ==============================================================================

# ─── GET All Prescriptions ────────────────────────────────────────────────────
@app.get("/api/prescriptions", response_model=List[Prescription], tags=["Prescriptions"])
def get_all_prescriptions():
    """Retrieve all prescriptions in the system"""
    return pharmacy_service.get_all_prescriptions()

# ─── GET Prescription by ID ───────────────────────────────────────────────────
@app.get("/api/prescriptions/{prescription_id}", response_model=Prescription, tags=["Prescriptions"])
def get_prescription(prescription_id: int):
    """Retrieve a specific prescription by its ID"""
    prescription = pharmacy_service.get_prescription_by_id(prescription_id)
    if not prescription:
        raise HTTPException(
            status_code=404,
            detail=f"Prescription with ID {prescription_id} not found"
        )
    return prescription

# ─── GET Prescriptions by Patient ────────────────────────────────────────────
@app.get("/api/prescriptions/patient/{patient_id}", response_model=List[Prescription], tags=["Prescriptions"])
def get_prescriptions_by_patient(patient_id: int):
    """Retrieve all prescriptions for a specific patient"""
    prescriptions = pharmacy_service.get_prescriptions_by_patient(patient_id)
    if not prescriptions:
        raise HTTPException(
            status_code=404,
            detail=f"No prescriptions found for patient ID {patient_id}"
        )
    return prescriptions

# ─── GET Prescriptions by Doctor ─────────────────────────────────────────────
@app.get("/api/prescriptions/doctor/{doctor_id}", response_model=List[Prescription], tags=["Prescriptions"])
def get_prescriptions_by_doctor(doctor_id: int):
    """Retrieve all prescriptions issued by a specific doctor"""
    prescriptions = pharmacy_service.get_prescriptions_by_doctor(doctor_id)
    if not prescriptions:
        raise HTTPException(
            status_code=404,
            detail=f"No prescriptions found for doctor ID {doctor_id}"
        )
    return prescriptions

# ─── GET Prescriptions by Status ─────────────────────────────────────────────
@app.get("/api/prescriptions/status/{status}", response_model=List[Prescription], tags=["Prescriptions"])
def get_prescriptions_by_status(status: PrescriptionStatus):
    """Retrieve all prescriptions filtered by status"""
    prescriptions = pharmacy_service.get_prescriptions_by_status(status)
    if not prescriptions:
        raise HTTPException(
            status_code=404,
            detail=f"No prescriptions found with status {status}"
        )
    return prescriptions

# ─── POST Create Prescription ─────────────────────────────────────────────────
@app.post("/api/prescriptions", response_model=Prescription, status_code=status.HTTP_201_CREATED, tags=["Prescriptions"])
def create_prescription(prescription: PrescriptionCreate):
    """Create a new prescription in the system"""
    return pharmacy_service.create_prescription(prescription)

# ─── PUT Update Prescription ──────────────────────────────────────────────────
@app.put("/api/prescriptions/{prescription_id}", response_model=Prescription, tags=["Prescriptions"])
def update_prescription(prescription_id: int, prescription: PrescriptionUpdate):
    """Update an existing prescription's details"""
    updated = pharmacy_service.update_prescription(prescription_id, prescription)
    if not updated:
        raise HTTPException(
            status_code=404,
            detail=f"Prescription with ID {prescription_id} not found"
        )
    return updated

# ─── PATCH Dispense Prescription ─────────────────────────────────────────────
@app.patch("/api/prescriptions/{prescription_id}/dispense", response_model=Prescription, tags=["Prescriptions"])
def dispense_prescription(prescription_id: int):
    """Mark a prescription as dispensed"""
    dispensed = pharmacy_service.dispense_prescription(prescription_id)
    if not dispensed:
        raise HTTPException(
            status_code=404,
            detail=f"Prescription with ID {prescription_id} not found"
        )
    return dispensed

# ─── DELETE Prescription ──────────────────────────────────────────────────────
@app.delete("/api/prescriptions/{prescription_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Prescriptions"])
def delete_prescription(prescription_id: int):
    """Remove a prescription from the system"""
    success = pharmacy_service.delete_prescription(prescription_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Prescription with ID {prescription_id} not found"
        )
    return None
