Python

import unittest
from unittest.mock import Mock, patch
from yourapplication import app, db
from yourapplication.controllers import CakeController

class TestCakeController(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.controller = CakeController()

    def test_get_all_cakes(self):
        with patch('yourapplication.controllers.CakeController.get_all_cakes') as mock_get_all_cakes:
            mock_get_all_cakes.return_value = []
            result = self.controller.get_all_cakes()
            self.assertEqual(result, [])

    def test_get_cake_by_id(self):
        with patch('yourapplication.controllers.CakeController.get_cake_by_id') as mock_get_cake_by_id:
            mock_get_cake_by_id.return_value = {}
            result = self.controller.get_cake_by_id(1)
            self.assertEqual(result, {})

    def test_create_cake(self):
        with patch('yourapplication.controllers.CakeController.create_cake') as mock_create_cake:
            mock_create_cake.return_value = {}
            result = self.controller.create_cake({})
            self.assertEqual(result, {})

    def test_update_cake(self):
        with patch('yourapplication.controllers.CakeController.update_cake') as mock_update_cake:
            mock_update_cake.return_value = {}
            result = self.controller.update_cake(1, {})
            self.assertEqual(result, {})

    def test_delete_cake(self):
        with patch('yourapplication.controllers.CakeController.delete_cake') as mock_delete_cake:
            mock_delete_cake.return_value = True
            result = self.controller.delete_cake(1)
            self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()