# appointment-service/data_service.py
from models import Appointment, AppointmentCreate, AppointmentUpdate, AppointmentStatus, AppointmentType

class AppointmentDataService:
    def __init__(self):
        self.appointments = [
            Appointment(
                id=1,
                patient_id=1,
                patient_name="Kasun Perera",
                doctor_id=1,
                doctor_name="Dr. Nuwan Rajapaksa",
                appointment_date="2026-04-01",
                appointment_time="09:00 AM",
                appointment_type=AppointmentType.GENERAL_CHECKUP,
                status=AppointmentStatus.CONFIRMED,
                reason="Regular diabetes checkup",
                notes="Patient should bring previous reports"
            ),
            Appointment(
                id=2,
                patient_id=2,
                patient_name="Nimasha Fernando",
                doctor_id=2,
                doctor_name="Dr. Sandya Wickramasinghe",
                appointment_date="2026-04-02",
                appointment_time="10:30 AM",
                appointment_type=AppointmentType.CONSULTATION,
                status=AppointmentStatus.SCHEDULED,
                reason="Severe headaches and dizziness",
                notes="First time consultation"
            ),
            Appointment(
                id=3,
                patient_id=3,
                patient_name="Ruwan Silva",
                doctor_id=1,
                doctor_name="Dr. Nuwan Rajapaksa",
                appointment_date="2026-04-03",
                appointment_time="02:00 PM",
                appointment_type=AppointmentType.FOLLOW_UP,
                status=AppointmentStatus.SCHEDULED,
                reason="Blood pressure follow up",
                notes="Check medication effectiveness"
            ),
            Appointment(
                id=4,
                patient_id=4,
                patient_name="Dilani Jayawardena",
                doctor_id=4,
                doctor_name="Dr. Chathurika Senanayake",
                appointment_date="2026-03-28",
                appointment_time="11:00 AM",
                appointment_type=AppointmentType.GENERAL_CHECKUP,
                status=AppointmentStatus.COMPLETED,
                reason="Annual health checkup",
                notes="All results normal"
            ),
            Appointment(
                id=5,
                patient_id=5,
                patient_name="Chamara Dissanayake",
                doctor_id=5,
                doctor_name="Dr. Asanka Madushanka",
                appointment_date="2026-04-05",
                appointment_time="08:00 AM",
                appointment_type=AppointmentType.SURGERY,
                status=AppointmentStatus.CONFIRMED,
                reason="Appendix removal surgery",
                notes="Patient must fast 12 hours before surgery"
            ),
        ]
        self.next_id = 6

    def get_all_appointments(self):
        return self.appointments

    def get_appointment_by_id(self, appointment_id: int):
        return next((a for a in self.appointments if a.id == appointment_id), None)

    def get_appointments_by_patient(self, patient_id: int):
        return [a for a in self.appointments if a.patient_id == patient_id]

    def get_appointments_by_doctor(self, doctor_id: int):
        return [a for a in self.appointments if a.doctor_id == doctor_id]

    def get_appointments_by_status(self, status: AppointmentStatus):
        return [a for a in self.appointments if a.status == status]

    def get_appointments_by_date(self, date: str):
        return [a for a in self.appointments if a.appointment_date == date]

    def get_appointments_by_type(self, appointment_type: AppointmentType):
        return [a for a in self.appointments if a.appointment_type == appointment_type]

    def add_appointment(self, appointment_data: AppointmentCreate):
        new_appointment = Appointment(id=self.next_id, **appointment_data.dict())
        self.appointments.append(new_appointment)
        self.next_id += 1
        return new_appointment

    def update_appointment(self, appointment_id: int, appointment_data: AppointmentUpdate):
        appointment = self.get_appointment_by_id(appointment_id)
        if appointment:
            update_data = appointment_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(appointment, key, value)
            return appointment
        return None

    def cancel_appointment(self, appointment_id: int):
        appointment = self.get_appointment_by_id(appointment_id)
        if appointment:
            appointment.status = AppointmentStatus.CANCELLED
            return appointment
        return None

    def delete_appointment(self, appointment_id: int):
        appointment = self.get_appointment_by_id(appointment_id)
        if appointment:
            self.appointments.remove(appointment)
            return True
        return False
