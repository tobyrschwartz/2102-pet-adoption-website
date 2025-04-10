# pylint: disable=import-error
"""Tests for main.py"""

# pylint: disable=W0621
import sqlite3
from unittest.mock import patch
import pytest
from main import app


@pytest.fixture
def client():
    """Creates a test user for the Flask app"""
    app.testing = True
    with app.test_client as client:
        clear_test_user()
        yield client

def clear_test_user():
    """Clear existing test user in database"""
    conn = sqlite3.connect('pets_adoption.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE usernam= 'test';")
    conn.commit()
    conn.close()

def test_create_user(client):
    """Test user registration"""
    response = client.post('/api/users', json={'username': 'test', 'password': 'test'})
    assert response.status_code == 201
    assert response.json == {'message': 'User created successfully'}

def mock_get_user_role():
    """Mocking get_user_role() for testing"""
    with patch('main.get_user_role') as role:
        yield role


def test_not_logged_in(client):
    """Tests if a user is not logged in"""
    with client:
        response = client.get('/protected')
        assert response.status_code == 401
        assert response.json == {"error": "You must log in"}

def test_not_logged_in_2(client, mock_get_user_role):
    """Tests when the user is not logged in"""
    mock_get_user_role.return_value = 1

    # Logged in user
    with client:
        with client.session_transaction() as session:
            session['user_id'] = 123

        response = client.get('/protected')
        assert response.status_code == 403
        assert response.json == {"error": "You do not have permission to access this resource"}

def test_logged_in(client, mock_get_user_role):
    """Tests when the user is logged in"""
    mock_get_user_role.return_value = 2

    # Logged in user
    with client:
        with client.session_transaction() as session:
            session['user_id'] = 123

        response = client.get('/protected')
        assert response.status_code == 200
        assert response.json == {"message": "You have access"}

def test_home_page(client):
    """Tests homepage accessibility"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Pet Adoption API!" in response.data


def test_login_get(client):
    """Tests that HTML form is properly returned"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"<form method=\"POST\">" in response.data


@patch('main.login')
def test_login(mock_login, client):
    """Test login with valid credentials"""
    mock_login.return_value = '''
        <form method="POST">
            Email: <input type="text" name="email"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
        '''
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'secret'})
    assert response.status_code == 200
    mock_login.assert_called_once_with('test@example.com', 'secret')
    assert b"Logged in" in response.data


@patch('main.logout')
def test_logout(mock_logout, client):
    """Tests logging out"""
    mock_logout.return_value = "Logged out"
    response = client.get('/logout')
    assert response.status_code == 200
    mock_logout.assert_called_once()
    assert b"Logged out" in response.data


@patch('main.get_user_role')
def test_create_pet_no_auth(client):
    """Tests creating a pet without being logged in"""
    response = client.get('/api/pets/create')
    assert response.status_code == 401
    assert response.json == {"error": "You must log in"}


@patch('main.get_user_role')
def test_create_pet_no_permission(mock_get_user_role, client):
    """Tests creating a pet without being an admin"""
    mock_get_user_role.return_value = 1

    with client.session_transaction() as sess:
        sess['user_id'] = 1

    response = client.get('/api/pets/create')
    assert response.status_code == 403
    assert response.json == {"error": "You do not have permission to access this resource"}


@patch('main.get_user_role')
def test_create_pet_success(mock_get_user_role, client):
    """Tests that we can create a pet (if we have admin permission)"""
    mock_get_user_role.return_value = 2

    with client.session_transaction() as sess:
        sess['user_id'] = 1

    response = client.get('/api/pets/create')
    assert response.status_code == 201
    assert response.json == {"message": "Pet created successfully!"}
