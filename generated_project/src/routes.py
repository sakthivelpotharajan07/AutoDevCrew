from flask import Blueprint, request, redirect, url_for, render_template
from src.utils.auth import authenticate_user, hash_password
from src.models.user import User
from src.forms.login_form import LoginForm

routes = Blueprint('routes', __name__)

@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and authenticate_user(form.password.data, user.password):
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@routes.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=hash_password(form.password.data))
        user.save_to_db()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)