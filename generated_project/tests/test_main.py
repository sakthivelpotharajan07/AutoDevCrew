from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the cloth shopping dashboard"}

def test_get_categories():
    response = client.get("/categories")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1