from pydantic import BaseModel
from typing import Dict, Any

class Settings(BaseModel):
    development: bool = False
    testing: bool = False
    production: bool = False
    database: Dict[str, str] = {"host": "localhost", "database": "clothing_dashboard", "user": "root", "password": "password"}
    secret_key: str = "your_secret_key_here"
    jwt_token_time_to_live: int = 30
    algorithm: str = "HS256"
    max_user_login_attempts: int = 5
    allowed_hosts: Any = None

settings = Settings(development=False, testing=False, production=False,
                   database={"host": "localhost", "database": "clothing_dashboard", "user": "root", "password": "password"},
                   secret_key="your_secret_key_here", jwt_token_time_to_live=30, algorithm="HS256", max_user_login_attempts=5)