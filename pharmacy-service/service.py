# pharmacy-service/service.py
from data_service import PharmacyDataService
from models import (
    MedicineCreate, MedicineUpdate, MedicineCategory, MedicineStatus,
    PrescriptionCreate, PrescriptionUpdate, PrescriptionStatus
)

class PharmacyService:
    def __init__(self):
        self.data_service = PharmacyDataService()

    # ─── Medicine Methods ──────────────────────────────────────────────────────
    def get_all_medicines(self):
        return self.data_service.get_all_medicines()

    def get_medicine_by_id(self, medicine_id: int):
        return self.data_service.get_medicine_by_id(medicine_id)

    def get_medicines_by_category(self, category: MedicineCategory):
        return self.data_service.get_medicines_by_category(category)

    def get_medicines_by_status(self, status: MedicineStatus):
        return self.data_service.get_medicines_by_status(status)

    def get_in_stock_medicines(self):
        return self.data_service.get_in_stock_medicines()

    def create_medicine(self, medicine_data: MedicineCreate):
        return self.data_service.add_medicine(medicine_data)

    def update_medicine(self, medicine_id: int, medicine_data: MedicineUpdate):
        return self.data_service.update_medicine(medicine_id, medicine_data)

    def delete_medicine(self, medicine_id: int):
        return self.data_service.delete_medicine(medicine_id)

    # ─── Prescription Methods ──────────────────────────────────────────────────
    def get_all_prescriptions(self):
        return self.data_service.get_all_prescriptions()

    def get_prescription_by_id(self, prescription_id: int):
        return self.data_service.get_prescription_by_id(prescription_id)

    def get_prescriptions_by_patient(self, patient_id: int):
        return self.data_service.get_prescriptions_by_patient(patient_id)

    def get_prescriptions_by_doctor(self, doctor_id: int):
        return self.data_service.get_prescriptions_by_doctor(doctor_id)

    def get_prescriptions_by_status(self, status: PrescriptionStatus):
        return self.data_service.get_prescriptions_by_status(status)

    def create_prescription(self, prescription_data: PrescriptionCreate):
        return self.data_service.add_prescription(prescription_data)

    def update_prescription(self, prescription_id: int, prescription_data: PrescriptionUpdate):
        return self.data_service.update_prescription(prescription_id, prescription_data)

    def dispense_prescription(self, prescription_id: int):
        return self.data_service.dispense_prescription(prescription_id)

    def delete_prescription(self, prescription_id: int):
        return self.data_service.delete_prescription(prescription_id)
