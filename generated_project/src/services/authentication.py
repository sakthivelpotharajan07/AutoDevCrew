Target Language: Python

from typing import Dict
import hashlib
import json

class Authentication:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self) -> Dict:
        try:
            with open('users.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open('users.json', 'w') as f:
            json.dump(self.users, f)

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.users[username] = hashed_password
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        if username not in self.users:
            return False
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return self.users[username] == hashed_password

    def authenticate(self, username: str, password: str) -> bool:
        return self.login(username, password)

auth_service = Authentication()