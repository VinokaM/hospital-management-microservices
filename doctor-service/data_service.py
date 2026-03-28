# doctor-service/data_service.py
from models import Doctor, DoctorCreate, DoctorUpdate, Specialization, Availability, Gender

class DoctorDataService:
    def __init__(self):
        self.doctors = [
            Doctor(
                id=1,
                first_name="Nuwan",
                last_name="Rajapaksa",
                age=45,
                gender=Gender.MALE,
                specialization=Specialization.CARDIOLOGY,
                phone="0771111111",
                email="nuwan.rajapaksa@hospital.com",
                qualification="MBBS, MD (Cardiology)",
                experience_years=18,
                availability=Availability.AVAILABLE,
                consultation_fee=3500.00
            ),
            Doctor(
                id=2,
                first_name="Sandya",
                last_name="Wickramasinghe",
                age=38,
                gender=Gender.FEMALE,
                specialization=Specialization.NEUROLOGY,
                phone="0772222222",
                email="sandya.w@hospital.com",
                qualification="MBBS, MD (Neurology)",
                experience_years=12,
                availability=Availability.AVAILABLE,
                consultation_fee=4000.00
            ),
            Doctor(
                id=3,
                first_name="Pradeep",
                last_name="Gunasekara",
                age=50,
                gender=Gender.MALE,
                specialization=Specialization.ORTHOPEDICS,
                phone="0773333333",
                email="pradeep.g@hospital.com",
                qualification="MBBS, MS (Orthopedics)",
                experience_years=22,
                availability=Availability.ON_LEAVE,
                consultation_fee=3000.00
            ),
            Doctor(
                id=4,
                first_name="Chathurika",
                last_name="Senanayake",
                age=35,
                gender=Gender.FEMALE,
                specialization=Specialization.PEDIATRICS,
                phone="0774444444",
                email="chathurika.s@hospital.com",
                qualification="MBBS, DCH",
                experience_years=8,
                availability=Availability.AVAILABLE,
                consultation_fee=2500.00
            ),
            Doctor(
                id=5,
                first_name="Asanka",
                last_name="Madushanka",
                age=42,
                gender=Gender.MALE,
                specialization=Specialization.SURGERY,
                phone="0775555555",
                email="asanka.m@hospital.com",
                qualification="MBBS, MS (Surgery)",
                experience_years=15,
                availability=Availability.UNAVAILABLE,
                consultation_fee=5000.00
            ),
        ]
        self.next_id = 6

    def get_all_doctors(self):
        return self.doctors

    def get_doctor_by_id(self, doctor_id: int):
        return next((d for d in self.doctors if d.id == doctor_id), None)

    def get_doctors_by_specialization(self, specialization: Specialization):
        return [d for d in self.doctors if d.specialization == specialization]

    def get_doctors_by_availability(self, availability: Availability):
        return [d for d in self.doctors if d.availability == availability]

    def get_available_doctors(self):
        return [d for d in self.doctors if d.availability == Availability.AVAILABLE]

    def add_doctor(self, doctor_data: DoctorCreate):
        new_doctor = Doctor(id=self.next_id, **doctor_data.dict())
        self.doctors.append(new_doctor)
        self.next_id += 1
        return new_doctor

    def update_doctor(self, doctor_id: int, doctor_data: DoctorUpdate):
        doctor = self.get_doctor_by_id(doctor_id)
        if doctor:
            update_data = doctor_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(doctor, key, value)
            return doctor
        return None

    def delete_doctor(self, doctor_id: int):
        doctor = self.get_doctor_by_id(doctor_id)
        if doctor:
            self.doctors.remove(doctor)
            return True
        return False
