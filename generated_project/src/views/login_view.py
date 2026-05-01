from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.exc import IntegrityError
from typing import List
from passlib.context import CryptContext

router = APIRouter()

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///login.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    password = Column(String)

# Create the database tables
Base.metadata.create_all(bind=engine)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Password context
pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")

# Define the UserIn and UserOut models
class UserIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a user
@router.post("/users/")
def create_user(user: UserIn, db = Depends(get_db)):
    user_obj = User(username=user.username, password=pwd_context.hash(user.password))
    try:
        db.add(user_obj)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User created"}

# Login endpoint
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": user.username, "token_type": "bearer"}