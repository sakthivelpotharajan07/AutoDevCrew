import unittest
from unittest.mock import patch, MagicMock
from flask.testing import FlaskClient
from src.app import create_app
from src.forms.login_form import LoginForm
from src.models.user import User
from src.utils.auth import hash_password, authenticate_user
from src.routes import login

class TestLoginForm(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()

    def test_empty_form(self):
        with self.app.test_request_context('/login', method='POST'):
            form = LoginForm()
            self.assertFalse(form.validate())

    def test_valid_form(self):
        with self.app.test_request_context('/login', method='POST'):
            form = LoginForm(email='user@example.com', password='password123')
            self.assertTrue(form.validate())

    def test_invalid_email(self):
        with self.app.test_request_context('/login', method='POST'):
            form = LoginForm(email='invalid_email', password='password123')
            self.assertFalse(form.validate())

    def test_invalid_password(self):
        with self.app.test_request_context('/login', method='POST'):
            form = LoginForm(email='user@example.com', password='short')
            self.assertFalse(form.validate())

    @patch('src.utils.auth.authenticate_user')
    def test_authenticate_user_success(self, mock_authenticate_user):
        mock_authenticate_user.return_value = True
        with self.app.test_request_context('/login', method='POST'):
            form = LoginForm(email='user@example.com', password='password123')
            self.assertTrue(form.validate())
            mock_authenticate_user.assert_called_once_with('user@example.com', 'password123')

    @patch('src.utils.auth.authenticate_user')
    def test_authenticate_user_failure(self, mock_authenticate_user):
        mock_authenticate_user.return_value = False
        with self.app.test_request_context('/login', method='POST'):
            form = LoginForm(email='user@example.com', password='password123')
            self.assertFalse(form.validate())
            mock_authenticate_user.assert_called_once_with('user@example.com', 'password123')

    def test_login_route(self):
        with self.app.test_request_context('/login', method='GET'):
            response = self.client.get('/login')
            self.assertEqual(response.status_code, 200)

    def test_login_route_post(self):
        with self.app.test_request_context('/login', method='POST'):
            response = self.client.post('/login', data={'email': 'user@example.com', 'password': 'password123'})
            self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()