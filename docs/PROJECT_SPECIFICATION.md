# ⚡ VoltFlow — Electricity Board Connection & Utility Service Management System
## Project Specification & Requirements Document

---

## 1. Executive Summary & Problem Definition

### 1.1 Problem Statement
State electricity distribution companies (Discoms / Electricity Boards) often struggle with manual, fragmented, and opaque processes for handling new electricity power connection requests, load sanctions, site technical feasibility audits, smart meter provisioning, and power grievance resolution. 

Consumers face delays, lack of tracking visibility, and cumbersome in-person visits to division sub-offices. Concurrently, Section Officers, Junior Engineers (JEs), and Field Linemen struggle with uncoordinated site inspection queues, transformer overload risks, and untracked service requests.

### 1.2 Solution: VoltFlow Platform
**VoltFlow** is an enterprise-grade, full-stack Electricity Board Connection & Utility Service Management Web Application. It unifies:
1. **Consumer Connection Lifecycle**: Online application submission for domestic, commercial, industrial, and agricultural electricity connections with load specifications and document verification.
2. **Field Inspection & Feasibility Auditing**: Engineering assessment of pole distance, transformer capacity, line clearances, and cost quotation estimation.
3. **Smart Meter Allocation & Grid Integration**: Meter serial number provisioning, initial reading calibration, phase configuration, and substation-feeder linking.
4. **Outage & Service Grievance Desk**: Rapid ticketing for power outages, voltage fluctuations, meter malfunctions, and safety hazards with priority dispatch.
5. **Real-time Grid & Operations Analytics**: Executive KPIs on total load sanctioned (MW), pending feasibility audits, active power meters, category breakdown, and SLA resolution timings.

---

## 2. Target Users & Stakeholders

| Role | Responsibilities & Use Cases |
| :--- | :--- |
| **Electricity Consumer / Applicant** | Applies for new connection, load enhancement, or category changes; tracks application status; reviews quotation estimate; logs outage grievances. |
| **Junior Engineer / Field Inspector** | Conducts technical site feasibility, checks transformer loading, measures pole distance, records inspection remarks, approves or rejects with technical justifications. |
| **Section Officer / Substation Superintendent** | Verifies consumer documentation, sanctions load (kW), issues cost quotations, assigns smart meter hardware, reviews division statistics. |
| **Lineman / Grid Maintenance Crew** | Assigned to outage grievances, diagnoses line faults, resolves power breakdowns, logs field resolution notes. |
| **Board Administrator / Chief Engineer** | Monitors regional grid KPIs, load distribution across consumer categories, revenue estimates, and SLA adherence. |

---

## 3. Scope of the System

### 3.1 In-Scope Features
- **Application Management (CRUD)**:
  - Submit new power connection application (Single Phase / Three Phase, 1 kW – 500 kW).
  - Search & filter by Application ID, applicant name, substation, tariff category, status, and date range.
  - View comprehensive application dossier with dynamic stage progression.
  - Update application details, modify load, update statuses.
  - Cancel/Archive applications with confirmation modals and cancellation audit tracking.
- **Technical Feasibility & Field Inspection**:
  - Assign field inspections to designated Junior Engineers.
  - Record pole distance (meters), nearest distribution transformer ID, available transformer capacity (kVA), line clearances, and meter box readiness.
  - Approve or Reject feasibility with engineering notes.
  - Auto-generate estimated connection quotation (Security deposit + service connection charges + meter cost).
- **Meter Provisioning & Grid Registry**:
  - Issue smart digital, prepaid, or solar net-meters with unique serial identifiers.
  - Assign to feeder lines and substations (e.g., North Substation 33/11kV).
  - Record baseline kWh readings and switch meter state to Active.
- **Power Outage & Grievance Resolution Desk**:
  - File grievance tickets (Total Outage, Voltage Surge, Sparking Wire, Meter Defect).
  - Assign priority (Critical, High, Medium, Low) and field crew.
  - Status progression (`Registered` → `In Progress` → `Resolved` → `Closed`).
- **Operational Analytics Dashboard**:
  - Live counts: Total Applications, Pending Feasibility, Active Meters, Sanctioned Load (kW/MW), Active Outages.
  - Tariff category distribution (Domestic LT-1, Commercial LT-2, Industrial HT-1, Agriculture LT-4).
  - Substation feeder health and inspection turnaround times.
- **Full REST API with Validation & Persistence**:
  - Pydantic v2 schemas for strict type safety.
  - SQLAlchemy ORM with SQLite (development) and PostgreSQL (production).
  - Automatic OpenAPI / Swagger UI docs (`/docs`).

---

## 4. Functional Requirements

