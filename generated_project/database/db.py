import sqlite3
from sqlite3 import Error

class DatabaseHelper:
    def __init__(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
        except Error as e:
            print(e)

    def create_expense_table(self):
        query = """CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE,
                    category TEXT,
                    description TEXT,
                    amount REAL
                    );"""
        self.cursor.execute(query)
        self.conn.commit()

    def insert_expense(self, date, category, description, amount):
        query = """INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?);"""
        self.cursor.execute(query, (date, category, description, amount))
        self.conn.commit()

    def retrieve_all_expenses(self):
        query = """SELECT * FROM expenses ORDER BY date DESC;"""
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()