from flask import Blueprint, request, jsonify
from src import db
from src.models import User, Cake, Order
from src.schemas import UserSchema, CakeSchema, OrderSchema
from src.controllers import user_controller, cake_controller, order_controller

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    schema = UserSchema(many=True)
    return jsonify(schema.dump(users))

@users_blueprint.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    schema = UserSchema()
    return jsonify(schema.dump(user))

@users_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = user_controller.create_user(data)
    schema = UserSchema()
    return jsonify(schema.dump(user))

@users_blueprint.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = user_controller.update_user(id, data)
    schema = UserSchema()
    return jsonify(schema.dump(user))

@users_blueprint.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user_controller.delete_user(id)
    return jsonify({"message": "User deleted successfully"})

@users_blueprint.route('/users/<id>/cakes', methods=['GET'])
def get_user_cakes(id):
    cakes = cake_controller.get_user_cakes(id)
    schema = CakeSchema(many=True)
    return jsonify(schema.dump(cakes))

@users_blueprint.route('/users/<id>/orders', methods=['GET'])
def get_user_orders(id):
    orders = order_controller.get_user_orders(id)
    schema = OrderSchema(many=True)
    return jsonify(schema.dump(orders))

@users_blueprint.route('/users/<id>/orders', methods=['POST'])
def create_order(id):
    data = request.get_json()
    order = order_controller.create_order(id, data)
    schema = OrderSchema()
    return jsonify(schema.dump(order))