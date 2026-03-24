from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from src.models import Cake, Order
from src.controllers import CakeController, OrderController

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cake_ordering.db'
db = SQLAlchemy(app)

cake_controller = CakeController()
order_controller = OrderController()

@app.route('/cakes', methods=['GET'])
def get_cakes():
    cakes = cake_controller.get_cakes()
    return jsonify([cake.serialize() for cake in cakes])

@app.route('/cakes', methods=['POST'])
def create_cake():
    data = request.get_json()
    cake = cake_controller.create_cake(data)
    return jsonify(cake.serialize())

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = order_controller.get_orders()
    return jsonify([order.serialize() for order in orders])

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    order = order_controller.create_order(data)
    return jsonify(order.serialize())

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)