from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_plugins_endpoint():
    r = client.get("/plugins")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(p.get("name") == "customer_onboarding" for p in data)