# doctor-service/service.py
from data_service import DoctorDataService
from models import DoctorCreate, DoctorUpdate, Specialization, Availability

class DoctorService:
    def __init__(self):
        self.data_service = DoctorDataService()

    def get_all(self):
        return self.data_service.get_all_doctors()

    def get_by_id(self, doctor_id: int):
        return self.data_service.get_doctor_by_id(doctor_id)

    def get_by_specialization(self, specialization: Specialization):
        return self.data_service.get_doctors_by_specialization(specialization)

    def get_by_availability(self, availability: Availability):
        return self.data_service.get_doctors_by_availability(availability)

    def get_available_doctors(self):
        return self.data_service.get_available_doctors()

    def create(self, doctor_data: DoctorCreate):
        return self.data_service.add_doctor(doctor_data)

    def update(self, doctor_id: int, doctor_data: DoctorUpdate):
        return self.data_service.update_doctor(doctor_id, doctor_data)

    def delete(self, doctor_id: int):
        return self.data_service.delete_doctor(doctor_id)
