from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from src.services.authentication import Authentication

db = SQLAlchemy()

class Login:
    def __init__(self):
        self.authentication = Authentication()

    def login(self):
        data = request.json
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400
        user = self.authentication.authenticate(username, password)
        if user:
            return jsonify({'message': 'Login successful', 'user': user}), 200
        return jsonify({'message': 'Invalid username or password'}), 401

login_blueprint = Blueprint('login', __name__)
login_service = Login()

@login_blueprint.route('/login', methods=['POST'])
def login():
    return login_service.login()