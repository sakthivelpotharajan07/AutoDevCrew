Target Language: Python

import unittest
from src.app import app, db
from src.models import User
import json

class TestUserFunctionality(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        new_user = User(username='testuser', email='testuser@example.com', password='testpassword')
        db.session.add(new_user)
        db.session.commit()
        self.assertEqual(new_user.username, 'testuser')

    def test_get_user(self):
        new_user = User(username='testuser', email='testuser@example.com', password='testpassword')
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(username='testuser').first()
        self.assertEqual(user.username, 'testuser')

    def test_update_user(self):
        new_user = User(username='testuser', email='testuser@example.com', password='testpassword')
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(username='testuser').first()
        user.username = 'updateduser'
        db.session.commit()
        self.assertEqual(user.username, 'updateduser')

    def test_delete_user(self):
        new_user = User(username='testuser', email='testuser@example.com', password='testpassword')
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(username='testuser').first()
        db.session.delete(user)
        db.session.commit()
        self.assertIsNone(User.query.filter_by(username='testuser').first())

    def test_register_user_with_api(self):
        with app.test_client() as client:
            response = client.post('/api/register', data=json.dumps({
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password': 'testpassword'
            }), content_type='application/json')
            self.assertEqual(response.status_code, 201)

    def test_login_user_with_api(self):
        with app.test_client() as client:
            client.post('/api/register', data=json.dumps({
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password': 'testpassword'
            }), content_type='application/json')
            response = client.post('/api/login', data=json.dumps({
                'username': 'testuser',
                'password': 'testpassword'
            }), content_type='application/json')
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()