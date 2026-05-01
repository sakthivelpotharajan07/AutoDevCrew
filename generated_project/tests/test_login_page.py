import unittest
from unittest.mock import patch, MagicMock
from flask.testing import FlaskClient
from your_application import create_app
from src.models.user import User
from src.forms.login_form import LoginForm
from src.utils.auth import authenticate_user
from src.routes import login
from src.utils.auth import hash_password

class TestLoginPage(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_login_page_get(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_login_page_post(self):
        form = LoginForm(username='test', password='test')
        response = self.client.post('/login', data=form.data)
        self.assertEqual(response.status_code, 302)

    @patch('src.utils.auth.authenticate_user')
    def test_login_page_post_authenticated(self, mock_authenticate_user):
        mock_authenticate_user.return_value = True
        form = LoginForm(username='test', password='test')
        response = self.client.post('/login', data=form.data)
        self.assertEqual(response.status_code, 302)

    @patch('src.utils.auth.authenticate_user')
    def test_login_page_post_not_authenticated(self, mock_authenticate_user):
        mock_authenticate_user.return_value = False
        form = LoginForm(username='test', password='test')
        response = self.client.post('/login', data=form.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_hash_password(self):
        password = 'test'
        hashed_password = hash_password(password)
        self.assertNotEqual(password, hashed_password)

if __name__ == '__main__':
    unittest.main()