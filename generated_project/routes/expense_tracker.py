from flask import Blueprint, render_template, request, jsonify
from routes import db
from models import Expense

expense_tracker = Blueprint('expense_tracker', __name__, template_folder='templates')

@expense_tracker.route('/expenses', methods=['GET'])
def show_expenses():
    expenses = Expense.query.all()
    return render_template('expenses.html', expenses=expenses)

@expense_tracker.route('/add-expense', methods=['POST'])
def add_expense():
    data = request.json
    expense = Expense(**data)
    db.session.add(expense)
    db.session.commit()
    return jsonify({'message': 'Expense added successfully'})

@expense_tracker.route('/update-expense/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    expense = Expense.query.get(expense_id)
    data = request.json
    expense.category = data.get('category')
    expense.amount = data.get('amount')
    db.session.commit()
    return jsonify({'message': 'Expense updated successfully'})

@expense_tracker.route('/delete-expense/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return jsonify({'message': 'Expense deleted successfully'})

@expense_tracker.before_request
def authenticate():
    # Add authentication code here
    pass