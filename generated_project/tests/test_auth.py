Target Language: Python

from fastapi.testclient import TestClient
from main import app
from src.utils.password import verify_password
from src.models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.database import Base, User as UserModel

engine = create_engine("sqlite:///test.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

client = TestClient(app)

def test_user_registration():
    user_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/register", json=user_data)
    assert response.status_code == 201
    user = session.query(UserModel).filter_by(username="testuser").first()
    assert user
    assert verify_password("testpassword", user.password)

def test_user_login():
    user_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/token", data=user_data)
    assert response.status_code == 200
    assert response.json()["access_token"]

def test_invalid_login():
    user_data = {"username": "testuser", "password": "wrongpassword"}
    response = client.post("/token", data=user_data)
    assert response.status_code == 401

def test_login_with_non_existent_user():
    user_data = {"username": "nonexistentuser", "password": "testpassword"}
    response = client.post("/token", data=user_data)
    assert response.status_code == 401