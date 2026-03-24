import unittest
from unittest.mock import Mock, patch
from src.app import app, db
from src.models import Cake, Order
from tests.test_base import TestBase

class TestOrders(TestBase):
    def test_create_order(self):
        cake = Cake(name="Test Cake", price=10.99)
        db.session.add(cake)
        db.session.commit()

        order_data = {"cake_id": cake.id, "customer_name": "Test Customer", "quantity": 2}
        response = self.client.post("/orders", json=order_data)
        self.assertEqual(response.status_code, 201)

        order = Order.query.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.cake_id, cake.id)
        self.assertEqual(order.customer_name, "Test Customer")
        self.assertEqual(order.quantity, 2)

    def test_get_all_orders(self):
        cake = Cake(name="Test Cake", price=10.99)
        db.session.add(cake)
        db.session.commit()

        order1 = Order(cake_id=cake.id, customer_name="Test Customer 1", quantity=2)
        order2 = Order(cake_id=cake.id, customer_name="Test Customer 2", quantity=3)
        db.session.add_all([order1, order2])
        db.session.commit()

        response = self.client.get("/orders")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    def test_get_order_by_id(self):
        cake = Cake(name="Test Cake", price=10.99)
        db.session.add(cake)
        db.session.commit()

        order = Order(cake_id=cake.id, customer_name="Test Customer", quantity=2)
        db.session.add(order)
        db.session.commit()

        response = self.client.get(f"/orders/{order.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["id"], order.id)
        self.assertEqual(response.json["cake_id"], cake.id)
        self.assertEqual(response.json["customer_name"], "Test Customer")
        self.assertEqual(response.json["quantity"], 2)

    def test_update_order(self):
        cake = Cake(name="Test Cake", price=10.99)
        db.session.add(cake)
        db.session.commit()

        order = Order(cake_id=cake.id, customer_name="Test Customer", quantity=2)
        db.session.add(order)
        db.session.commit()

        updated_order_data = {"cake_id": cake.id, "customer_name": "Updated Customer", "quantity": 3}
        response = self.client.put(f"/orders/{order.id}", json=updated_order_data)
        self.assertEqual(response.status_code, 200)

        updated_order = Order.query.get(order.id)
        self.assertEqual(updated_order.cake_id, cake.id)
        self.assertEqual(updated_order.customer_name, "Updated Customer")
        self.assertEqual(updated_order.quantity, 3)

    def test_delete_order(self):
        cake = Cake(name="Test Cake", price=10.99)
        db.session.add(cake)
        db.session.commit()

        order = Order(cake_id=cake.id, customer_name="Test Customer", quantity=2)
        db.session.add(order)
        db.session.commit()

        response = self.client.delete(f"/orders/{order.id}")
        self.assertEqual(response.status_code, 204)

        self.assertIsNone(Order.query.get(order.id))

if __name__ == "__main__":
    unittest.main()