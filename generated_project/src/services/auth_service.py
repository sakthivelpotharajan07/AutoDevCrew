from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
import jwt
import datetime

db = SQLAlchemy()

class AuthenticationService:
    def __init__(self, app: Flask):
        self.app = app
        self.db = db

    def register(self, username: str, password: str):
        user = self.db.session.query(User).filter_by(username=username).first()
        if user:
            return False
        new_user = User(username=username, password=generate_password_hash(password))
        self.db.session.add(new_user)
        self.db.session.commit()
        return True

    def login(self, username: str, password: str):
        user = self.db.session.query(User).filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return False
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user.id
        }
        token = jwt.encode(payload, self.app.config['SECRET_KEY'], algorithm='HS256')
        return token

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"