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