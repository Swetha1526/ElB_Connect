# tests/backend/test_health.py
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "VoltFlow" in data["service"]

def test_api_info(client):
    response = client.get("/api")
    assert response.status_code == 200
    data = response.json()
    assert "documentation" in data
    assert "/docs" in data["documentation"]
