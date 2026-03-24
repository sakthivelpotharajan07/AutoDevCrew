Python

from flask import Blueprint, render_template, request, redirect, url_for
from src.models.CakeModel import CakeModel

class CakeView:
    def __init__(self):
        self.cake_model = CakeModel()
        self.cake_blueprint = Blueprint('cake', __name__, template_folder='templates')

    def index(self):
        cakes = self.cake_model.get_all_cakes()
        return render_template('cakes.html', cakes=cakes)

    def show(self, cake_id):
        cake = self.cake_model.get_cake_by_id(cake_id)
        return render_template('cake.html', cake=cake)

    def create(self):
        if request.method == 'POST':
            self.cake_model.create_cake(request.form)
            return redirect(url_for('cake.index'))
        return render_template('create_cake.html')

    def update(self, cake_id):
        cake = self.cake_model.get_cake_by_id(cake_id)
        if request.method == 'POST':
            self.cake_model.update_cake(cake_id, request.form)
            return redirect(url_for('cake.show', cake_id=cake_id))
        return render_template('update_cake.html', cake=cake)

    def delete(self, cake_id):
        self.cake_model.delete_cake(cake_id)
        return redirect(url_for('cake.index'))
        
    def register_routes(self, app):
        self.cake_blueprint.add_url_rule('/cakes', view_func=self.index)
        self.cake_blueprint.add_url_rule('/cakes/<int:cake_id>', view_func=self.show)
        self.cake_blueprint.add_url_rule('/cakes/create', view_func=self.create, methods=['GET', 'POST'])
        self.cake_blueprint.add_url_rule('/cakes/<int:cake_id>/update', view_func=self.update, methods=['GET', 'POST'])
        self.cake_blueprint.add_url_rule('/cakes/<int:cake_id>/delete', view_func=self.delete)
        app.register_blueprint(self.cake_blueprint)