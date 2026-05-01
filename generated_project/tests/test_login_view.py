import pytest
from flask.testing import FlaskClient
from src import create_app, db
from src.models.user import User
from src.forms.login_form import LoginForm
from src.utils.auth import authenticate_user
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.create_all(app=app)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_view_get_request(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_login_view_post_request_valid_credentials(client):
    user = User(username='test', password=generate_password_hash('test'))
    db.session.add(user)
    db.session.commit()
    form = LoginForm(username='test', password='test')
    response = client.post('/login', data=form.data)
    assert response.status_code == 302

def test_login_view_post_request_invalid_credentials(client):
    user = User(username='test', password=generate_password_hash('test'))
    db.session.add(user)
    db.session.commit()
    form = LoginForm(username='test', password='wrong')
    response = client.post('/login', data=form.data)
    assert response.status_code == 401

def test_login_view_post_request_empty_credentials(client):
    response = client.post('/login', data={'username': '', 'password': ''})
    assert response.status_code == 400

def test_login_view_authenticate_user_valid_credentials(app):
    user = User(username='test', password=generate_password_hash('test'))
    db.session.add(user)
    db.session.commit()
    assert authenticate_user('test', 'test')

def test_login_view_authenticate_user_invalid_credentials(app):
    user = User(username='test', password=generate_password_hash('test'))
    db.session.add(user)
    db.session.commit()
    assert not authenticate_user('test', 'wrong')