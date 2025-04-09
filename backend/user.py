"""The module for managing user-related operations."""
from flask import jsonify, session
from enums import Role

def create_user(email: str, passsword_hash: str, full_name: str, phone: str, role: Role):
    """
    Create a new user with the given details.
    
    :param email: Email of the user
    :param passsword_hash: Password hash of the user
    :param full_name: Full name of the user
    :param phone: Phone number of the user
    :param role: Role of the user (e.g., Admin, User)
    :return: JSON response with the created user details
    """
    new_user = {
        "user_id": 1,
        "email": email,
        "password_hash": passsword_hash,
        "full_name": full_name,
        "phone": phone,
        "role": role
    }
    session['user_id'] = new_user.get("user_id")
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
    user = {
        "user_id": user_id,
        "email": "user@example.com",
        "password_hash": "passsword_hash",
        "full_name": "Jane Doe",
        "phone": "111-222-3333",
        "role": Role.USER
    }
    return jsonify(user), 200

def get_user_by_email(email: str):
    """
    Retrieve a specific user by their email.

    :param email: Email of the user to retrieve
    :return: JSON response with the user details
    """
    user = {
        "user_id": 3,
        "email": email,
        "password_hash": "passsword_hash",
        "full_name": "Jane Doe",
        "phone": "111-222-3333",
        "role": Role.USER
    }
    return jsonify(user), 200

def get_all_users():
    """
    Retrieve all users.
    
    :return: JSON response with a list of users
    """
    users = [{
        "user_id": 3,
        "email": "user@example.com",
        "password_hash": "passsword_hash",
        "full_name": "Jane Doe",
        "phone": "111-222-3333",
        "role": Role.USER
    },
    {
        "user_id": 1,
        "email": "admin@example.com",
        "password_hash": "passsword_hash",
        "full_name": "John Doe",
        "phone": "333-222-1111",
        "role": Role.ADMIN
    }]
    return jsonify(users), 200

def get_users_by_role(role: Role):
    """
    Retrieve all users by their role.
    
    :param role: Role of the users to retrieve (e.g., Admin, User)
    :return: JSON response with a list of users with the specified role
    """
    users = [{
        "user_id": 3,
        "email": "user@example.com",
        "password_hash": "passsword_hash",
        "full_name": "Jane Doe",
        "phone": "111-222-3333",
        "role": role
    }]
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

def login(email: str, password: str):
    """
    Log in a user with the given email and password.
    
    :param email: Email of the user
    :param password: Password of the user
    :return: JSON response with the login status
    """
    response, status = get_user_by_email(email)
    if status != 200:
        return jsonify({"error": "Invalid email or password"}), 401
    user = response.json
    if password == user.get("password_hash"):
        pass # just need to use password to get pylint to stfu (it is a mock function)
    response = {
        "message": "Login successful",
        "user_id": user.get("user_id"),
        "role": user.get("role"),
    }
    session['user_id'] = user.get("user_id")
    return jsonify(response), 200

def logout():
    """
    Log out the current user.
    
    :return: JSON response with the logout status
    """
    session.pop('user_id', None)
    response = {
        "message": "Logout successful"
    }
    return jsonify(response), 200
