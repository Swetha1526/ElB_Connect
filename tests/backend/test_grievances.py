# tests/backend/test_grievances.py
import pytest

def test_grievance_workflow(client):
    # 1. Create Public Grievance
    payload = {
        "full_name": "Grievance Reporter",
        "phone": "9887766554",
        "email": "reporter@example.com",
        "address": "Block C, Metro City",
        "category": "Power Outage",
        "priority": "High",
        "description": "Total blackout in sector for past 2 hours."
    }
    create_res = client.post("/api/v1/grievances/public", json=payload)
    assert create_res.status_code == 201
    grv_data = create_res.json()
    assert grv_data["grievance_number"].startswith("GRV-")
    assert grv_data["status"] == "Registered"
    grv_id = grv_data["id"]

    # 2. Assign Lineman
    assign_res = client.put(f"/api/v1/grievances/{grv_id}", json={
        "status": "In_Progress",
        "assigned_lineman": "Lineman Vijay Kumar",
        "resolution_notes": "Lineman dispatched to distribution box."
    })
    assert assign_res.status_code == 200
    assert assign_res.json()["status"] == "In_Progress"
    assert assign_res.json()["assigned_lineman"] == "Lineman Vijay Kumar"

    # 3. Resolve Grievance
    resolve_res = client.put(f"/api/v1/grievances/{grv_id}", json={
        "status": "Resolved",
        "resolution_notes": "Blown fuse replaced in distribution pillar box. Supply restored."
    })
    assert resolve_res.status_code == 200
    assert resolve_res.json()["status"] == "Resolved"
    assert resolve_res.json()["resolved_at"] is not None

    # 4. List Grievances with filter
    list_res = client.get("/api/v1/grievances?status=Resolved")
    assert list_res.status_code == 200
    assert any(g["id"] == grv_id for g in list_res.json())
