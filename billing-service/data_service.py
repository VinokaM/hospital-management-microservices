# billing-service/data_service.py
from models import (
    Bill, BillCreate, BillUpdate, BillItem,
    Payment, PaymentCreate,
    PaymentStatus, PaymentMethod, ServiceType
)

class BillingDataService:
    def __init__(self):

        # ─── Mock Bill Data ────────────────────────────────────────────────────
        self.bills = [
            Bill(
                id=1,
                patient_id=1,
                patient_name="Kasun Perera",
                doctor_id=1,
                doctor_name="Dr. Nuwan Rajapaksa",
                appointment_id=1,
                bill_date="2026-03-25",
                due_date="2026-04-25",
                items=[
                    BillItem(
                        service_type=ServiceType.CONSULTATION,
                        description="Cardiology Consultation",
                        quantity=1,
                        unit_price=3500.00,
                        total_price=3500.00
                    ),
                    BillItem(
                        service_type=ServiceType.LAB_TEST,
                        description="Blood Sugar Test",
                        quantity=1,
                        unit_price=500.00,
                        total_price=500.00
                    ),
                    BillItem(
                        service_type=ServiceType.PHARMACY,
                        description="Metformin 500mg x60",
                        quantity=60,
                        unit_price=15.50,
                        total_price=930.00
                    ),
                ],
                subtotal=4930.00,
                discount=200.00,
                tax=473.00,
                total_amount=5203.00,
                paid_amount=5203.00,
                balance=0.00,
                payment_status=PaymentStatus.PAID,
                payment_method=PaymentMethod.CASH,
                notes="Full payment received"
            ),
            Bill(
                id=2,
                patient_id=2,
                patient_name="Nimasha Fernando",
                doctor_id=2,
                doctor_name="Dr. Sandya Wickramasinghe",
                appointment_id=2,
                bill_date="2026-03-26",
                due_date="2026-04-26",
                items=[
                    BillItem(
                        service_type=ServiceType.CONSULTATION,
                        description="Neurology Consultation",
                        quantity=1,
                        unit_price=4000.00,
                        total_price=4000.00
                    ),
                    BillItem(
                        service_type=ServiceType.PHARMACY,
                        description="Paracetamol 500mg x21",
                        quantity=21,
                        unit_price=5.00,
                        total_price=105.00
                    ),
                ],
                subtotal=4105.00,
                discount=0.00,
                tax=410.50,
                total_amount=4515.50,
                paid_amount=0.00,
                balance=4515.50,
                payment_status=PaymentStatus.PENDING,
                payment_method=None,
                notes="Payment pending"
            ),
            Bill(
                id=3,
                patient_id=3,
                patient_name="Ruwan Silva",
                doctor_id=1,
                doctor_name="Dr. Nuwan Rajapaksa",
                appointment_id=3,
                bill_date="2026-03-20",
                due_date="2026-04-20",
                items=[
                    BillItem(
                        service_type=ServiceType.CONSULTATION,
                        description="Cardiology Follow-up",
                        quantity=1,
                        unit_price=3500.00,
                        total_price=3500.00
                    ),
                    BillItem(
                        service_type=ServiceType.RADIOLOGY,
                        description="Chest X-Ray",
                        quantity=1,
                        unit_price=2500.00,
                        total_price=2500.00
                    ),
                    BillItem(
                        service_type=ServiceType.PHARMACY,
                        description="Atorvastatin 20mg x90",
                        quantity=90,
                        unit_price=22.00,
                        total_price=1980.00
                    ),
                ],
                subtotal=7980.00,
                discount=500.00,
                tax=748.00,
                total_amount=8228.00,
                paid_amount=5000.00,
                balance=3228.00,
                payment_status=PaymentStatus.PARTIALLY_PAID,
                payment_method=PaymentMethod.CREDIT_CARD,
                notes="Partial payment made via credit card"
            ),
            Bill(
                id=4,
                patient_id=4,
                patient_name="Dilani Jayawardena",
                doctor_id=4,
                doctor_name="Dr. Chathurika Senanayake",
                appointment_id=4,
                bill_date="2026-03-28",
                due_date="2026-04-28",
                items=[
                    BillItem(
                        service_type=ServiceType.CONSULTATION,
                        description="Pediatrics Consultation",
                        quantity=1,
                        unit_price=2500.00,
                        total_price=2500.00
                    ),
                    BillItem(
                        service_type=ServiceType.LAB_TEST,
                        description="Full Blood Count",
                        quantity=1,
                        unit_price=1500.00,
                        total_price=1500.00
                    ),
                ],
                subtotal=4000.00,
                discount=0.00,
                tax=400.00,
                total_amount=4400.00,
                paid_amount=4400.00,
                balance=0.00,
                payment_status=PaymentStatus.PAID,
                payment_method=PaymentMethod.INSURANCE,
                notes="Paid via health insurance"
            ),
            Bill(
                id=5,
                patient_id=5,
                patient_name="Chamara Dissanayake",
                doctor_id=5,
                doctor_name="Dr. Asanka Madushanka",
                appointment_id=5,
                bill_date="2026-03-28",
                due_date="2026-04-28",
                items=[
                    BillItem(
                        service_type=ServiceType.SURGERY,
                        description="Appendectomy Surgery",
                        quantity=1,
                        unit_price=75000.00,
                        total_price=75000.00
                    ),
                    BillItem(
                        service_type=ServiceType.ROOM_CHARGE,
                        description="Private Ward - 3 days",
                        quantity=3,
                        unit_price=8000.00,
                        total_price=24000.00
                    ),
                    BillItem(
                        service_type=ServiceType.NURSING,
                        description="Nursing Care - 3 days",
                        quantity=3,
                        unit_price=3000.00,
                        total_price=9000.00
                    ),
                    BillItem(
                        service_type=ServiceType.PHARMACY,
                        description="Post-surgery medications",
                        quantity=1,
                        unit_price=3500.00,
                        total_price=3500.00
                    ),
                ],
                subtotal=111500.00,
                discount=5000.00,
                tax=10650.00,
                total_amount=117150.00,
                paid_amount=0.00,
                balance=117150.00,
                payment_status=PaymentStatus.OVERDUE,
                payment_method=None,
                notes="Payment overdue - contact patient"
            ),
        ]
        self.next_bill_id = 6

        # ─── Mock Payment Data ─────────────────────────────────────────────────
        self.payments = [
            Payment(
                id=1,
                bill_id=1,
                patient_id=1,
                patient_name="Kasun Perera",
                amount_paid=5203.00,
                payment_method=PaymentMethod.CASH,
                payment_date="2026-03-25",
                transaction_id="TXN-2026-001",
                notes="Full payment in cash"
            ),
            Payment(
                id=2,
                bill_id=3,
                patient_id=3,
                patient_name="Ruwan Silva",
                amount_paid=5000.00,
                payment_method=PaymentMethod.CREDIT_CARD,
                payment_date="2026-03-21",
                transaction_id="TXN-2026-002",
                notes="Partial payment via credit card"
            ),
            Payment(
                id=3,
                bill_id=4,
                patient_id=4,
                patient_name="Dilani Jayawardena",
                amount_paid=4400.00,
                payment_method=PaymentMethod.INSURANCE,
                payment_date="2026-03-28",
                transaction_id="TXN-2026-003",
                notes="Insurance claim approved and paid"
            ),
        ]
        self.next_payment_id = 4

    # ─── Bill CRUD ─────────────────────────────────────────────────────────────
    def get_all_bills(self):
        return self.bills

    def get_bill_by_id(self, bill_id: int):
        return next((b for b in self.bills if b.id == bill_id), None)

    def get_bills_by_patient(self, patient_id: int):
        return [b for b in self.bills if b.patient_id == patient_id]

    def get_bills_by_doctor(self, doctor_id: int):
        return [b for b in self.bills if b.doctor_id == doctor_id]

    def get_bills_by_status(self, status: PaymentStatus):
        return [b for b in self.bills if b.payment_status == status]

    def get_bills_by_date(self, date: str):
        return [b for b in self.bills if b.bill_date == date]

    def add_bill(self, bill_data: BillCreate):
        new_bill = Bill(id=self.next_bill_id, **bill_data.dict())
        self.bills.append(new_bill)
        self.next_bill_id += 1
        return new_bill

    def update_bill(self, bill_id: int, bill_data: BillUpdate):
        bill = self.get_bill_by_id(bill_id)
        if bill:
            update_data = bill_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(bill, key, value)
            return bill
        return None

    def mark_bill_paid(self, bill_id: int, payment_method: PaymentMethod):
        bill = self.get_bill_by_id(bill_id)
        if bill:
            bill.payment_status = PaymentStatus.PAID
            bill.paid_amount = bill.total_amount
            bill.balance = 0.00
            bill.payment_method = payment_method
            return bill
        return None

    def delete_bill(self, bill_id: int):
        bill = self.get_bill_by_id(bill_id)
        if bill:
            self.bills.remove(bill)
            return True
        return False

    # ─── Payment CRUD ──────────────────────────────────────────────────────────
    def get_all_payments(self):
        return self.payments

    def get_payment_by_id(self, payment_id: int):
        return next((p for p in self.payments if p.id == payment_id), None)

    def get_payments_by_bill(self, bill_id: int):
        return [p for p in self.payments if p.bill_id == bill_id]

    def get_payments_by_patient(self, patient_id: int):
        return [p for p in self.payments if p.patient_id == patient_id]

    def add_payment(self, payment_data: PaymentCreate):
        new_payment = Payment(id=self.next_payment_id, **payment_data.dict())
        self.payments.append(new_payment)
        self.next_payment_id += 1
        return new_payment

    def delete_payment(self, payment_id: int):
        payment = self.get_payment_by_id(payment_id)
        if payment:
            self.payments.remove(payment)
            return True
        return False
