from flask import Blueprint, request, jsonify
from src.models import Cake, Order
from src import db

cake_controller = Blueprint('cake_controller', __name__)

@cake_controller.route('/cakes', methods=['GET'])
def get_all_cakes():
    cakes = Cake.query.all()
    output = []
    for cake in cakes:
        cake_data = {'id': cake.id, 'name': cake.name, 'price': cake.price}
        output.append(cake_data)
    return jsonify(output)

@cake_controller.route('/cakes', methods=['POST'])
def create_cake():
    new_cake = Cake(name=request.json['name'], price=request.json['price'])
    db.session.add(new_cake)
    db.session.commit()
    return jsonify({'id': new_cake.id, 'name': new_cake.name, 'price': new_cake.price})

@cake_controller.route('/cakes/<id>', methods=['GET'])
def get_cake(id):
    cake = Cake.query.filter_by(id=id).first()
    if cake is None:
        return jsonify({'message': 'Cake not found'})
    cake_data = {'id': cake.id, 'name': cake.name, 'price': cake.price}
    return jsonify(cake_data)

@cake_controller.route('/cakes/<id>', methods=['PUT'])
def update_cake(id):
    cake = Cake.query.filter_by(id=id).first()
    if cake is None:
        return jsonify({'message': 'Cake not found'})
    cake.name = request.json.get('name', cake.name)
    cake.price = request.json.get('price', cake.price)
    db.session.commit()
    return jsonify({'id': cake.id, 'name': cake.name, 'price': cake.price})

@cake_controller.route('/cakes/<id>', methods=['DELETE'])
def delete_cake(id):
    cake = Cake.query.filter_by(id=id).first()
    if cake is None:
        return jsonify({'message': 'Cake not found'})
    db.session.delete(cake)
    db.session.commit()
    return jsonify({'message': 'Cake deleted'})

@cake_controller.route('/orders', methods=['POST'])
def create_order():
    new_order = Order(cake_id=request.json['cake_id'], quantity=request.json['quantity'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'id': new_order.id, 'cake_id': new_order.cake_id, 'quantity': new_order.quantity})