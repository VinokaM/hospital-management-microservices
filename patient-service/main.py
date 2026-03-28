# patient-service/main.py
from fastapi import FastAPI, HTTPException, status
from models import Patient, PatientCreate, PatientUpdate, BloodGroup, Gender
from service import PatientService
from typing import List

app = FastAPI(
    title="Patient Microservice",
    description="Manages all patient records for the Hospital Management System",
    version="1.0.0"
)

# Initialize service
patient_service = PatientService()

# ─── Root ─────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health Check"])
def read_root():
    return {
        "service": "Patient Microservice",
        "status": "running",
        "version": "1.0.0",
        "port": 8001
    }

# ─── GET All Patients ─────────────────────────────────────────────────────────
@app.get("/api/patients", response_model=List[Patient], tags=["Patients"])
def get_all_patients():
    """Retrieve all patients registered in the hospital"""
    return patient_service.get_all()

# ─── GET Patient by ID ────────────────────────────────────────────────────────
@app.get("/api/patients/{patient_id}", response_model=Patient, tags=["Patients"])
def get_patient(patient_id: int):
    """Retrieve a specific patient by their ID"""
    patient = patient_service.get_by_id(patient_id)
    if not patient:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} not found"
        )
    return patient

# ─── GET Patients by Blood Group ──────────────────────────────────────────────
@app.get("/api/patients/blood-group/{blood_group}", response_model=List[Patient], tags=["Patients"])
def get_patients_by_blood_group(blood_group: BloodGroup):
    """Retrieve all patients with a specific blood group"""
    patients = patient_service.get_by_blood_group(blood_group)
    if not patients:
        raise HTTPException(
            status_code=404,
            detail=f"No patients found with blood group {blood_group}"
        )
    return patients

# ─── GET Patients by Gender ───────────────────────────────────────────────────
@app.get("/api/patients/gender/{gender}", response_model=List[Patient], tags=["Patients"])
def get_patients_by_gender(gender: Gender):
    """Retrieve all patients filtered by gender"""
    patients = patient_service.get_by_gender(gender)
    if not patients:
        raise HTTPException(
            status_code=404,
            detail=f"No patients found with gender {gender}"
        )
    return patients

# ─── POST Create Patient ──────────────────────────────────────────────────────
@app.post("/api/patients", response_model=Patient, status_code=status.HTTP_201_CREATED, tags=["Patients"])
def create_patient(patient: PatientCreate):
    """Register a new patient in the hospital system"""
    return patient_service.create(patient)

# ─── PUT Update Patient ───────────────────────────────────────────────────────
@app.put("/api/patients/{patient_id}", response_model=Patient, tags=["Patients"])
def update_patient(patient_id: int, patient: PatientUpdate):
    """Update an existing patient's information"""
    updated_patient = patient_service.update(patient_id, patient)
    if not updated_patient:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} not found"
        )
    return updated_patient

# ─── DELETE Patient ───────────────────────────────────────────────────────────
@app.delete("/api/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Patients"])
def delete_patient(patient_id: int):
    """Remove a patient record from the system"""
    success = patient_service.delete(patient_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} not found"
        )
    return None
