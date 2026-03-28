# appointment-service/main.py
from fastapi import FastAPI, HTTPException, status
from models import Appointment, AppointmentCreate, AppointmentUpdate, AppointmentStatus, AppointmentType
from service import AppointmentService
from typing import List

app = FastAPI(
    title="Appointment Microservice",
    description="Manages all appointment records for the Hospital Management System",
    version="1.0.0"
)

# Initialize service
appointment_service = AppointmentService()

# ─── Root ─────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health Check"])
def read_root():
    return {
        "service": "Appointment Microservice",
        "status": "running",
        "version": "1.0.0",
        "port": 8003
    }

# ─── GET All Appointments ─────────────────────────────────────────────────────
@app.get("/api/appointments", response_model=List[Appointment], tags=["Appointments"])
def get_all_appointments():
    """Retrieve all appointments in the hospital"""
    return appointment_service.get_all()

# ─── GET Appointment by ID ────────────────────────────────────────────────────
@app.get("/api/appointments/{appointment_id}", response_model=Appointment, tags=["Appointments"])
def get_appointment(appointment_id: int):
    """Retrieve a specific appointment by its ID"""
    appointment = appointment_service.get_by_id(appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=404,
            detail=f"Appointment with ID {appointment_id} not found"
        )
    return appointment

# ─── GET Appointments by Patient ─────────────────────────────────────────────
@app.get("/api/appointments/patient/{patient_id}", response_model=List[Appointment], tags=["Appointments"])
def get_appointments_by_patient(patient_id: int):
    """Retrieve all appointments for a specific patient"""
    appointments = appointment_service.get_by_patient(patient_id)
    if not appointments:
        raise HTTPException(
            status_code=404,
            detail=f"No appointments found for patient ID {patient_id}"
        )
    return appointments

# ─── GET Appointments by Doctor ──────────────────────────────────────────────
@app.get("/api/appointments/doctor/{doctor_id}", response_model=List[Appointment], tags=["Appointments"])
def get_appointments_by_doctor(doctor_id: int):
    """Retrieve all appointments assigned to a specific doctor"""
    appointments = appointment_service.get_by_doctor(doctor_id)
    if not appointments:
        raise HTTPException(
            status_code=404,
            detail=f"No appointments found for doctor ID {doctor_id}"
        )
    return appointments

# ─── GET Appointments by Status ───────────────────────────────────────────────
@app.get("/api/appointments/status/{status}", response_model=List[Appointment], tags=["Appointments"])
def get_appointments_by_status(status: AppointmentStatus):
    """Retrieve all appointments filtered by status"""
    appointments = appointment_service.get_by_status(status)
    if not appointments:
        raise HTTPException(
            status_code=404,
            detail=f"No appointments found with status {status}"
        )
    return appointments

# ─── GET Appointments by Date ─────────────────────────────────────────────────
@app.get("/api/appointments/date/{date}", response_model=List[Appointment], tags=["Appointments"])
def get_appointments_by_date(date: str):
    """Retrieve all appointments for a specific date (format: YYYY-MM-DD)"""
    appointments = appointment_service.get_by_date(date)
    if not appointments:
        raise HTTPException(
            status_code=404,
            detail=f"No appointments found for date {date}"
        )
    return appointments

# ─── GET Appointments by Type ─────────────────────────────────────────────────
@app.get("/api/appointments/type/{appointment_type}", response_model=List[Appointment], tags=["Appointments"])
def get_appointments_by_type(appointment_type: AppointmentType):
    """Retrieve all appointments filtered by type"""
    appointments = appointment_service.get_by_type(appointment_type)
    if not appointments:
        raise HTTPException(
            status_code=404,
            detail=f"No appointments found with type {appointment_type}"
        )
    return appointments

# ─── POST Create Appointment ──────────────────────────────────────────────────
@app.post("/api/appointments", response_model=Appointment, status_code=status.HTTP_201_CREATED, tags=["Appointments"])
def create_appointment(appointment: AppointmentCreate):
    """Schedule a new appointment in the hospital system"""
    return appointment_service.create(appointment)

# ─── PUT Update Appointment ───────────────────────────────────────────────────
@app.put("/api/appointments/{appointment_id}", response_model=Appointment, tags=["Appointments"])
def update_appointment(appointment_id: int, appointment: AppointmentUpdate):
    """Update an existing appointment's details"""
    updated_appointment = appointment_service.update(appointment_id, appointment)
    if not updated_appointment:
        raise HTTPException(
            status_code=404,
            detail=f"Appointment with ID {appointment_id} not found"
        )
    return updated_appointment

# ─── PATCH Cancel Appointment ─────────────────────────────────────────────────
@app.patch("/api/appointments/{appointment_id}/cancel", response_model=Appointment, tags=["Appointments"])
def cancel_appointment(appointment_id: int):
    """Cancel a specific appointment"""
    cancelled = appointment_service.cancel(appointment_id)
    if not cancelled:
        raise HTTPException(
            status_code=404,
            detail=f"Appointment with ID {appointment_id} not found"
        )
    return cancelled

# ─── DELETE Appointment ───────────────────────────────────────────────────────
@app.delete("/api/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Appointments"])
def delete_appointment(appointment_id: int):
    """Remove an appointment record from the system"""
    success = appointment_service.delete(appointment_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Appointment with ID {appointment_id} not found"
        )
    return None
