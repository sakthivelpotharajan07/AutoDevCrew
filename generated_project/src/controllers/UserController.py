from flask import Blueprint, request, jsonify
from src import db
from src.models import User, Cake, Order
from src.decorators import token_required

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/users', methods=['GET'])
@token_required
def get_all_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {'id': user.id, 'name': user.name, 'email': user.email}
        output.append(user_data)
    return jsonify({'users': output})

@user_blueprint.route('/user/<id>', methods=['GET'])
@token_required
def get_one_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'User not found'})
    user_data = {'id': user.id, 'name': user.name, 'email': user.email}
    return jsonify({'user': user_data})

@user_blueprint.route('/user', methods=['POST'])
def create_user():
    new_user = User(name=request.json['name'], email=request.json['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created'})

@user_blueprint.route('/user/<id>', methods=['PUT'])
@token_required
def update_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'User not found'})
    user.name = request.json.get('name', user.name)
    user.email = request.json.get('email', user.email)
    db.session.commit()
    return jsonify({'message': 'User updated'})

@user_blueprint.route('/user/<id>', methods=['DELETE'])
@token_required
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'User not found'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

@user_blueprint.route('/user/orders', methods=['GET'])
@token_required
def get_user_orders():
    user_id = request.args.get('user_id')
    orders = Order.query.filter_by(user_id=user_id).all()
    output = []
    for order in orders:
        order_data = {'id': order.id, 'cake_id': order.cake_id, 'user_id': order.user_id, 'quantity': order.quantity}
        output.append(order_data)
    return jsonify({'orders': output})

@user_blueprint.route('/user/order', methods=['POST'])
@token_required
def create_order():
    new_order = Order(cake_id=request.json['cake_id'], user_id=request.json['user_id'], quantity=request.json['quantity'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'New order created'})