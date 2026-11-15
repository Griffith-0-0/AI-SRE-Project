from fastapi.testclient import TestClient

from demo_app.gateway.main import app

client = TestClient(app)


def test_gateway_health_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "gateway"}
