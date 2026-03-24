from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cakes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Cake(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(200), nullable=False)
    orders = relationship('Order', backref='cake', lazy=True)

class Order(db.Model):
    id = Column(Integer, primary_key=True)
    cake_id = Column(Integer, ForeignKey('cake.id'), nullable=False)
    customer_name = Column(String(100), nullable=False)
    order_date = Column(DateTime, nullable=False)
    status = Column(Enum('pending', 'delivered', 'cancelled'), default='pending')