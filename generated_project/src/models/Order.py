from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    cake_type = db.Column(db.String(100), nullable=False)
    cake_size = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Order('{self.customer_name}', '{self.cake_type}', '{self.cake_size}', {self.quantity}, {self.order_date}, {self.total_cost})"

    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'cake_type': self.cake_type,
            'cake_size': self.cake_size,
            'quantity': self.quantity,
            'order_date': self.order_date,
            'total_cost': self.total_cost
        }