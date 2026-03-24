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