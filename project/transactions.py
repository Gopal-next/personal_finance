import sqlite3
from datetime import datetime


# def add_transaction(user_id, transaction_type, category, amount, date=None):
#     conn = sqlite3.connect('finance.db')
#     cursor = conn.cursor()
#     if date is None:
#         date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#     cursor.execute('''
#         INSERT INTO transactions (user_id, transaction_type, category, amount, date)
#         VALUES (?, ?, ?, ?, ?)
#     ''', (user_id, transaction_type, category, amount, date))
    
#     conn.commit()
#     conn.close()

import sqlite3
from datetime import datetime

def add_transaction(user_id, transaction_type, category, amount, date=None):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insert the new transaction
    cursor.execute('''
        INSERT INTO transactions (user_id, transaction_type, category, amount, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, transaction_type, category, amount, date))
    
    conn.commit()

    # Check the user's budget for the category
    cursor.execute('SELECT monthly_budget FROM budget WHERE user_id = ? AND category = ?', (user_id, category))
    budget = cursor.fetchone()

    if budget:
        budget_limit = budget[0]

        # Calculate total expenses for the category
        cursor.execute('''
            SELECT SUM(amount) 
            FROM transactions 
            WHERE user_id = ? AND category = ? AND transaction_type = 'expense'
        ''', (user_id, category))
        
        total_expense = cursor.fetchone()[0] or 0  # Use 0 if no expenses found

        # Notify if the total expense exceeds the budget
        if total_expense > budget_limit:
            print(f"Notification: Your expenses in the category '{category}' have exceeded the budget limit of {budget_limit}. Total expenses: {total_expense}. Delete or update the transactions to not to get notification")

    conn.close()


def view_all_transactions(user_id):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM transactions WHERE user_id = ?', (user_id,))
    transactions = cursor.fetchall()

    if not transactions:
        print("No transactions found.")
    else:
        for transaction in transactions:
            print(f"ID: {transaction[0]}, User ID: {transaction[1]}, Type: {transaction[2]}, Category: {transaction[3]}, Amount: {transaction[4]}, Date: {transaction[5]}")

    conn.close()

def update_transaction(transaction_id, category, amount, date=None):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    if date is None:
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        UPDATE transactions
        SET category = ?, amount = ?, date = ?
        WHERE id = ?
    ''', (category, amount, date, transaction_id))

    conn.commit()
    conn.close()

def delete_transaction(transaction_id):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
    conn.commit()
    conn.close()

def fetch_by_category(user_id, transaction_type):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT category, SUM(amount)
        FROM transactions
        WHERE user_id = ? AND transaction_type = ?
        GROUP BY category
    ''', (user_id, transaction_type))

    fetch = cursor.fetchall()
    conn.close()

    total = 0
    for category, total_amount in fetch:
        print(f"Category: {category}, Total Amount: {total_amount}")
        total += total_amount

    print("Overall amount:", total)
    # overall_amount = sum(row[1] for row in fetch)
    # print(f"Overall amount: {overall_amount}")