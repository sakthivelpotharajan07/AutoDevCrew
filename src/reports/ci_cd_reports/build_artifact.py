
# --- src/app.py ---
from flask import Flask, render_template, request, jsonify
from src.config import Config
from src.database import db
from src.models import Cake, Order
from src.routes import cake_routes, order_routes

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(cake_routes)
app.register_blueprint(order_routes)

if __name__ == '__main__':
    app.run(debug=True)

# --- src/config.py ---
Python

class Config:
    FLASK_APP = 'app'
    FLASK_ENV = 'development'
    FLASK_DEBUG = True
    SECRET_KEY = 'secret_key_here'

class DatabaseConfig:
    DB_HOST = 'localhost'
    DB_PORT = 5432
    DB_NAME = 'cake_ordering'
    DB_USER = 'postgres'
    DB_PASSWORD = 'password_here'

    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Configurations:
    DEFAULT = Config
    DB = DatabaseConfig

# --- src/models.py ---
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    orders = db.relationship('Order', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Cake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    orders = db.relationship('OrderItem', backref='cake', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_cost = db.Column(db.Float, nullable=False)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    cake_id = db.Column(db.Integer, db.ForeignKey('cake.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# --- src/routes.py ---
from flask import Blueprint, request, jsonify
from src.models import Cake, Order
from src.controllers import CakeController, OrderController
from src.database import db

routes = Blueprint('routes', __name__)

@routes.route('/cakes', methods=['GET'])
def get_cakes():
    cakes = CakeController.get_all_cakes()
    return jsonify([cake.serialize() for cake in cakes])

@routes.route('/cakes', methods=['POST'])
def create_cake():
    data = request.get_json()
    cake = CakeController.create_cake(data)
    return jsonify(cake.serialize())

@routes.route('/cakes/<int:cake_id>', methods=['GET'])
def get_cake(cake_id):
    cake = CakeController.get_cake(cake_id)
    if cake:
        return jsonify(cake.serialize())
    return jsonify({'error': 'Cake not found'}), 404

@routes.route('/orders', methods=['GET'])
def get_orders():
    orders = OrderController.get_all_orders()
    return jsonify([order.serialize() for order in orders])

@routes.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    order = OrderController.create_order(data)
    return jsonify(order.serialize())

@routes.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = OrderController.get_order(order_id)
    if order:
        return jsonify(order.serialize())
    return jsonify({'error': 'Order not found'}), 404

# --- src/templates/base.html ---
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cake Ordering Website</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="{{ url_for('home') }}">Home</a></li>
                <li><a href="{{ url_for('cakes') }}">Cakes</a></li>
                <li><a href="{{ url_for('orders') }}">Orders</a></li>
            </ul>
        </nav>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>
        <p>&copy; 2024 Cake Ordering Website</p>
    </footer>
</body>
</html>

# --- src/templates/cake_list.html ---
{% extends 'base.html' %}

{% block content %}
    <h1>Cake List</h1>
    <ul>
    {% for cake in cakes %}
        <li>
            {{ cake.name }} ({{ cake.flavor }})
            <a href="{{ url_for('cake_details', cake_id=cake.id) }}">Details</a>
        </li>
    {% endfor %}
    </ul>
    <p><a href="{{ url_for('create_cake') }}">Create New Cake</a></p>
{% endblock %}

# --- src/templates/cake_details.html ---
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cake Details</title>
</head>
<body>
    <h1>Cake Details</h1>
    <p>Cake Name: {{ cake.name }}</p>
    <p>Cake Description: {{ cake.description }}</p>
    <p>Price: {{ cake.price }}</p>
    <p>Size: {{ cake.size }}</p>
    <p>Flavor: {{ cake.flavor }}</p>
    <form action="/order" method="post">
        <input type="hidden" name="cake_id" value="{{ cake.id }}">
        <label for="quantity">Quantity:</label>
        <input type="number" id="quantity" name="quantity" min="1" value="1">
        <button type="submit">Order Now</button>
    </form>
</body>
</html>

# --- src/templates/order_form.html ---
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cake Order Form</title>
</head>
<body>
    <h1>Cake Order Form</h1>
    <form id="order-form" method="post">
        <label for="cake-type">Cake Type:</label>
        <select id="cake-type" name="cake-type">
            <option value="chocolate">Chocolate</option>
            <option value="vanilla">Vanilla</option>
            <option value="red-velvet">Red Velvet</option>
        </select>
        <br><br>
        <label for="size">Size:</label>
        <select id="size" name="size">
            <option value="small">Small (6 inches)</option>
            <option value="medium">Medium (8 inches)</option>
            <option value="large">Large (10 inches)</option>
        </select>
        <br><br>
        <label for="quantity">Quantity:</label>
        <input type="number" id="quantity" name="quantity" min="1" value="1">
        <br><br>
        <label for="pickup-date">Pickup Date:</label>
        <input type="date" id="pickup-date" name="pickup-date">
        <br><br>
        <label for="pickup-time">Pickup Time:</label>
        <input type="time" id="pickup-time" name="pickup-time">
        <br><br>
        <label for="customer-name">Customer Name:</label>
        <input type="text" id="customer-name" name="customer-name">
        <br><br>
        <label for="customer-email">Customer Email:</label>
        <input type="email" id="customer-email" name="customer-email">
        <br><br>
        <label for="special-instructions">Special Instructions:</label>
        <textarea id="special-instructions" name="special-instructions"></textarea>
        <br><br>
        <input type="submit" value="Place Order">
    </form>
</body>
</html>

# --- src/static/css/style.css ---
CSS

# --- src/static/js/script.js ---
JavaScript

# --- src/database.py ---
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()

Base = declarative_base()

def create_database_engine():
    database_url = current_app.config['DATABASE_URL']
    engine = create_engine(database_url)
    return engine

def create_session():
    engine = create_database_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def create_tables():
    engine = create_database_engine()
    Base.metadata.create_all(engine)

def get_db_session():
    session = create_session()
    return session

# --- src/utils.py ---
import datetime
import hashlib
import json
import re
from typing import Any, Dict

def validate_email(email: str) -> bool:
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    return bool(re.match(email_regex, email))

def validate_password(password: str) -> bool:
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    return bool(re.match(password_regex, password))

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_order_id() -> str:
    return str(datetime.datetime.now().timestamp())

def parse_json(data: str) -> Dict[str, Any]:
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return {}

def validate_phone_number(phone_number: str) -> bool:
    phone_number_regex = r"^\d{3}-\d{3}-\d{4}$"
    return bool(re.match(phone_number_regex, phone_number))

# --- src/auth.py ---
Python

from flask importBlueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'error': 'Missing username or password'}), 400
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({'error': 'Username already exists'}), 400
        new_user = User(username=username, password=generate_password_hash(password))
        new_user.save_to_db()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'error': 'Missing username or password'}), 400
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid username or password'}), 401
        return jsonify({'message': 'Logged in successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth.route('/protected', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Hello, {current_user}'}), 200

# --- tests/test_app.py ---
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

# --- tests/test_models.py ---
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

# --- tests/test_routes.py ---
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

# --- requirements.txt ---
Python
Flask==2.2.2
Flask-SQLAlchemy==2.5.1
Flask-WTF==1.0.1
WTForms==3.0.1
Flask-Login==0.6.0
Flask-Bcrypt==1.0.1
Flask-DebugToolbar==0.11.0
python-dotenv==0.20.0
numpy==1.23.4
pandas==1.5.1
sqlalchemy==1.4.42
psycopg2==2.9.5
Flask-Cors==3.0.10
requests==2.28.1
MarkupSafe==2.1.1
Jinja2==3.1.1
Werkzeug==2.2.2
itsdangerous==2.1.2
click==8.1.3
setuptools==58.1.0
wheel==0.37.1
Flask-Migrate==3.1.0
Flask-Script==2.0.6
alembic==1.9.2
Mako==1.2.2
python-editor==1.0.4
