# patient-service/service.py
from data_service import PatientDataService
from models import PatientCreate, PatientUpdate, BloodGroup, Gender

class PatientService:
    def __init__(self):
        self.data_service = PatientDataService()

    def get_all(self):
        return self.data_service.get_all_patients()

    def get_by_id(self, patient_id: int):
        return self.data_service.get_patient_by_id(patient_id)

    def get_by_blood_group(self, blood_group: BloodGroup):
        return self.data_service.get_patients_by_blood_group(blood_group)

    def get_by_gender(self, gender: Gender):
        return self.data_service.get_patients_by_gender(gender)

    def create(self, patient_data: PatientCreate):
        return self.data_service.add_patient(patient_data)

    def update(self, patient_id: int, patient_data: PatientUpdate):
        return self.data_service.update_patient(patient_id, patient_data)

    def delete(self, patient_id: int):
        return self.data_service.delete_patient(patient_id)
