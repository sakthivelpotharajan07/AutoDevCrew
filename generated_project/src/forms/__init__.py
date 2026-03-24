from fastapi import Form
from pydantic import BaseModel

class LoginFormData(BaseModel):
    username: str = Form(...)
    password: str = Form(...)