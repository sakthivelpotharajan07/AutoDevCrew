Python

from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from src.services.authentication import Authentication

router = APIRouter(tags=["login"])

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    authentication = Authentication()
    user = authentication.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )
    return {"access_token": user.generate_token(), "token_type": "bearer"}