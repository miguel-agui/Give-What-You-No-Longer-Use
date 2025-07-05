from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/users/", json={"email": "test@example.com", "password": "secret"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
