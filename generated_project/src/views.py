from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from pydantic import BaseModel
from typing import Optional

SQLALCHEMY_DATABASE_URL = "sqlite:///users.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)

router = APIRouter()

security = HTTPBasic()

class UserCredentials(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(credentials: UserCredentials):
    db = SessionLocal()
    user = db.query(User).filter(User.username == credentials.username).first()
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return JSONResponse(content={"message": "Login successful"}, status_code=200)