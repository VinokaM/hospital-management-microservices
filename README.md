# 🏥 Hospital Management System - Microservices

## Project Structure
```
hospital-management/
│
├── requirements.txt
│
├── gateway/                    ← API Gateway  (Port 8000)
│   └── main.py
│
├── patient-service/            ← Member 1     (Port 8001)
│   ├── models.py
│   ├── data_service.py
│   ├── service.py
│   └── main.py
│
├── doctor-service/             ← Member 2     (Port 8002)
│   ├── models.py
│   ├── data_service.py
│   ├── service.py
│   └── main.py
│
├── appointment-service/        ← Member 3     (Port 8003)
│   ├── models.py
│   ├── data_service.py
│   ├── service.py
│   └── main.py
│
├── pharmacy-service/           ← Member 4     (Port 8004)
│   ├── models.py
│   ├── data_service.py
│   ├── service.py
│   └── main.py
│
└── billing-service/            ← Member 5     (Port 8005)
    ├── models.py
    ├── data_service.py
    ├── service.py
    └── main.py
```

---

## Setup

### Step 1 - Create virtual environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### Step 2 - Install packages
```bash
pip install -r requirements.txt
```

---

## Running All Services (6 Terminals)

| Terminal | Command | Port | Swagger |
|----------|---------|------|---------|
| 1 | `cd patient-service && uvicorn main:app --reload --port 8001` | 8001 | http://localhost:8001/docs |
| 2 | `cd doctor-service && uvicorn main:app --reload --port 8002` | 8002 | http://localhost:8002/docs |
| 3 | `cd appointment-service && uvicorn main:app --reload --port 8003` | 8003 | http://localhost:8003/docs |
| 4 | `cd pharmacy-service && uvicorn main:app --reload --port 8004` | 8004 | http://localhost:8004/docs |
| 5 | `cd billing-service && uvicorn main:app --reload --port 8005` | 8005 | http://localhost:8005/docs |
| 6 | `cd gateway && uvicorn main:app --reload --port 8000` | 8000 | http://localhost:8000/docs |

---

## Using the Gateway

### Step 1 - Login
```
POST http://localhost:8000/auth/login
username: admin
password: hospital2026
```

### Step 2 - Copy the token from response

### Step 3 - Authorize in Swagger
1. Go to http://localhost:8000/docs
2. Click the Authorize button (lock icon)
3. Enter: Bearer <your_token>
4. Click Authorize

### Step 4 - Now access all services through gateway
- Patients:      /gateway/patients
- Doctors:       /gateway/doctors
- Appointments:  /gateway/appointments
- Medicines:     /gateway/medicines
- Prescriptions: /gateway/prescriptions
- Bills:         /gateway/bills
- Payments:      /gateway/payments
