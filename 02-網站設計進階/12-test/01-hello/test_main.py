from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World"}

def test_create_item():
    payload = {"name": "Test Item", "price": 10.99}
    response = client.post("/items/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"item": payload}
