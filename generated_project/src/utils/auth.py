Target Language: Python

from hashlib import sha256
from hmac import compare_digest
import secrets
import string

def generate_salt():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(16))

def hash_password(password, salt):
    return sha256((password + salt).encode()).hexdigest()

def verify_password(stored_password, provided_password, salt):
    return compare_digest(stored_password, hash_password(provided_password, salt))

def authenticate(username, password, stored_username, stored_password, stored_salt):
    if username != stored_username:
        return False
    return verify_password(stored_password, password, stored_salt)

def register_user(username, password):
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    return username, hashed_password, salt

def get_user_credentials(username):
    # This function should be implemented to retrieve user credentials from the database
    # For demonstration purposes, it returns dummy data
    if username == "test_user":
        return "test_user", "hashed_password", "salt"
    return None, None, None