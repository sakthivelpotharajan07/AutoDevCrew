Target Language: Python

from flask import Blueprint, render_template, request, redirect, url_for
from src.models import User

class UserView:
    def __init__(self):
        self.user_blueprint = Blueprint('user', __name__, template_folder='templates')

    def index(self):
        users = User.query.all()
        return render_template('user/index.html', users=users)

    def create(self):
        if request.method == 'POST':
            new_user = User(name=request.form['name'], email=request.form['email'])
            new_user.save_to_db()
            return redirect(url_for('user.index'))
        return render_template('user/create.html')

    def update(self, id):
        user = User.query.get(id)
        if request.method == 'POST':
            user.name = request.form['name']
            user.email = request.form['email']
            user.save_to_db()
            return redirect(url_for('user.index'))
        return render_template('user/update.html', user=user)

    def delete(self, id):
        user = User.query.get(id)
        user.delete_from_db()
        return redirect(url_for('user.index'))