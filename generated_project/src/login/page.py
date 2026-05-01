Target Language: Python

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from src.login.forms import LoginForm
from src.login.models import User

login_page = Blueprint('login_page', __name__)

@login_page.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@login_page.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page.login'))