Python

from flask import Blueprint, request, jsonify
from src.forms.login import LoginForm
from src.services.authentication import Authentication

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        authentication = Authentication()
        if authentication.authenticate(username, password):
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    else:
        return jsonify({'message': 'Invalid form data'}), 400