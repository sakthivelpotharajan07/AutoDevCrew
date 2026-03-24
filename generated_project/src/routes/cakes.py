from flask import Blueprint, request, jsonify
from src.models import Cake, Order
from src import db

cakes = Blueprint('cakes', __name__)

@cakes.route('/cakes', methods=['GET'])
def get_all_cakes():
    cakes = Cake.query.all()
    return jsonify([cake.to_dict() for cake in cakes])

@cakes.route('/cakes/<int:cake_id>', methods=['GET'])
def get_cake(cake_id):
    cake = Cake.query.get(cake_id)
    if cake:
        return jsonify(cake.to_dict())
    return jsonify({'error': 'Cake not found'}), 404

@cakes.route('/cakes', methods=['POST'])
def create_cake():
    data = request.json
    cake = Cake(name=data['name'], price=data['price'], description=data['description'])
    db.session.add(cake)
    db.session.commit()
    return jsonify(cake.to_dict()), 201

@cakes.route('/cakes/<int:cake_id>', methods=['PUT'])
def update_cake(cake_id):
    cake = Cake.query.get(cake_id)
    if cake:
        data = request.json
        cake.name = data['name']
        cake.price = data['price']
        cake.description = data['description']
        db.session.commit()
        return jsonify(cake.to_dict())
    return jsonify({'error': 'Cake not found'}), 404

@cakes.route('/cakes/<int:cake_id>', methods=['DELETE'])
def delete_cake(cake_id):
    cake = Cake.query.get(cake_id)
    if cake:
        db.session.delete(cake)
        db.session.commit()
        return jsonify({'message': 'Cake deleted'})
    return jsonify({'error': 'Cake not found'}), 404

@cakes.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    order = Order(customer_name=data['customer_name'], cake_id=data['cake_id'])
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict()), 201