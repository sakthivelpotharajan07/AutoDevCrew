import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from typing import Optional
from .config import settings

SECRET_KEY = settings.SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")
access_token_expires = timedelta(minutes=30)

class Authenticator:
    def __init__(self):
        self.security = HTTPBearer()

    def verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return pwd_context.hash(password)

    def create_access_token(
        data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, SECRET_KEY, algorithm="HS256"
        )
        return encoded_jwt

    async def get_current_user(
        self, http_authorization_credentials: HTTPAuthorizationCredentials
    ) -> Optional[str]:
        payload = jwt.decode(
            http_authorization_credentials.credentials, SECRET_KEY, algorithms=["HS256"]
        )
        return payload["user_id"]

    def create_token_for_user(self, username: str):
        user_id = username  # replace with actual user_id
        data = {"sub": user_id}
        access_token = self.create_access_token(data, access_token_expires)
        return access_token