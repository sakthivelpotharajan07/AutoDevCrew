Python 

from typing import Any
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request
from fastapi import Response
from fastapi import status

security = HTTPBearer()