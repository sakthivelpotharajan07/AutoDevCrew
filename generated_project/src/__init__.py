from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class LoginResponse(BaseModel):
    token: str

class LoginRequest(BaseModel):
    username: str
    password: str

def get_db():
    from src.database import database
    return database

def authenticate_user(username: str, password: str):
    db = get_db()
    user = db.query(User).filter(User.username == username).first()
    if not user or not user.check_password(password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return user

from src.models import User

def get_current_user(token: str):
    db = get_db()
    user = db.query(User).filter(User.token == token).first()
    return user

security = HTTPBearer()

@app.get("/login")
async def login(request: Request):
    return {"message": "Login page"}

@app.post("/login", response_model=LoginResponse)
async def login_for_access_token(login_request: LoginRequest):
    user = authenticate_user(login_request.username, login_request.password)
    token = user.token
    return {"token": token}

@app.get("/users/me")
async def read_users_me(token: HTTPAuthorizationCredentials = Depends(security)):
    current_user = get_current_user(token.credentials)
    return current_user