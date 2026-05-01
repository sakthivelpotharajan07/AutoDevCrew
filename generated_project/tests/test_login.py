import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_page():
    response = client.get("/login")
    assert response.status_code == 200

def test_login_success():
    response = client.post("/login", data={"username": "test", "password": "test"})
    assert response.status_code == 200

def test_login_failure():
    response = client.post("/login", data={"username": "test", "password": "wrong"})
    assert response.status_code == 401

def test_login_invalid_request():
    response = client.post("/login", data={"wrong_key": "wrong_value"})
    assert response.status_code == 422