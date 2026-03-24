import unittest
from flask_testing import TestCase
from app import create_app
from app.models import Cake, Order
from app.routes import cakes, orders

class TestRoutes(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        return app

    def test_cake_routes(self):
        response = self.client.get('/cakes')
        self.assertEqual(response.status_code, 200)

    def test_order_routes(self):
        response = self.client.get('/orders')
        self.assertEqual(response.status_code, 200)

    def test_create_cake(self):
        cake = {'name': 'Test Cake', 'description': 'Test Cake Description', 'price': 10.99}
        response = self.client.post('/cakes', json=cake)
        self.assertEqual(response.status_code, 201)

    def test_create_order(self):
        order = {'cake_id': 1, 'quantity': 2}
        response = self.client.post('/orders', json=order)
        self.assertEqual(response.status_code, 201)

    def test_get_cake(self):
        cake = Cake(name='Test Cake', description='Test Cake Description', price=10.99)
        cake.save_to_db()
        response = self.client.get(f'/cakes/{cake.id}')
        self.assertEqual(response.status_code, 200)

    def test_get_order(self):
        order = Order(cake_id=1, quantity=2)
        order.save_to_db()
        response = self.client.get(f'/orders/{order.id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()