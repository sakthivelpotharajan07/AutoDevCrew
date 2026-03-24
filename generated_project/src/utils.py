import datetime
import hashlib
import json
import re
from typing import Any, Dict

def validate_email(email: str) -> bool:
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    return bool(re.match(email_regex, email))

def validate_password(password: str) -> bool:
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    return bool(re.match(password_regex, password))

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_order_id() -> str:
    return str(datetime.datetime.now().timestamp())

def parse_json(data: str) -> Dict[str, Any]:
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return {}

def validate_phone_number(phone_number: str) -> bool:
    phone_number_regex = r"^\d{3}-\d{3}-\d{4}$"
    return bool(re.match(phone_number_regex, phone_number))