# 📡 VoltFlow REST API Documentation

Comprehensive guide to all REST endpoints exposed by the VoltFlow Electricity Board Management backend.

---

## Base URLs
- **Local Development**: `http://127.0.0.1:8000/api/v1`
- **Interactive Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc Documentation**: `http://127.0.0.1:8000/redoc`

---

## 1. System Health Endpoints

### `GET /health`
- **Description**: Returns live uptime and system status.
- **Status Code**: `200 OK`
- **Response**:
```json
{
  "status": "healthy",
  "service": "VoltFlow Electricity Board Management System",
  "version": "1.0.0",
  "environment": "development"
}
```

### `GET /api`
- **Description**: Returns API meta information and top-level resource links.
- **Status Code**: `200 OK`

---

## 2. Dashboard Analytics

### `GET /api/v1/stats/dashboard`
- **Description**: Returns real-time aggregate KPIs, tariff distributions, and live activity audit logs.
- **Status Code**: `200 OK`
- **Response Schema**:
```json
{
  "total_applications": 8,
  "pending_verifications": 1,
  "pending_inspections": 1,
  "pending_payments": 1,
  "active_meters": 2,
  "total_sanctioned_load_kw": 17.0,
  "total_sanctioned_load_mw": 0.017,
  "total_grievances": 3,
  "active_grievances": 2,
  "resolved_grievances": 1,
  "estimated_revenue_inr": 21100.0,
  "status_distribution": [
    { "status": "Meter_Assigned_Active", "count": 2 },
    { "status": "Payment_Pending", "count": 1 }
  ],
  "category_distribution": [
    { "category": "Domestic", "count": 3, "total_load_kw": 14.0 },
    { "category": "Commercial", "count": 3, "total_load_kw": 87.0 }
  ],
  "substation_metrics": [
    { "substation_name": "Central Substation 33/11kV", "total_applications": 2, "active_meters": 2, "total_load_kw": 17.0 }
  ],
  "recent_activity": []
}
```

---

## 3. Power Connection Applications

### `GET /api/v1/applications`
- **Description**: List applications with multi-field search, status filtering, and pagination.
- **Query Parameters**:
  - `search` *(string, optional)*: Match ID, name, phone, address.
  - `status` *(string, optional)*: Filter by `Submitted`, `Document_Verified`, `Field_Inspection_Scheduled`, `Inspection_Approved`, `Payment_Pending`, `Meter_Assigned_Active`, `Rejected`.
  - `category` *(string, optional)*: `Domestic`, `Commercial`, `Industrial`, `Agricultural`.
  - `substation` *(string, optional)*: Substation name.
  - `page` *(int, default=1)*: Page index.
  - `page_size` *(int, default=10, max=100)*: Items per page.
  - `sort_by` *(string, default="created_at")*: Sort attribute.
  - `sort_order` *(string, default="desc")*: `asc` or `desc`.
- **Status Code**: `200 OK`

### `GET /api/v1/applications/{id_or_number}`
- **Description**: Retrieve application dossier by integer database ID or application tracking string (e.g. `APP-2026-1001`).
- **Status Code**: `200 OK` / `404 Not Found`

### `POST /api/v1/applications`
- **Description**: Submit a new electricity connection request. Automatically calculates quotation demand note.
- **Status Code**: `201 Created` / `422 Validation Error`
- **Request Body**:
```json
{
  "connection_type": "New Connection",
  "category": "Domestic",
  "requested_load_kw": 5.0,
  "phase": "Single Phase",
  "premises_type": "Owned",
  "substation_name": "Central Substation 33/11kV",
  "remarks": "Near Community Center",
  "consumer": {
    "full_name": "Rajesh Kumar",
    "email": "rajesh@example.com",
    "phone": "9876543210",
    "national_id": "AADHAAR-1234-5678",
    "address": "Flat 101, Sunshine Heights",
    "city": "Metro City",
    "pincode": "110001",
    "consumer_category": "Domestic"
  }
}
```

### `PUT /api/v1/applications/{application_id}`
- **Description**: Update application status, sanctioned load, quotation amount, or demand note payment status.
- **Status Code**: `200 OK`
- **Request Body**:
```json
{
  "status": "Document_Verified",
  "sanctioned_load_kw": 5.0,
  "action_note": "Aadhaar and property tax receipt verified by Section Officer.",
  "performed_by": "Er. Suresh V"
}
```

### `DELETE /api/v1/applications/{application_id}`
- **Description**: Cancel and delete an application.
- **Status Code**: `200 OK`

---

## 4. Field Inspections & Feasibility Audits

### `GET /api/v1/inspections`
- **Description**: List all site feasibility surveys.
- **Status Code**: `200 OK`

### `POST /api/v1/inspections`
- **Description**: Schedule a field inspection for an application.
- **Status Code**: `201 Created`
- **Request Body**:
```json
{
  "application_id": 3,
  "inspector_name": "Er. Ramesh Kulkarni (JE-South)",
  "feasibility_status": "Feasible",
  "pole_distance_meters": 22.5,
  "transformer_id": "TR-CENTRAL-04",
  "transformer_capacity_kva": 250.0,
  "meter_box_ready": true,
  "remarks": "Three-phase pole extension clear."
}
```

### `PUT /api/v1/inspections/{inspection_id}`
- **Description**: Record survey measurements and update feasibility outcome (`Feasible`, `Pole_Extension_Needed`, `Non_Feasible`).
- **Status Code**: `200 OK`

---

## 5. Smart Meters & Grid Registry

### `GET /api/v1/meters`
- **Description**: List all smart energy meters in the grid registry. Filter by status (`Active`, `Suspended`).
- **Status Code**: `200 OK`

### `POST /api/v1/meters`
- **Description**: Provision and energize a new smart meter for an approved application.
- **Status Code**: `201 Created`
- **Request Body**:
```json
{
  "application_id": 2,
  "meter_serial_number": "MTR-2026-9042",
  "meter_type": "Smart Digital",
  "phase": "Three Phase",
  "initial_reading_kwh": 0.0,
  "substation_name": "Tech Park Substation 66/11kV",
  "feeder_line": "Feeder-11kV-TechZone",
  "status": "Active"
}
```

### `PUT /api/v1/meters/{meter_id}`
- **Description**: Update meter readings or status.
- **Status Code**: `200 OK`

---

## 6. Power Outage & Service Grievances

### `GET /api/v1/grievances`
- **Description**: List consumer grievance tickets. Filter by `status` or `priority`.
- **Status Code**: `200 OK`

### `POST /api/v1/grievances/public`
- **Description**: Self-service consumer complaint logging.
- **Status Code**: `201 Created`
- **Request Body**:
```json
{
  "full_name": "Kiran Patel",
  "phone": "9812345678",
  "email": "kiran@example.com",
  "address": "Sector 14, Main Road",
  "category": "Power Outage",
  "priority": "High",
  "description": "Transformer spark followed by blackout in Street 4."
}
```

### `PUT /api/v1/grievances/{grievance_id}`
- **Description**: Assign lineman or record resolution notes and mark resolved.
- **Status Code**: `200 OK`
