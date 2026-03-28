# billing-service/service.py
from data_service import BillingDataService
from models import (
    BillCreate, BillUpdate, PaymentCreate,
    PaymentStatus, PaymentMethod
)

class BillingService:
    def __init__(self):
        self.data_service = BillingDataService()

    # ─── Bill Methods ──────────────────────────────────────────────────────────
    def get_all_bills(self):
        return self.data_service.get_all_bills()

    def get_bill_by_id(self, bill_id: int):
        return self.data_service.get_bill_by_id(bill_id)

    def get_bills_by_patient(self, patient_id: int):
        return self.data_service.get_bills_by_patient(patient_id)

    def get_bills_by_doctor(self, doctor_id: int):
        return self.data_service.get_bills_by_doctor(doctor_id)

    def get_bills_by_status(self, status: PaymentStatus):
        return self.data_service.get_bills_by_status(status)

    def get_bills_by_date(self, date: str):
        return self.data_service.get_bills_by_date(date)

    def create_bill(self, bill_data: BillCreate):
        return self.data_service.add_bill(bill_data)

    def update_bill(self, bill_id: int, bill_data: BillUpdate):
        return self.data_service.update_bill(bill_id, bill_data)

    def mark_bill_paid(self, bill_id: int, payment_method: PaymentMethod):
        return self.data_service.mark_bill_paid(bill_id, payment_method)

    def delete_bill(self, bill_id: int):
        return self.data_service.delete_bill(bill_id)

    # ─── Payment Methods ───────────────────────────────────────────────────────
    def get_all_payments(self):
        return self.data_service.get_all_payments()

    def get_payment_by_id(self, payment_id: int):
        return self.data_service.get_payment_by_id(payment_id)

    def get_payments_by_bill(self, bill_id: int):
        return self.data_service.get_payments_by_bill(bill_id)

    def get_payments_by_patient(self, patient_id: int):
        return self.data_service.get_payments_by_patient(patient_id)

    def create_payment(self, payment_data: PaymentCreate):
        return self.data_service.add_payment(payment_data)

    def delete_payment(self, payment_id: int):
        return self.data_service.delete_payment(payment_id)
