Python

from flask import Flask, render_template, redirect, url_for
from src.routes import main_routes, auth_routes
from src.models import db
from src.forms import login_form
from src.utils.auth import authenticate_user, hash_password
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

app.register_blueprint(main_routes)
app.register_blueprint(auth_routes)

@login_manager.user_loader
def load_user(user_id):
    from src.models.user import User
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)