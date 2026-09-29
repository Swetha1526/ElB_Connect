# ⚡ VoltFlow — Electricity Board Connection & Utility Service Management System

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI_v0.110+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.14-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy_v2.0-D71F00?style=flat&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org)
[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)](https://sqlite.org)
[![Tests](https://img.shields.io/badge/Tests-100%25%20Passing-brightgreen?style=flat&logo=pytest&logoColor=white)](https://docs.pytest.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**VoltFlow** is an enterprise-grade, production-quality full-stack web application designed for state electricity distribution companies (DISCOMs / Electricity Boards) and power utility corporations. It provides an end-to-end digital lifecycle for power connection applications, engineering feasibility surveys, smart meter grid allocations, power outage grievances, and live telemetry analytics.

---

## 🌟 Key Features

1. **⚡ Full Connection Lifecycle Management (CRUD)**:
   - Apply for Domestic (LT-1), Commercial (LT-2), Industrial (HT-1), and Agricultural (LT-4) connections.
   - Dynamic real-time quotation demand note calculation (Security deposit + service connection charge + meter fee).
   - Multi-field search, status filtering, tariff filtering, substation filtering, and server-side pagination.
   - Stage progression: `Submitted` ➔ `Document_Verified` ➔ `Field_Inspection_Scheduled` ➔ `Inspection_Approved` ➔ `Payment_Pending` ➔ `Meter_Assigned_Active`.

2. **📋 Field Feasibility Auditing**:
   - Junior Engineer (JE) inspection records: pole distance measurements, transformer capacity (kVA), line clearance, and meter box readiness.
   - Automated feasibility evaluation (`Feasible`, `Pole_Extension_Needed`, `Non_Feasible`).

3. **⚡ Smart Meter Registry & Grid Allocation**:
   - Hardware serial provisioning (`MTR-YYYY-XXXX`), phase mapping (Single Phase / Three Phase), and 11kV feeder line assignment.
   - Baseline calibration and continuous energy reading tracker (kWh).

4. **⚠️ Power Outage & Grievance Desk**:
   - Consumer complaint ticketing for total blackouts, voltage surges, sparking hazards, and billing inquiries.
   - Priority tagging (`Critical`, `High`, `Medium`, `Low`), lineman dispatch, and resolution tracking.

5. **🔍 Consumer Self-Service Tracking**:
   - Fast lookup by Application Number (e.g., `APP-2026-1001`) with visual step-by-step progress stepper and printable demand note preview.

6. **📊 Operations Analytics & Audit Trail**:
   - Real-time KPI statistics: Total Applications, Active Meters, Sanctioned Load (MW), Active Outages, and Revenue Collections.
   - Substation health matrix and tamper-evident audit logs.

---

## 🏗️ Architecture & Tech Stack

```
User (Browser)
      ↓
Frontend: HTML5 + Modern CSS3 + Vanilla JavaScript (ES6+ Fetch API)
      ↓ REST API (JSON)
FastAPI Backend (Python)
      ↓
Business Service Layer & Pydantic v2 Schemas
      ↓
SQLAlchemy ORM
      ↓
SQL Database (SQLite in Development / PostgreSQL in Production)
```

| Layer | Technology |
| :--- | :--- |
| **Frontend** | HTML5 Semantic, Modern CSS3 Design Tokens, Vanilla JavaScript ES6+, Fetch API |
| **Backend** | Python 3.11+, FastAPI, Pydantic v2, Uvicorn ASGI Server |
| **Data Layer** | SQLAlchemy 2.0 ORM, SQLite (Dev), PostgreSQL (Production) |
| **Testing** | Pytest, Pytest-Asyncio, FastAPI TestClient / HTTPX |
| **Deployment** | Docker, Docker Compose, Render / Railway (Backend), Vercel / Netlify (Frontend) |

---

## 📁 Project Directory Structure

```text
mini_proj13/
├── frontend/
│   ├── index.html              # Master SPA shell
│   ├── css/
│   │   ├── style.css           # Premium cyber-dark design system
│   │   └── responsive.css      # Mobile, tablet, and print media queries
│   ├── js/
│   │   ├── config.js           # Endpoint resolution & constants
│   │   ├── api.js              # Centralized Fetch API client
│   │   ├── ui.js               # Modals, toasts, formatters & badges
│   │   └── app.js              # App state, event listeners, view controllers
│   └── assets/
│       └── logo.svg            # VoltFlow branding
│
├── backend/
│   ├── app/
│   │   ├── main.py             # FastAPI entrypoint, middleware, static mount
│   │   ├── config.py           # Configuration & CORS settings
│   │   ├── models/             # SQLAlchemy ORM models (6 tables)
│   │   ├── schemas/            # Pydantic v2 validation models
│   │   ├── database/           # Engine, session, and seed scripts
│   │   ├── services/           # Business logic layer
│   │   ├── routes/             # REST API routers
│   │   └── utils/              # Quotation calculators & ID generators
│   ├── requirements.txt        # Pinned Python dependencies
│   ├── .env.example            # Environment template
│   └── README.md
│
├── database/
│   ├── schema.sql              # Raw SQL DDL schema
│   └── seed.sql                # Realistic initial electricity board dataset
│
├── tests/
│   ├── conftest.py             # Pytest in-memory DB fixture
│   └── backend/                # Automated API test suite (7 tests)
│
├── docs/
│   ├── PROJECT_SPECIFICATION.md
│   ├── ARCHITECTURE.md
│   ├── DATABASE.md
│   ├── API_DOCUMENTATION.md
│   ├── DEPLOYMENT.md
│   └── USER_GUIDE.md
│
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## ⚡ Quick Start & Local Development

### 1. Prerequisites
- Python 3.10+ installed
- Git

### 2. Clone & Setup
```bash
# Navigate to project directory
cd mini_proj13

# Create & activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 3. Initialize & Seed Database
```bash
python backend/app/database/seed_data.py --force
```

### 4. Run the Full-Stack Server
```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

Open your browser at:
- **Application Portal**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Running Automated Tests

Run the complete backend test suite:
```bash
pytest tests/ -v
```

Output:
```text
tests/backend/test_applications.py::test_create_and_get_application PASSED [ 14%]
tests/backend/test_applications.py::test_application_validation_errors PASSED [ 28%]
tests/backend/test_grievances.py::test_grievance_workflow PASSED         [ 42%]
tests/backend/test_health.py::test_health_check PASSED                   [ 57%]
tests/backend/test_health.py::test_api_info PASSED                       [ 71%]
tests/backend/test_inspections.py::test_inspection_lifecycle PASSED      [ 85%]
tests/backend/test_meters.py::test_meter_allocation_and_readings PASSED  [100%]
======================== 7 passed in 0.33s =========================
```

---

## 🐳 Docker Deployment

Build and run using Docker Compose:
```bash
docker-compose up -d --build
```
Access the application at `http://localhost:8000`.

---

## 🎬 5-Minute Demonstration Walkthrough

1. **Dashboard Telemetry**: Open [http://127.0.0.1:8000](http://127.0.0.1:8000), review real-time KPI counters, load distribution bars, and live audit timeline.
2. **Submit New Application**: Click **⚡ Apply New Connection**, fill in applicant info and requested load (e.g. 30 kW Commercial). Note the dynamic quotation calculation updates to ₹36,700 in real time. Submit and observe the toast notification and table update.
3. **Inspect Application Dossier**: Click **👁️ View** on an application to demonstrate the visual stage stepper, technical specs, and chronological audit trail.
4. **Action / Load Sanction**: Click **⚙️ Action**, advance status to `Inspection_Approved`, sanction load, and observe audit trail persistence.
5. **Field Feasibility Survey**: Open **Field Feasibility Audits**, click **📝 Record Survey**, record pole distance and transformer capacity.
6. **Smart Meter Allocation**: Open **Smart Meter Registry**, click **⚡ Allocate & Energize Meter**, assign hardware serial and feeder line.
7. **Outage Grievance Desk**: Open **Outage Grievance Desk**, log a power breakdown ticket with High priority, assign a lineman crew, and mark it resolved.
8. **Consumer Self-Service**: Open **Track Application**, search `APP-2026-1001` to show the applicant status view and print-ready dossier.
9. **Interactive API Docs**: Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to demonstrate OpenAPI Swagger documentation.

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
