"""The module for managing user-related operations."""
import sqlite3
from flask import jsonify, make_response, session
from bcrypt import hashpw
from enums import Role

def get_db_connection():
    """
    Create a database connection to the SQLite database.
    :return: SQLite connection object
    """
    conn = sqlite3.connect('petadoption.db')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

def create_user(user_data: dict):
    """
    Creates a new user in the database.
    Assumes password is already hashed.

    Args:
        user_data (dict): A dictionary containing user details:
            - email (str): User's email (must be unique).
            - password_hash (str): The pre-hashed password.
            - full_name (str): User's full name.
            - phone (str): User's phone number (optional).
            - role (int): User's role (integer value from Role enum).
            - approved (bool): Whether the user is approved (default is False).

    Returns:
        tuple: (dict or None, str or None) - (user_data, error_message)
               user_data is a dictionary representation of the created user if successful.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM Users WHERE email = ?
    ''', (user_data['email'],))
    count = cursor.fetchone()[0]
    if count > 0:
        return jsonify("Email already exists"), 400
    cursor.execute('''
        INSERT INTO Users (email, password_hash, full_name, phone, role, approved)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        user_data['email'],
        user_data['password_hash'],
        user_data['full_name'],
        user_data.get('phone', None),
        user_data['role'],
        user_data.get('approved', False)
    ))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    new_user = {'user_id': user_id}
    return jsonify(new_user), 201

def delete_user(user_id: int):
    """
    Create a new user with the given details.
    
    :param username: Username of the user
    :param passsword_hash: Password hash of the user
    :param full_name: Full name of the user
    :param phone: Phone number of the user
    :param role: Role of the user (e.g., Admin, User)
    :return: JSON response with the deleted user and 
    """
    response = {
        "message": "User deleted successfully",
        "user_id": user_id
    }
    return jsonify(response), 200

def get_user_by_id(user_id: int):
    """
    Retrieve a specific user by their ID.

    :param user_id: ID of the user to retrieve
    :return: JSON response with the user details
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    user = dict(user)
    if 'password_hash' in user:
        del user['password_hash']
    return jsonify(user), 200

def get_user_by_id_internal(user_id: int):
    """
    Retrieve a specific user by their ID.

    :param user_id: ID of the user to retrieve
    :return: JSON response with the user details
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    user = dict(user)
    if 'password_hash' in user:
        del user['password_hash']
    return user

def get_user_by_email(email: str):
    """
    Retrieve a specific user by their email.

    :param email: Email of the user to retrieve
    :return: JSON response with the user details
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM USERS WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    user = dict(user)
    user['role'] = Role(user['role'])
    if 'password_hash' in user:
        del user['password_hash']
    return jsonify(user), 200

def get_all_users():
    """
    Retrieve all users.
    
    :return: JSON response with a list of users
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    conn.close()
    if not users:
        return jsonify({"error": "No users found"}), 404

    users = [dict(user) for user in users]
    for user in users:
        user['role'] = Role(user['role'])
    return jsonify(users), 200

def get_users_by_role(role: Role):
    """
    Retrieve all users by their role.
    
    :param role: Role of the users to retrieve (e.g., Admin, User)
    :return: JSON response with a list of users with the specified role
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE role = ?', (role,))
    users = cursor.fetchall()
    conn.close()
    if not users:
        return jsonify({"error": "No users found"}), 404

    users = [dict(user) for user in users]
    for user in users:
        user['role'] = Role(user['role'])
    return jsonify(users), 200

def get_user_role(user_id: str):
    """
    Retrieve the role of a user by their ID.
    :param user_id: ID of the user to retrieve the role for
    :return: ENUM corresponding to the user's role
    """
    response, status = get_user_by_id(user_id)
    if status != 200:
        return Role.GUEST
    user = response.json
    if user.get("role") == Role.ADMIN:
        return Role.ADMIN
    if user.get("role") == Role.STAFF:
        return Role.STAFF
    if user.get("role") == Role.USER:
        return Role.USER
    return Role.GUEST

def get_pw_hash_from_email(email: str):
    """
    Retrieve the password hash of a user by their email.
    
    :param email: Email of the user
    :return: Password hash of the user
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM Users WHERE email = ?', (email,))
    pw_hash = cursor.fetchone()
    conn.close()
    return pw_hash[0] if pw_hash else None

def login(email: str, guessed_password: bytearray):
    """
    Log in a user with the given email and password.
    
    :param email: Email of the user
    :param password: Password of the user
    :return: JSON response with the login status
    """
    response, status = get_user_by_email(email)
    if status != 200:
        return jsonify({"error": "Invalid email or password"}), 401
    user = response.get_json()
    hashed_password = get_pw_hash_from_email(email)
    if hashed_password is None:
        return jsonify({"error": "Invalid email or password"}), 401
    guessed_hash = hashpw(guessed_password, hashed_password)
    if guessed_hash == hashed_password:
        if user.get("role") >= Role.STAFF:
            response = {
            "message": "Login successful",
            "user_id": user.get("user_id"),
            "full_name": user.get("full_name"),
            "role": user.get("role"),
            "approved": user.get("approved"),
            "redirect_url": "/admin/dashboard",
            }
        else:
            response = {
            "message": "Login successful",
            "user_id": user.get("user_id"),
            "full_name": user.get("full_name"),
            "role": user.get("role"),
            "approved": user.get("approved"),
            "redirect_url": "/home",
            }
        session.permanent = True
        session['user_id'] = user.get("user_id")
        return jsonify(response), 200
    return jsonify({"error": "Invalid email or password"}), 401

def logout():
    """
    Log out the current user.
    
    :return: JSON response with the logout status
    """
    if 'user_id' not in session:
        return jsonify({"message": "You're already logged out"}), 200
    session.clear()
    response = {
        "message": "Logged out successfully"
    }
    resp = make_response(jsonify(response))
    resp.delete_cookie("session")
    return resp, 200
