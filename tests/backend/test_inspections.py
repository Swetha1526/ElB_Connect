# tests/backend/test_inspections.py
import pytest

def test_inspection_lifecycle(client):
    # 1. Create Application
    app_res = client.post("/api/v1/applications", json={
        "connection_type": "New Connection",
        "category": "Commercial",
        "requested_load_kw": 15.0,
        "phase": "Three Phase",
        "premises_type": "Owned",
        "substation_name": "Central Substation 33/11kV",
        "consumer": {
            "full_name": "Commercial Corp",
            "email": "corp@example.com",
            "phone": "9898989898",
            "national_id": "PAN-CORP1234K",
            "address": "Commercial Complex, 5th Main",
            "city": "Metro City",
            "pincode": "560001",
            "consumer_category": "Commercial"
        }
    })
    app_id = app_res.json()["id"]

    # 2. Schedule Inspection
    insp_res = client.post("/api/v1/inspections", json={
        "application_id": app_id,
        "inspector_name": "Er. Testing Inspector",
        "feasibility_status": "Feasible",
        "pole_distance_meters": 20.0,
        "transformer_id": "TR-TEST-01",
        "transformer_capacity_kva": 250.0,
        "meter_box_ready": True,
        "remarks": "Site inspection scheduled"
    })
    assert insp_res.status_code == 201
    insp_id = insp_res.json()["id"]

    # Verify application status shifted to Field_Inspection_Scheduled
    app_check = client.get(f"/api/v1/applications/{app_id}").json()
    assert app_check["status"] == "Field_Inspection_Scheduled"

    # 3. Complete Inspection with Feasible status
    comp_res = client.put(f"/api/v1/inspections/{insp_id}", json={
        "feasibility_status": "Feasible",
        "pole_distance_meters": 18.0,
        "remarks": "Feasibility approved. Low impedance feeder line."
    })
    assert comp_res.status_code == 200
    assert comp_res.json()["completed_at"] is not None

    # Verify application moved to Inspection_Approved
    app_approved = client.get(f"/api/v1/applications/{app_id}").json()
    assert app_approved["status"] == "Inspection_Approved"
    assert app_approved["sanctioned_load_kw"] == 15.0