### FR-1: Connection Application Workflow
- **FR-1.1**: System shall accept applications with applicant name, email, 10-digit mobile number, Aadhaar/ID, complete address, pincode, consumer category (`Domestic`, `Commercial`, `Industrial`, `Agricultural`), requested load in kW, phase (`Single Phase`, `Three Phase`), and premises ownership type (`Owned`, `Rented`).
- **FR-1.2**: System shall automatically generate a unique, non-repeating Application ID formatted as `APP-YYYY-XXXX` (e.g., `APP-2026-1042`).
- **FR-1.3**: System shall calculate an initial estimated quotation based on tariff category, load capacity, and phase charges.
- **FR-1.4**: System shall support full lifecycle transitions: `Submitted` → `Document_Verified` → `Field_Inspection_Scheduled` → `Inspection_Approved` → `Payment_Pending` → `Meter_Assigned_Active` (or `Rejected`).

### FR-2: Field Inspection & Feasibility Auditing
- **FR-2.1**: Officer can schedule inspection with target inspection date and assigned inspector name.
- **FR-2.2**: Inspector records distance from nearest pole (meters), transformer capacity, phase feasibility, line clearance, and feasibility status (`Feasible`, `Transformer_Upgrade_Required`, `Pole_Extension_Needed`, `Non_Feasible`).
- **FR-2.3**: System shall validate that distance $> 100m$ flags a pole extension requirement.

### FR-3: Meter Allocation & Provisioning
- **FR-3.1**: Board officer can assign a unique Meter Serial Number (e.g., `MTR-2026-XXXX`), meter type (`Smart Digital`, `Prepaid Digital`, `Solar Net-Meter`, `Bi-directional Three-Phase`), initial reading, and substation feeder code.
- **FR-3.2**: Assigning an active meter automatically transitions application status to `Meter_Assigned_Active`.

### FR-4: Outage & Grievance Management
- **FR-4.1**: Users can register outage and service complaints linked to consumer name or meter number.
- **FR-4.2**: System supports priority tagging (`Critical`, `High`, `Medium`, `Low`) and categorisation (`Power Outage`, `Voltage Fluctuation`, `Meter Defect`, `Hazardous Sparking`, `Billing Inquiry`).
- **FR-4.3**: Field team updates resolution notes and marks tickets as `Resolved` with resolution timestamps.

### FR-5: Search, Filter, Sort, Pagination
- **FR-5.1**: Server-side filtering by `status`, `category`, `substation`, `search` (multi-field keyword match across ID, name, phone, address).
- **FR-5.2**: Pagination with configurable page sizes (10, 25, 50) returning total count, pages, and current page.
- **FR-5.3**: Sorting by submission date, load, applicant name, and status.

---

## 5. Non-Functional Requirements

| Category | Requirement Specification |
| :--- | :--- |
| **Performance** | API response times $< 100\text{ms}$ for standard queries. Frontend initial load time $< 1.2\text{s}$. |
| **Scalability** | Clean separation of API, Services, and ORM repository layers allowing zero-friction migration from SQLite to PostgreSQL. |
| **Security** | Input validation on all endpoints using Pydantic, SQL injection prevention via parameterized ORM queries, XSS protection via HTML sanitization, CORS protection. |
| **Reliability** | Persistent SQL database with ACID transactional integrity and rollback on transaction failures. |
| **Usability & UX** | Responsive layout across mobile ($320\text{px}-480\text{px}$), tablet ($768\text{px}-1024\text{px}$), and desktop ($1280\text{px}+$); instant visual feedback via loaders, toast banners, modal dialogs, and clear empty states. |
| **Accessibility** | Semantic HTML5 elements (`<header>`, `<nav>`, `<main>`, `<section>`, `<dialog>`), keyboard navigation, high contrast UI tokens, and ARIA labels. |

---

## 6. Architecture & Technology Stack Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT BROWSER                           │
│     Vanilla HTML5 + Modern CSS3 + Modular JavaScript (ES6+) │
│     Responsive Grid / Modals / Toast Alerts / Fetch API     │
└──────────────────────────────┬──────────────────────────────┘
                               │ JSON REST Requests
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND (Python)                  │
│  ├── Routes (Applications, Inspections, Meters, Grievances) │
│  ├── Pydantic v2 Schemas (Validation & Serialization)       │
│  ├── Service Layer (Business Logic & Quotation Calc)        │
│  └── SQLAlchemy ORM (Data Layer & Session Management)       │
└──────────────────────────────┬──────────────────────────────┘
                               │ SQL Transactions
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   RELATIONAL SQL DATABASE                   │
│   SQLite (Local / Dev) ──► PostgreSQL (Production Ready)    │
│   Tables: consumers, applications, inspections, meters,     │
│           grievances, audit_logs                            │
└─────────────────────────────────────────────────────────────┘
```
