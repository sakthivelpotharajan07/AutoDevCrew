from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from src.forms.login_form import LoginForm
from src.models.user import User
from src.utils.auth import hash_password, verify_password
from src.auth import authenticate_user

login_page = Blueprint('login_page', __name__)

@login_page.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and verify_password(form.password.data, user.password):
            login_user(user)
            flash('You have been logged in.')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)

@login_page.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and verify_password(password, user.password):
        return user
    return None