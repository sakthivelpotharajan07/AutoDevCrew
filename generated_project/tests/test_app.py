import unittest
from app import create_app
from app.models import Cake, Order
from app.controllers import CakeController, OrderController

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app = self.app.test_client()

    def test_cake_creation(self):
        cake = Cake(name='Chocolate Cake', description='A rich, mocha-flavored cake', price=50.0)
        CakeController.create_cake(cake)

    def test_order_creation(self):
        order = Order(customer_name='John Doe', cake_id=1, quantity=2)
        OrderController.create_order(order)

    def test_get_all_cakes(self):
        response = self.app.get('/cakes')
        self.assertEqual(response.status_code, 200)

    def test_get_all_orders(self):
        response = self.app.get('/orders')
        self.assertEqual(response.status_code, 200)

    def test_get_cake_by_id(self):
        response = self.app.get('/cakes/1')
        self.assertEqual(response.status_code, 200)

    def test_get_order_by_id(self):
        response = self.app.get('/orders/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()