from flask import Blueprint, request, jsonify
from src.models import Order, Cake
from src import db

orders = Blueprint('orders', __name__)

@orders.route('/orders', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    return jsonify([order.serialize() for order in orders])

@orders.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    cake_id = data.get('cake_id')
    customer_name = data.get('customer_name')
    order_date = data.get('order_date')

    cake = Cake.query.get(cake_id)
    if cake is None:
        return jsonify({'error': 'Cake not found'}), 404

    order = Order(cake=cake, customer_name=customer_name, order_date=order_date)
    db.session.add(order)
    db.session.commit()
    return jsonify(order.serialize())

@orders.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if order is None:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(order.serialize())

@orders.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get(order_id)
    if order is None:
        return jsonify({'error': 'Order not found'}), 404

    data = request.get_json()
    cake_id = data.get('cake_id')
    customer_name = data.get('customer_name')
    order_date = data.get('order_date')

    if cake_id:
        cake = Cake.query.get(cake_id)
        if cake is None:
            return jsonify({'error': 'Cake not found'}), 404
        order.cake = cake
    if customer_name:
        order.customer_name = customer_name
    if order_date:
        order.order_date = order_date

    db.session.commit()
    return jsonify(order.serialize())

@orders.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if order is None:
        return jsonify({'error': 'Order not found'}), 404
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted'})