import unittest
from unittest.mock import patch, MagicMock
from yourapplication import app, db
from yourapplication.models import Cake, Order

class TestCakes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_create_cake(self):
        cake = Cake(name='Test Cake', price=10.99)
        db.session.add(cake)
        db.session.commit()
        self.assertIn(cake, Cake.query.all())

    def test_create_order(self):
        cake = Cake(name='Test Cake', price=10.99)
        db.session.add(cake)
        db.session.commit()
        order = Order(cake_id=cake.id, quantity=2)
        db.session.add(order)
        db.session.commit()
        self.assertIn(order, Order.query.all())

    @patch('yourapplication.models.Cake')
    def test_cake_view(self, mock_cake):
        mock_cake.query.get.return_value = MagicMock(id=1, name='Test Cake', price=10.99)
        response = self.app.get('/cakes/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Cake', response.data)

    @patch('yourapplication.models.Order')
    def test_order_view(self, mock_order):
        mock_order.query.get.return_value = MagicMock(id=1, cake_id=1, quantity=2)
        response = self.app.get('/orders/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'2', response.data)

if __name__ == '__main__':
    unittest.main()