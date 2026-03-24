from flask import Blueprint, request, jsonify
from src import app
from src.models import Cake, Order
from src.database import db

order_controller = Blueprint('order_controller', __name__)

@order_controller.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    cake_id = data.get('cake_id')
    customer_name = data.get('customer_name')
    quantity = data.get('quantity')

    cake = Cake.query.get(cake_id)
    if cake is None:
        return jsonify({'error': 'Cake not found'}), 404

    order = Order(cake_id=cake_id, customer_name=customer_name, quantity=quantity)
    db.session.add(order)
    db.session.commit()

    return jsonify({'message': 'Order created successfully'}), 201

@order_controller.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    output = []
    for order in orders:
        cake = Cake.query.get(order.cake_id)
        order_data = {
            'id': order.id,
            'cake_name': cake.name,
            'customer_name': order.customer_name,
            'quantity': order.quantity
        }
        output.append(order_data)
    return jsonify({'orders': output}), 200

@order_controller.route('/orders/<id>', methods=['GET'])
def get_order(id):
    order = Order.query.get(id)
    if order is None:
        return jsonify({'error': 'Order not found'}), 404

    cake = Cake.query.get(order.cake_id)
    order_data = {
        'id': order.id,
        'cake_name': cake.name,
        'customer_name': order.customer_name,
        'quantity': order.quantity
    }
    return jsonify({'order': order_data}), 200

@order_controller.route('/orders/<id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get(id)
    if order is None:
        return jsonify({'error': 'Order not found'}), 404

    data = request.get_json()
    customer_name = data.get('customer_name')
    quantity = data.get('quantity')

    order.customer_name = customer_name
    order.quantity = quantity
    db.session.commit()

    return jsonify({'message': 'Order updated successfully'}), 200

@order_controller.route('/orders/<id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)
    if order is None:
        return jsonify({'error': 'Order not found'}), 404

    db.session.delete(order)
    db.session.commit()

    return jsonify({'message': 'Order deleted successfully'}), 200