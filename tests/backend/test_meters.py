# tests/backend/test_meters.py
import pytest

def test_meter_allocation_and_readings(client):
    # 1. Create Application
    app_res = client.post("/api/v1/applications", json={
        "connection_type": "New Connection",
        "category": "Domestic",
        "requested_load_kw": 5.0,
        "phase": "Single Phase",
        "premises_type": "Owned",
        "substation_name": "East Substation 33/11kV",
        "consumer": {
            "full_name": "Smart Meter Consumer",
            "email": "meter.consumer@example.com",
            "phone": "9812345678",
            "national_id": "AADHAAR-9999-1111",
            "address": "45 Smart Grid Lane",
            "city": "Metro City",
            "pincode": "110001",
            "consumer_category": "Domestic"
        }
    })
    app_id = app_res.json()["id"]

    # 2. Allocate Meter
    meter_res = client.post("/api/v1/meters", json={
        "application_id": app_id,
        "meter_type": "Smart Digital",
        "phase": "Single Phase",
        "initial_reading_kwh": 0.0,
        "current_reading_kwh": 0.0,
        "substation_name": "East Substation 33/11kV",
        "feeder_line": "Feeder-11kV-Residential",
        "status": "Active"
    })
    assert meter_res.status_code == 201
    meter_data = meter_res.json()
    assert meter_data["meter_serial_number"].startswith("MTR-")
    meter_id = meter_data["id"]

    # Verify Application is now Meter_Assigned_Active & Paid
    app_status = client.get(f"/api/v1/applications/{app_id}").json()
    assert app_status["status"] == "Meter_Assigned_Active"
    assert app_status["payment_status"] == "Paid"

    # 3. Update Meter Reading
    up_res = client.put(f"/api/v1/meters/{meter_id}", json={
        "current_reading_kwh": 250.5
    })
    assert up_res.status_code == 200
    assert up_res.json()["current_reading_kwh"] == 250.5

    # 4. List Meters
    list_res = client.get("/api/v1/meters?status=Active")
    assert list_res.status_code == 200
    assert any(m["id"] == meter_id for m in list_res.json())
