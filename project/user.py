import sqlite3
conn = sqlite3.connect('finance.db')
# cursor = conn.cursor()

def register_user(username, password):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    if not (5 <= len(password) <= 16):
        raise ValueError("Password must be between 5 to 16 characters")
    
    if not (any(char.islower() for char in password) and any(char.isupper() for char in password) and 
            any(char.isdigit() for char in password) and any(char in '!@#$%^&*()' for char in password)):
        raise ValueError("Password must contain at least one uppercase, one lowercase letter, one digit, and one special character")

    
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        print(f"User '{username}' registered successfully!")
    except sqlite3.IntegrityError:
        raise ValueError("Username already exists")
    finally:
            conn.close()
    

def login_user(username, password):
    cursor = conn.cursor()

    # Fetch the user by username
    cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    if user is None:
        conn.close()  
        raise ValueError("Username does not exist")

    if user[1] != password:
        conn.close()  
        raise ValueError("Invalid password")

    # Get the user ID and return it
    user_id = user[0]

    conn.close()

    return user_id

