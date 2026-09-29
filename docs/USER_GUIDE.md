# 📖 VoltFlow User Guide & Demonstration Manual

A practical, role-by-role guide to using and demonstrating the VoltFlow Electricity Board Connection & Utility Service Platform.

---

## 1. Consumer Journey: Applying for Power Connection

1. Click the **⚡ Apply New Connection** button in the header or on the Power Applications page.
2. Fill in the **Applicant Identity & Premises** details (Name, Contact Email, 10-digit Phone, Aadhaar/National ID, Address, PIN code).
3. Select your **Connection Specifications**:
   - **Tariff Category**: Domestic (LT-1), Commercial (LT-2), Industrial (HT-1), or Agricultural (LT-4).
   - **Requested Load (kW)**: e.g. 5.0 kW for homes, 30.0 kW for commercial clinics.
   - **Phase**: Single Phase (230V) or Three Phase (415V).
   - **Premises Ownership**: Owned or Rented.
   - **Target Substation**: Choose the nearest local substation.
4. Note that the **Dynamic Estimated Quotation Demand Note** computes the exact security deposit, service fee, and meter cost in real time.
5. Click **Submit Application**.
6. A success notification will display your tracking number (e.g., `APP-2026-1009`).

---

## 2. Consumer Journey: Tracking an Application

1. Click **Track Application** in the sidebar.
2. Enter your Application Number (e.g., `APP-2026-1001` or `APP-2026-1002`).
3. Click **🔍 Track Application**.
4. View your real-time stage progress tracker:
   - `Submitted` ➔ `Doc Verified` ➔ `Field Inspection` ➔ `Approved` ➔ `Payment Pending` ➔ `Meter Active`.
5. Check your demand note quotation details and energized smart meter serial.
6. Click **🖨️ Print Application Dossier** for a clean, print-ready document.

---

## 3. Section Officer Journey: Document Verification & Load Sanction

1. Open **Power Applications** from the sidebar.
2. Use the search bar or status dropdown to find newly submitted applications.
3. Click **👁️ View** to review the complete application dossier and historical audit trail.
4. Click **⚙️ Action** to open the management modal:
   - Advance status (e.g. from `Submitted` to `Document_Verified` or `Payment_Pending`).
   - Sanction the load (kW) and update payment status.
   - Add an audit note explaining the decision.
5. Click **Save & Record Action**. The audit timeline automatically records your entry.

---

## 4. Junior Engineer (JE) Journey: Site Feasibility Surveys

1. Navigate to **Field Feasibility Audits**.
2. Click **+ Schedule Field Survey** to assign an engineer to a pending application.
3. Once the site inspection is conducted, click **📝 Record Survey**:
   - Enter measured pole distance (meters).
   - Enter distribution transformer code and capacity (kVA).
   - Check meter box readiness.
   - Mark Feasibility Outcome as **Feasible**, **Pole Extension Needed**, or **Non-Feasible**.
4. Click **Save Survey Findings**. If marked Feasible, the application is automatically transitioned to `Inspection_Approved`.

---

## 5. Superintendent Journey: Allocating Smart Meters

1. Navigate to **Smart Meter Registry**.
2. Click **⚡ Allocate & Energize Meter**.
3. Enter the Application ID, select meter type (Smart Digital, Prepaid, Solar Net-Meter), phase, substation, and feeder line.
4. Click **Allocate & Energize**. The meter is commissioned in the grid registry, and the application status is promoted to `Meter_Assigned_Active`.

---

## 6. Grievance Desk Journey: Logging & Resolving Outages

1. Click **⚠️ Report Outage** or open **Outage Grievance Desk**.
2. File a complaint with incident category (Total Power Outage, Voltage Surge, Sparking Wire, Meter Defect) and priority (Critical, High, Medium, Low).
3. Linemen / Section Officers can click **🛠️ Action / Resolve** to assign emergency crews, log repair details, and mark the ticket **Resolved**.
