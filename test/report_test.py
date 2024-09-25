import pytest
import sqlite3
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from project.report import monthly_report, yearly_report  # Adjust this import based on your file structure

@pytest.fixture
def db_connection():
    # Create an in-memory SQLite database for testing
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            transaction_type TEXT,
            category TEXT,
            amount REAL,
            date TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Add a test user
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('test_user', 'Password1!'))
    conn.commit()
    
    # Return connection for use in tests
    yield conn
   
    conn.close()
def test_monthly_report(db_connection, capsys):
    cursor = db_connection.cursor()
    
    # Get user_id of the inserted user
    cursor.execute('SELECT id FROM users WHERE username = ?', ('test_user',))
    user_id = cursor.fetchone()[0]

    # Add test transactions for January 2024
    cursor.execute('INSERT INTO transactions (user_id, transaction_type, category, amount, date) VALUES (?, ?, ?, ?, ?)', (user_id, 'income', 'salary', 2000, '2024-01-15 10:00:00'))
    cursor.execute('INSERT INTO transactions (user_id, transaction_type, category, amount, date) VALUES (?, ?, ?, ?, ?)', (user_id, 'expense', 'food', 300, '2024-01-20 10:00:00'))
    cursor.execute('INSERT INTO transactions (user_id, transaction_type, category, amount, date) VALUES (?, ?, ?, ?, ?)', (user_id, 'expense', 'drink', 100, '2024-01-25 10:00:00'))
    db_connection.commit()
    
    monthly_report(db_connection, user_id, '2024-01')
    
    captured = capsys.readouterr()
    
    # Assertions
    assert 'Total Income: 2000' in captured.out
    assert 'Total Expense: 400' in captured.out
    assert 'Savings: 1600' in captured.out


def test_yearly_report(db_connection, capsys):
    cursor = db_connection.cursor()
    
    cursor.execute('SELECT id FROM users WHERE username = ?', ('test_user',))
    user_id = cursor.fetchone()[0]

    cursor.execute('INSERT INTO transactions (user_id, transaction_type, category, amount, date) VALUES (?, ?, ?, ?, ?)', (user_id, 'income', 'salary', 24000, '2024-01-15 10:00:00'))
    cursor.execute('INSERT INTO transactions (user_id, transaction_type, category, amount, date) VALUES (?, ?, ?, ?, ?)', (user_id, 'expense', 'food', 3600, '2024-01-20 10:00:00'))
    cursor.execute('INSERT INTO transactions (user_id, transaction_type, category, amount, date) VALUES (?, ?, ?, ?, ?)', (user_id, 'expense', 'drink', 1200, '2024-02-20 10:00:00'))
    db_connection.commit()

    yearly_report(db_connection,user_id, '2024')
    
    # Capture printed output
    captured = capsys.readouterr()
    
    # Assertions
    assert 'Total Income: 24000' in captured.out
    assert 'Total Expense: 4800' in captured.out
    assert 'Savings: 19200' in captured.out
