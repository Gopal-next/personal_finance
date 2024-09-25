import pytest
import sqlite3
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from project.transactions import add_transaction, view_all_transactions, update_transaction, delete_transaction, fetch_by_category


@pytest.fixture
def db_connection():
    conn = sqlite3.connect(":memory:")  
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create transactions table
    cursor.execute('''
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            transaction_type TEXT,
            category TEXT,
            amount REAL,
            date TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    
    yield conn 
    
    conn.close()

def test_add_transaction(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('test_user', 'Password1!'))
    db_connection.commit()

    cursor.execute('SELECT id FROM users WHERE username = ?', ('test_user',))
    user_id = cursor.fetchone()[0]

    # Test adding a transaction
    add_transaction(db_connection, user_id, 'expense', 'food', 100, '2024-09-25 10:00:00')

    # Verify the transaction was added
    cursor.execute('SELECT * FROM transactions WHERE user_id = ?', (user_id,))
    transactions = cursor.fetchall()
    
    assert len(transactions) == 1
    assert transactions[0][1] == user_id
    assert transactions[0][2] == 'expense'
    assert transactions[0][3] == 'food'
    assert transactions[0][4] == 100
    assert transactions[0][5] == '2024-09-25 10:00:00'


def test_view_all_transactions(db_connection, capsys):

    cursor = db_connection.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('test_user', 'Password1!'))
    db_connection.commit()

    cursor.execute('SELECT id FROM users WHERE username = ?', ('test_user',))
    user_id = cursor.fetchone()[0]

    add_transaction(db_connection, user_id, 'expense', 'food', 100)
    add_transaction(db_connection, user_id, 'income', 'salary', 200)


    view_all_transactions(db_connection, user_id)
    
    # Capture printed output
    captured = capsys.readouterr()
    assert 'food' in captured.out
    assert 'salary' in captured.out


def test_update_transaction(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('test_user', 'Password1!'))
    db_connection.commit()

    cursor.execute('SELECT id FROM users WHERE username = ?', ('test_user',))
    user_id = cursor.fetchone()[0]

    add_transaction(db_connection,user_id, 'expense', 'food', 100)

    cursor.execute('SELECT id FROM transactions WHERE user_id = ?', (user_id,))
    transaction_id = cursor.fetchone()[0]

    # Test updating the transaction
    update_transaction(db_connection,transaction_id, 'entertainment', 150, '2024-09-26 12:00:00')

    cursor.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,))
    updated_transaction = cursor.fetchone()

    assert updated_transaction[3] == 'entertainment'
    assert updated_transaction[4] == 150
    assert updated_transaction[5] == '2024-09-26 12:00:00'

def test_delete_transaction(db_connection):
    # Add a test user
    cursor = db_connection.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('test_user', 'Password1!'))
    db_connection.commit()

    cursor.execute('SELECT id FROM users WHERE username = ?', ('test_user',))
    user_id = cursor.fetchone()[0]

    # Add a test transaction
    add_transaction(db_connection,user_id, 'expense', 'food', 100)

    cursor.execute('SELECT id FROM transactions WHERE user_id = ?', (user_id,))
    transaction_id = cursor.fetchone()[0]

    delete_transaction(db_connection,transaction_id)

    # Verify the transaction was deleted
    cursor.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,))
    deleted_transaction = cursor.fetchone()

    assert deleted_transaction is None


