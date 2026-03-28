# patient-service/data_service.py
from models import Patient, PatientCreate, PatientUpdate, BloodGroup, Gender

class PatientDataService:
    def __init__(self):
        self.patients = [
            Patient(
                id=1,
                first_name="Kasun",
                last_name="Perera",
                age=35,
                gender=Gender.MALE,
                blood_group=BloodGroup.A_POS,
                phone="0771234567",
                email="kasun.perera@email.com",
                address="123 Galle Road, Colombo 03",
                medical_history="Diabetes Type 2"
            ),
            Patient(
                id=2,
                first_name="Nimasha",
                last_name="Fernando",
                age=28,
                gender=Gender.FEMALE,
                blood_group=BloodGroup.B_POS,
                phone="0779876543",
                email="nimasha.fernando@email.com",
                address="45 Kandy Road, Kegalle",
                medical_history="Asthma"
            ),
            Patient(
                id=3,
                first_name="Ruwan",
                last_name="Silva",
                age=52,
                gender=Gender.MALE,
                blood_group=BloodGroup.O_POS,
                phone="0712345678",
                email="ruwan.silva@email.com",
                address="78 Marine Drive, Galle",
                medical_history="Hypertension"
            ),
            Patient(
                id=4,
                first_name="Dilani",
                last_name="Jayawardena",
                age=42,
                gender=Gender.FEMALE,
                blood_group=BloodGroup.AB_NEG,
                phone="0765432109",
                email="dilani.j@email.com",
                address="12 Temple Road, Kandy",
                medical_history="None"
            ),
            Patient(
                id=5,
                first_name="Chamara",
                last_name="Dissanayake",
                age=19,
                gender=Gender.MALE,
                blood_group=BloodGroup.A_NEG,
                phone="0756789012",
                email="chamara.d@email.com",
                address="56 Negombo Road, Kurunegala",
                medical_history="None"
            ),
        ]
        self.next_id = 6

    def get_all_patients(self):
        return self.patients

    def get_patient_by_id(self, patient_id: int):
        return next((p for p in self.patients if p.id == patient_id), None)

    def get_patients_by_blood_group(self, blood_group: BloodGroup):
        return [p for p in self.patients if p.blood_group == blood_group]

    def get_patients_by_gender(self, gender: Gender):
        return [p for p in self.patients if p.gender == gender]

    def add_patient(self, patient_data: PatientCreate):
        new_patient = Patient(id=self.next_id, **patient_data.dict())
        self.patients.append(new_patient)
        self.next_id += 1
        return new_patient

    def update_patient(self, patient_id: int, patient_data: PatientUpdate):
        patient = self.get_patient_by_id(patient_id)
        if patient:
            update_data = patient_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(patient, key, value)
            return patient
        return None

    def delete_patient(self, patient_id: int):
        patient = self.get_patient_by_id(patient_id)
        if patient:
            self.patients.remove(patient)
            return True
        return False
