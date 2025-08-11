from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_and_login():
    # register
    r = client.post("/auth/register", json={"email": "test@example.com", "password": "secret"})
    assert r.status_code in (200, 400)  # allow reruns

    # login
    r = client.post("/auth/login", data={"username": "test@example.com", "password": "secret"})
    assert r.status_code == 200
    token = r.json().get("access_token")
    assert token

    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200