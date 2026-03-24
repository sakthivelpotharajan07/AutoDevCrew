import unittest
class TestBusinessManagementSystem(unittest.TestCase):
    def test_home_route(self):
        import requests; response = requests.get('http://localhost:5000/'); self.assertEqual(response.status_code, 200)
