from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
import secrets
from typing import Optional
from pydantic import BaseModel
from . import schemas, crud
from .database import get_db
from .config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None
    exp: datetime | None

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = crud.user.get(db, username=username)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

    return user

async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    return current_user

async def create_user(db: Session, user: schemas.UserCreate):
    db_user = crud.user.get(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.user.create(db, obj_in=user)

async def login_for_access_token(db: Session, form_data: OAuth2PasswordRequestForm):
    user = crud.user.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = crud.user.create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=15),
        secret_key=SECRET_KEY,
        algorithm=ALGORITHM)
    return Token(access_token=access_token, token_type="bearer")