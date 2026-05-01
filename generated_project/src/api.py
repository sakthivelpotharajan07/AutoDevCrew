from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from src.utils.password import hash_password, verify_password
from src.models.user import User

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserInDB(User):
    hashed_password: str

async def get_user(db, username: str):
    for user in db:
        if user.username == username:
            return user
    return None

async def authenticate_user(username: str, password: str, db):
    user = await get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = [
        UserInDB(username="test", hashed_password=hash_password("test")),
    ]
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user.username, "token_type": "bearer"}

@app.post("/api/login")
async def login_api(username: str, password: str):
    db = [
        UserInDB(username="test", hashed_password=hash_password("test")),
    ]
    user = await authenticate_user(username, password, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Login successful"}