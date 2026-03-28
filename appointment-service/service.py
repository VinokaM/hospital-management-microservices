# appointment-service/service.py
from data_service import AppointmentDataService
from models import AppointmentCreate, AppointmentUpdate, AppointmentStatus, AppointmentType

class AppointmentService:
    def __init__(self):
        self.data_service = AppointmentDataService()

    def get_all(self):
        return self.data_service.get_all_appointments()

    def get_by_id(self, appointment_id: int):
        return self.data_service.get_appointment_by_id(appointment_id)

    def get_by_patient(self, patient_id: int):
        return self.data_service.get_appointments_by_patient(patient_id)

    def get_by_doctor(self, doctor_id: int):
        return self.data_service.get_appointments_by_doctor(doctor_id)

    def get_by_status(self, status: AppointmentStatus):
        return self.data_service.get_appointments_by_status(status)

    def get_by_date(self, date: str):
        return self.data_service.get_appointments_by_date(date)

    def get_by_type(self, appointment_type: AppointmentType):
        return self.data_service.get_appointments_by_type(appointment_type)

    def create(self, appointment_data: AppointmentCreate):
        return self.data_service.add_appointment(appointment_data)

    def update(self, appointment_id: int, appointment_data: AppointmentUpdate):
        return self.data_service.update_appointment(appointment_id, appointment_data)

    def cancel(self, appointment_id: int):
        return self.data_service.cancel_appointment(appointment_id)

    def delete(self, appointment_id: int):
        return self.data_service.delete_appointment(appointment_id)
