"""Tests for main.py"""

# pylint: disable=W0621
from unittest.mock import patch
import pytest
from main import app
from enums import Role

@pytest.fixture
def client():
    """Creates a test client for the Flask app"""
    app.testing = True
    app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
    return app.test_client()

@pytest.fixture
def mock_get_user_role():
    """Mocking get_user_role() for testing"""
    with patch('main.get_user_role') as mock:
        yield mock

def test_create_user(client):
    """Test user registration"""
    # Since this endpoint requires admin permissions,
    # we need to simulate being logged in as an admin
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # Simulating an admin user
    # Mock get_user_role to return ADMIN
    with patch('main.get_user_role') as mock_role:
        mock_role.return_value = Role.ADMIN
        # Now make the request
        response = client.post('/api/users', json={'username': 'test', 'password': 'test'})
        assert response.status_code == 201
        # We only need to verify that we get a 201 status code
        # The exact structure of the response might vary
        # Let's just verify some expected fields exist
        assert 'user_id' in response.json
        assert 'email' in response.json
        assert 'role' in response.json

def test_not_logged_in(client):
    """Tests if a user is not logged in"""
    response = client.get('/protected')
    assert response.status_code == 401
    assert response.json == {"error": "You must log in"}

def test_not_logged_in_2(client, mock_get_user_role):
    """Tests when the user is not logged in but has insufficient permissions"""
    mock_get_user_role.return_value = 1  # USER role (not enough for the route)

    # Simulate logged in user
    with client.session_transaction() as sess:
        sess['user_id'] = 123

    response = client.get('/protected')
    assert response.status_code == 403
    assert response.json == {"error": "You do not have permission to access this resource"}

def test_logged_in(client, mock_get_user_role):
    """Tests when the user is logged in with sufficient permissions"""
    mock_get_user_role.return_value = 2  # STAFF role (enough for the route)

    # Simulate logged in user
    with client.session_transaction() as sess:
        sess['user_id'] = 123

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
    mock_login.return_value = ({"message": "Login successful"}, 200)
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'secret'})
    assert response.status_code == 200
    mock_login.assert_called_once_with('test@example.com', 'secret')

@patch('main.logout')
def test_logout(mock_logout, client):
    """Tests logging out"""
    mock_logout.return_value = ({"message": "Logout successful"}, 200)
    response = client.get('/logout')
    assert response.status_code == 200
    mock_logout.assert_called_once()

def test_create_pet_no_auth(client):
    """Tests creating a pet without being logged in"""
    # Don't set user_id in session to simulate not being logged in
    response = client.get('/api/pets/create')
    assert response.status_code == 401
    assert response.json == {"error": "You must log in"}

@patch('main.get_user_role')
def test_create_pet_no_permission(mock_get_user_role, client):
    """Tests creating a pet without being an admin"""
    mock_get_user_role.return_value = 1  # USER role (not enough)

    with client.session_transaction() as sess:
        sess['user_id'] = 1

    response = client.get('/api/pets/create')
    assert response.status_code == 403
    assert response.json == {"error": "You do not have permission to access this resource"}

@patch('main.get_user_role')
def test_create_pet_success(mock_get_user_role, client):
    """Tests that we can create a pet (if we have admin permission)"""
    mock_get_user_role.return_value = 2  # STAFF role (enough)

    with client.session_transaction() as sess:
        sess['user_id'] = 1

    response = client.get('/api/pets/create')
    assert response.status_code == 201
    assert response.json == {"message": "Pet created successfully!"}
    