from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class LoginForm(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_not_empty(cls, v):
        if not v:
            raise ValueError('Username is required')
        return v

    @validator('password')
    def password_not_empty(cls, v):
        if not v:
            raise ValueError('Password is required')
        return v

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class LoginError(BaseModel):
    detail: str
    status_code: int

class LoginController:
    def __init__(self):
        pass

    async def login(self, login_form: LoginForm):
        try:
            # authenticate user
            # assuming you have a function to authenticate user
            user = await self.authenticate_user(login_form.username, login_form.password)
            if user:
                # generate access token
                access_token = await self.generate_access_token(user)
                return LoginResponse(access_token=access_token, token_type="bearer")
            else:
                raise ValueError('Invalid username or password')
        except Exception as e:
            return LoginError(detail=str(e), status_code=401)

    async def authenticate_user(self, username: str, password: str):
        # implement your logic to authenticate user here
        # this is just a dummy implementation
        # you should use your actual database or authentication logic
        if username == "test" and password == "test":
            return True
        return None

    async def generate_access_token(self, user):
        # implement your logic to generate access token here
        # this is just a dummy implementation
        # you should use your actual token generation logic
        return "dummy_access_token"

login_controller = LoginController()