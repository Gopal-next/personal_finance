import sqlite3
from datetime import datetime
from project.database import create_budget_table

def create_budget_table():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            monthly_budget REAL NOT NULL,
            month TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')

def set_budget(user_id,category, monthly_budget,month):
    create_budget_table()
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO budget (user_id, category, monthly_budget, month)
        VALUES (?, ?, ?, ?)
    ''', (user_id, category, monthly_budget, month))

    conn.commit()
    conn.close()

def view_budget(user_id):
    create_budget_table()
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM budget WHERE user_id = ?', (user_id,))
    budgets = cursor.fetchall()

    if not budgets:
        print("No budgets set.")
    else:
        for budget in budgets:
            print(f"ID: {budget[0]}, User ID: {budget[1]}, Category: {budget[2]}, Budget: {budget[3]}, Month: {budget[4]}")
    
    conn.close()
