# pharmacy-service/data_service.py
from models import (
    Medicine, MedicineCreate, MedicineUpdate, MedicineCategory, MedicineStatus,
    Prescription, PrescriptionCreate, PrescriptionUpdate, PrescriptionStatus
)

class PharmacyDataService:
    def __init__(self):

        # ─── Mock Medicine Data ────────────────────────────────────────────────
        self.medicines = [
            Medicine(
                id=1,
                name="Metformin 500mg",
                generic_name="Metformin Hydrochloride",
                category=MedicineCategory.DIABETES,
                manufacturer="CeyPharma Ltd",
                unit_price=15.50,
                stock_quantity=500,
                status=MedicineStatus.IN_STOCK,
                description="Used to treat type 2 diabetes",
                expiry_date="2027-06-30"
            ),
            Medicine(
                id=2,
                name="Amoxicillin 250mg",
                generic_name="Amoxicillin Trihydrate",
                category=MedicineCategory.ANTIBIOTIC,
                manufacturer="Hemas Pharma",
                unit_price=8.75,
                stock_quantity=45,
                status=MedicineStatus.LOW_STOCK,
                description="Broad spectrum antibiotic for bacterial infections",
                expiry_date="2026-12-31"
            ),
            Medicine(
                id=3,
                name="Atorvastatin 20mg",
                generic_name="Atorvastatin Calcium",
                category=MedicineCategory.CARDIOVASCULAR,
                manufacturer="CeyPharma Ltd",
                unit_price=22.00,
                stock_quantity=300,
                status=MedicineStatus.IN_STOCK,
                description="Used to lower cholesterol and prevent heart disease",
                expiry_date="2027-03-31"
            ),
            Medicine(
                id=4,
                name="Paracetamol 500mg",
                generic_name="Acetaminophen",
                category=MedicineCategory.PAINKILLER,
                manufacturer="State Pharma",
                unit_price=5.00,
                stock_quantity=1000,
                status=MedicineStatus.IN_STOCK,
                description="Used for pain relief and fever reduction",
                expiry_date="2028-01-31"
            ),
            Medicine(
                id=5,
                name="Salbutamol 100mcg",
                generic_name="Salbutamol Sulfate",
                category=MedicineCategory.ANTIALLERGIC,
                manufacturer="Hemas Pharma",
                unit_price=350.00,
                stock_quantity=0,
                status=MedicineStatus.OUT_OF_STOCK,
                description="Inhaler used to treat asthma and COPD",
                expiry_date="2026-09-30"
            ),
        ]
        self.next_medicine_id = 6

        # ─── Mock Prescription Data ────────────────────────────────────────────
        self.prescriptions = [
            Prescription(
                id=1,
                patient_id=1,
                patient_name="Kasun Perera",
                doctor_id=1,
                doctor_name="Dr. Nuwan Rajapaksa",
                medicine_id=1,
                medicine_name="Metformin 500mg",
                dosage="1 tablet twice daily after meals",
                duration_days=30,
                quantity=60,
                total_price=930.00,
                prescribed_date="2026-03-25",
                status=PrescriptionStatus.DISPENSED,
                notes="Monitor blood sugar levels weekly"
            ),
            Prescription(
                id=2,
                patient_id=2,
                patient_name="Nimasha Fernando",
                doctor_id=2,
                doctor_name="Dr. Sandya Wickramasinghe",
                medicine_id=4,
                medicine_name="Paracetamol 500mg",
                dosage="1 tablet every 8 hours",
                duration_days=7,
                quantity=21,
                total_price=105.00,
                prescribed_date="2026-03-26",
                status=PrescriptionStatus.PENDING,
                notes="Take with food"
            ),
            Prescription(
                id=3,
                patient_id=3,
                patient_name="Ruwan Silva",
                doctor_id=1,
                doctor_name="Dr. Nuwan Rajapaksa",
                medicine_id=3,
                medicine_name="Atorvastatin 20mg",
                dosage="1 tablet once daily at night",
                duration_days=90,
                quantity=90,
                total_price=1980.00,
                prescribed_date="2026-03-20",
                status=PrescriptionStatus.DISPENSED,
                notes="Avoid grapefruit juice"
            ),
            Prescription(
                id=4,
                patient_id=4,
                patient_name="Dilani Jayawardena",
                doctor_id=4,
                doctor_name="Dr. Chathurika Senanayake",
                medicine_id=2,
                medicine_name="Amoxicillin 250mg",
                dosage="1 capsule three times daily",
                duration_days=5,
                quantity=15,
                total_price=131.25,
                prescribed_date="2026-03-27",
                status=PrescriptionStatus.PENDING,
                notes="Complete the full course"
            ),
            Prescription(
                id=5,
                patient_id=5,
                patient_name="Chamara Dissanayake",
                doctor_id=5,
                doctor_name="Dr. Asanka Madushanka",
                medicine_id=4,
                medicine_name="Paracetamol 500mg",
                dosage="2 tablets every 6 hours as needed",
                duration_days=3,
                quantity=24,
                total_price=120.00,
                prescribed_date="2026-03-28",
                status=PrescriptionStatus.ON_HOLD,
                notes="Post surgery pain management"
            ),
        ]
        self.next_prescription_id = 6

    # ─── Medicine CRUD ─────────────────────────────────────────────────────────
    def get_all_medicines(self):
        return self.medicines

    def get_medicine_by_id(self, medicine_id: int):
        return next((m for m in self.medicines if m.id == medicine_id), None)

    def get_medicines_by_category(self, category: MedicineCategory):
        return [m for m in self.medicines if m.category == category]

    def get_medicines_by_status(self, status: MedicineStatus):
        return [m for m in self.medicines if m.status == status]

    def get_in_stock_medicines(self):
        return [m for m in self.medicines if m.status == MedicineStatus.IN_STOCK]

    def add_medicine(self, medicine_data: MedicineCreate):
        new_medicine = Medicine(id=self.next_medicine_id, **medicine_data.dict())
        self.medicines.append(new_medicine)
        self.next_medicine_id += 1
        return new_medicine

    def update_medicine(self, medicine_id: int, medicine_data: MedicineUpdate):
        medicine = self.get_medicine_by_id(medicine_id)
        if medicine:
            update_data = medicine_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(medicine, key, value)
            return medicine
        return None

    def delete_medicine(self, medicine_id: int):
        medicine = self.get_medicine_by_id(medicine_id)
        if medicine:
            self.medicines.remove(medicine)
            return True
        return False

    # ─── Prescription CRUD ─────────────────────────────────────────────────────
    def get_all_prescriptions(self):
        return self.prescriptions

    def get_prescription_by_id(self, prescription_id: int):
        return next((p for p in self.prescriptions if p.id == prescription_id), None)

    def get_prescriptions_by_patient(self, patient_id: int):
        return [p for p in self.prescriptions if p.patient_id == patient_id]

    def get_prescriptions_by_doctor(self, doctor_id: int):
        return [p for p in self.prescriptions if p.doctor_id == doctor_id]

    def get_prescriptions_by_status(self, status: PrescriptionStatus):
        return [p for p in self.prescriptions if p.status == status]

    def add_prescription(self, prescription_data: PrescriptionCreate):
        new_prescription = Prescription(id=self.next_prescription_id, **prescription_data.dict())
        self.prescriptions.append(new_prescription)
        self.next_prescription_id += 1
        return new_prescription

    def update_prescription(self, prescription_id: int, prescription_data: PrescriptionUpdate):
        prescription = self.get_prescription_by_id(prescription_id)
        if prescription:
            update_data = prescription_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(prescription, key, value)
            return prescription
        return None

    def dispense_prescription(self, prescription_id: int):
        prescription = self.get_prescription_by_id(prescription_id)
        if prescription:
            prescription.status = PrescriptionStatus.DISPENSED
            return prescription
        return None

    def delete_prescription(self, prescription_id: int):
        prescription = self.get_prescription_by_id(prescription_id)
        if prescription:
            self.prescriptions.remove(prescription)
            return True
        return False
