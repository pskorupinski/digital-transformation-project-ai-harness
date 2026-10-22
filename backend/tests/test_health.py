def test_health_reports_ok_and_integrations_mode(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "integrations_mode": "fake"}
