import unittest
from unittest.mock import patch, Mock
from yourapplication import app, db
from yourapplication.models import Cake, Order
from yourapplication.controllers import CakeController, OrderController

class TestMainApplication(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index_route(self):
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)

    def test_cake_controller(self):
        cake_controller = CakeController()
        cake = Cake(name='Test Cake', price=10.99)
        db.session.add(cake)
        db.session.commit()
        self.assertEqual(cake_controller.get_cake(cake.id).name, 'Test Cake')

    def test_order_controller(self):
        order_controller = OrderController()
        cake = Cake(name='Test Cake', price=10.99)
        db.session.add(cake)
        db.session.commit()
        order = Order(cake_id=cake.id)
        db.session.add(order)
        db.session.commit()
        self.assertEqual(order_controller.get_order(order.id).cake_id, cake.id)

    @patch('yourapplication.controllers.CakeController.get_cake')
    def test_cake_controller_get_cake_mocked(self, mock_get_cake):
        cake_controller = CakeController()
        mock_cake = Mock(name='Test Cake', price=10.99)
        mock_get_cake.return_value = mock_cake
        self.assertEqual(cake_controller.get_cake(1).name, 'Test Cake')

if __name__ == '__main__':
    unittest.main()