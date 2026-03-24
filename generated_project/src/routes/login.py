from flask import Blueprint, render_template, request, redirect, url_for
from src.forms import LoginForm
from src.models import User
from src import db

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)