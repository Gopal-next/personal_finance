import sqlite3

def monthly_report(user_id, month):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    print(f"Fetching transactions for month: {month}")
    cursor.execute('''
                    SELECT transaction_type, SUM(amount) 
                    FROM transactions 
                    WHERE strftime('%Y-%m', date) = ? AND user_id = ?
                    GROUP BY transaction_type
                   ''', (month, user_id))
    
    report = cursor.fetchall()
    conn.close()
    print(f"Fetched data: {report}")

    income_categories = ['income', 'salary']
    expense_categories = ['expense', 'food', 'drink']
    
    total_income = sum(amount for t, amount in report if t in income_categories)
    total_expense = sum(amount for t, amount in report if t in expense_categories)
    savings = total_income - total_expense

    print(f"Total Income: {total_income}")
    print(f"Total Expense: {total_expense}")
    print(f"Savings: {savings}")

def yearly_report(user_id, year):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    print(f"Fetching transactions for year: {year}")
    
    cursor.execute('''
                    SELECT transaction_type, SUM(amount) 
                    FROM transactions 
                    WHERE substr(date, 1, 4) = ? AND user_id = ?
                    GROUP BY transaction_type
                   ''', (year, user_id))
    
    report = cursor.fetchall()
    conn.close()
    print(f"Fetched data: {report}")
    
    total_income = sum(amount for t, amount in report if t == 'income')
    total_expense = sum(amount for t, amount in report if t == 'expense')
    savings = total_income - total_expense

    print(f"Total Income: {total_income}")
    print(f"Total Expense: {total_expense}")
    print(f"Savings: {savings}")
