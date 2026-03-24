import unittest
from unittest.mock import MagicMock
from yourapplication import db
from yourapplication.models import Cake, Order, Customer

class TestModels(unittest.TestCase):

    def test_cake_model(self):
        cake = Cake(name='Test Cake', description='This is a test cake', price=10.99)
        db.session.add(cake)
        db.session.commit()
        self.assertEqual(cake.name, 'Test Cake')
        self.assertEqual(cake.description, 'This is a test cake')
        self.assertEqual(cake.price, 10.99)

    def test_order_model(self):
        customer = Customer(name='Test Customer', email='test@example.com')
        db.session.add(customer)
        db.session.commit()
        cake = Cake(name='Test Cake', description='This is a test cake', price=10.99)
        db.session.add(cake)
        db.session.commit()
        order = Order(customer_id=customer.id, cake_id=cake.id, quantity=2)
        db.session.add(order)
        db.session.commit()
        self.assertEqual(order.customer_id, customer.id)
        self.assertEqual(order.cake_id, cake.id)
        self.assertEqual(order.quantity, 2)

    def test_customer_model(self):
        customer = Customer(name='Test Customer', email='test@example.com')
        db.session.add(customer)
        db.session.commit()
        self.assertEqual(customer.name, 'Test Customer')
        self.assertEqual(customer.email, 'test@example.com')

if __name__ == '__main__':
    unittest.main()