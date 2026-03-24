Target Language: Python

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_login_page():
    response = client.get("/login")
    assert response.status_code == 200
    assert "Login" in response.text

def test_post_login_page_success():
    response = client.post("/login", data={"username": "test", "password": "test"})
    assert response.status_code == 200
    assert "Login successful" in response.text

def test_post_login_page_failure():
    response = client.post("/login", data={"username": "wrong", "password": "wrong"})
    assert response.status_code == 401
    assert "Invalid username or password" in response.text

def test_post_login_page_empty_fields():
    response = client.post("/login", data={"username": "", "password": ""})
    assert response.status_code == 400
    assert "Username and password are required" in response.text