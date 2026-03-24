from flask import Blueprint
from src.routes.login import login_router
from src.services.authentication import Authentication

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')
auth = Authentication()

def init_app(app):
    app.register_blueprint(auth_blueprint)
    auth.init_auth(app)