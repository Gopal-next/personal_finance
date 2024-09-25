import pytest
import sqlite3
import sys
import os

# Add the project folder to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from project.user import register_user,login_user  # Removed login_user since it isn't used in this test

@pytest.fixture
def db_connection():
    conn = sqlite3.connect(":memory:")  # In-memory database for isolated testing
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    
    yield conn  # Yield connection object for use in tests
    
    conn.close()

def test_register_user_success(db_connection):  # Pass fixture as a parameter
    cursor = db_connection.cursor()

    # Test registering a new user successfully
    register_user(db_connection, 'new_usr__1', 'Password1!')
    
    # Verify the user exists in the database
    cursor.execute('SELECT username FROM users WHERE username = ?', ('new_usr__1',))
    user = cursor.fetchone()
    
    assert user is not None
    assert user[0] == 'new_usr__1'



def test_register_user_existing_username(db_connection):
    conn = db_connection
    cursor = conn.cursor()
    
    # Insert a user directly into the test database
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('new_usr_1', 'Password1!'))
    conn.commit()

    # Try registering the same username again, should raise a ValueError
    with pytest.raises(ValueError, match="Username already exists"):
        register_user(conn,'new_usr_1', 'Password1!')

def test_login_user_success(db_connection):
    conn = db_connection
    cursor = conn.cursor()
    
    # Insert a user directly into the test database
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('existing_user', 'Password1!'))
    conn.commit()

    # Test successful login
    user_id = login_user(conn,'existing_user', 'Password1!')
    assert user_id is not None

def test_login_user_invalid_username(db_connection):
    # Test login with a non-existent username
    conn = db_connection
    cursor = conn.cursor()
    with pytest.raises(ValueError, match="Username does not exist"):
        login_user(conn,'nonexistent_user', 'Password1!')

def test_login_user_invalid_password(db_connection):
    conn = db_connection
    cursor = conn.cursor()
    
    # Insert a user directly into the test database
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('existing_user', 'Password1!'))
    conn.commit()

    # Test login with an incorrect password
    with pytest.raises(ValueError, match="Invalid password"):
        login_user(conn,'existing_user', 'WrongPassword!')
