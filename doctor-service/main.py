# doctor-service/main.py
from fastapi import FastAPI, HTTPException, status
from models import Doctor, DoctorCreate, DoctorUpdate, Specialization, Availability
from service import DoctorService
from typing import List

app = FastAPI(
    title="Doctor Microservice",
    description="Manages all doctor records for the Hospital Management System",
    version="1.0.0"
)

# Initialize service
doctor_service = DoctorService()

# ─── Root ─────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health Check"])
def read_root():
    return {
        "service": "Doctor Microservice",
        "status": "running",
        "version": "1.0.0",
        "port": 8002
    }

# ─── GET All Doctors ──────────────────────────────────────────────────────────
@app.get("/api/doctors", response_model=List[Doctor], tags=["Doctors"])
def get_all_doctors():
    """Retrieve all doctors registered in the hospital"""
    return doctor_service.get_all()

# ─── GET Doctor by ID ─────────────────────────────────────────────────────────
@app.get("/api/doctors/{doctor_id}", response_model=Doctor, tags=["Doctors"])
def get_doctor(doctor_id: int):
    """Retrieve a specific doctor by their ID"""
    doctor = doctor_service.get_by_id(doctor_id)
    if not doctor:
        raise HTTPException(
            status_code=404,
            detail=f"Doctor with ID {doctor_id} not found"
        )
    return doctor

# ─── GET Doctors by Specialization ───────────────────────────────────────────
@app.get("/api/doctors/specialization/{specialization}", response_model=List[Doctor], tags=["Doctors"])
def get_doctors_by_specialization(specialization: Specialization):
    """Retrieve all doctors with a specific specialization"""
    doctors = doctor_service.get_by_specialization(specialization)
    if not doctors:
        raise HTTPException(
            status_code=404,
            detail=f"No doctors found with specialization {specialization}"
        )
    return doctors

# ─── GET Doctors by Availability ─────────────────────────────────────────────
@app.get("/api/doctors/availability/{availability}", response_model=List[Doctor], tags=["Doctors"])
def get_doctors_by_availability(availability: Availability):
    """Retrieve all doctors filtered by availability status"""
    doctors = doctor_service.get_by_availability(availability)
    if not doctors:
        raise HTTPException(
            status_code=404,
            detail=f"No doctors found with availability status {availability}"
        )
    return doctors

# ─── GET All Available Doctors ────────────────────────────────────────────────
@app.get("/api/doctors/status/available", response_model=List[Doctor], tags=["Doctors"])
def get_available_doctors():
    """Retrieve all currently available doctors"""
    doctors = doctor_service.get_available_doctors()
    if not doctors:
        raise HTTPException(
            status_code=404,
            detail="No available doctors found at the moment"
        )
    return doctors

# ─── POST Create Doctor ───────────────────────────────────────────────────────
@app.post("/api/doctors", response_model=Doctor, status_code=status.HTTP_201_CREATED, tags=["Doctors"])
def create_doctor(doctor: DoctorCreate):
    """Register a new doctor in the hospital system"""
    return doctor_service.create(doctor)

# ─── PUT Update Doctor ────────────────────────────────────────────────────────
@app.put("/api/doctors/{doctor_id}", response_model=Doctor, tags=["Doctors"])
def update_doctor(doctor_id: int, doctor: DoctorUpdate):
    """Update an existing doctor's information"""
    updated_doctor = doctor_service.update(doctor_id, doctor)
    if not updated_doctor:
        raise HTTPException(
            status_code=404,
            detail=f"Doctor with ID {doctor_id} not found"
        )
    return updated_doctor

# ─── DELETE Doctor ────────────────────────────────────────────────────────────
@app.delete("/api/doctors/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Doctors"])
def delete_doctor(doctor_id: int):
    """Remove a doctor record from the system"""
    success = doctor_service.delete(doctor_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Doctor with ID {doctor_id} not found"
        )
    return None
