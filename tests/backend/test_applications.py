# tests/backend/test_applications.py
import pytest

def test_create_and_get_application(client):
    payload = {
        "connection_type": "New Connection",
        "category": "Domestic",
        "requested_load_kw": 4.5,
        "phase": "Single Phase",
        "premises_type": "Owned",
        "substation_name": "Central Substation 33/11kV",
        "remarks": "Residential electrification",
        "consumer": {
            "full_name": "Test Applicant",
            "email": "applicant@test.com",
            "phone": "9876500001",
            "national_id": "AADHAAR-1234-5678",
            "address": "123 Test Street",
            "city": "Metro City",
            "pincode": "110001",
            "consumer_category": "Domestic"
        }
    }

    # CREATE
    response = client.post("/api/v1/applications", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["application_number"].startswith("APP-")
    assert data["status"] == "Submitted"
    assert data["quotation_amount"] > 0
    assert data["consumer"]["full_name"] == "Test Applicant"
    app_id = data["id"]
    app_num = data["application_number"]

    # READ BY ID
    get_res = client.get(f"/api/v1/applications/{app_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == app_id

    # READ BY APP NUMBER
    get_num_res = client.get(f"/api/v1/applications/{app_num}")
    assert get_num_res.status_code == 200
    assert get_num_res.json()["application_number"] == app_num

    # UPDATE
    update_payload = {
        "status": "Document_Verified",
        "sanctioned_load_kw": 4.5,
        "action_note": "Aadhaar verified successfully",
        "performed_by": "Er. Testing Officer"
    }
    put_res = client.put(f"/api/v1/applications/{app_id}", json=update_payload)
    assert put_res.status_code == 200
    assert put_res.json()["status"] == "Document_Verified"
    assert len(put_res.json()["audit_logs"]) >= 2

    # SEARCH & LIST
    list_res = client.get("/api/v1/applications?search=Test Applicant")
    assert list_res.status_code == 200
    list_data = list_res.json()
    assert list_data["total"] >= 1
    assert any(item["id"] == app_id for item in list_data["items"])

    # DELETE
    del_res = client.delete(f"/api/v1/applications/{app_id}")
    assert del_res.status_code == 200

    # VERIFY 404 AFTER DELETE
    verify_res = client.get(f"/api/v1/applications/{app_id}")
    assert verify_res.status_code == 404

def test_application_validation_errors(client):
    # Invalid load (negative or zero)
    payload = {
        "connection_type": "New Connection",
        "category": "Domestic",
        "requested_load_kw": -5.0,
        "phase": "Single Phase",
        "premises_type": "Owned",
        "substation_name": "Central Substation 33/11kV",
        "consumer": {
            "full_name": "A",
            "email": "not-an-email",
            "phone": "123",
            "national_id": "1",
            "address": "X",
            "city": "C",
            "pincode": "1",
            "consumer_category": "Domestic"
        }
    }
    response = client.post("/api/v1/applications", json=payload)
    assert response.status_code == 422
