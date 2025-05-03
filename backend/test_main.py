"""Tests for main.py"""
#pylint: disable=redefined-outer-name
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

def test_not_logged_in(client):
    """Tests if a user is not logged in"""
    response = client.get('/protected')
    assert response.status_code == 401
    assert response.json == {"error": "You must log in"}

def test_not_logged_in_2(client, mock_get_user_role):
    """Tests when the user is not logged in but has insufficient permissions"""
    mock_get_user_role.return_value = 1  # USER role (not enough for the route)
    with client.session_transaction() as sess:
        sess['user_id'] = 123
    response = client.get('/protected')
    assert response.status_code == 403
    assert response.json == {"error": "You do not have permission to access this resource"}

def test_logged_in(client, mock_get_user_role):
    """Tests when the user is logged in with sufficient permissions"""
    mock_get_user_role.return_value = 2  # STAFF role (enough for the route)
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

@patch('main.login')
def test_login(mock_login, client):
    """Test login with valid credentials"""
    mock_login.return_value = ({"message": "Login successful"}, 200)
    response = client.post('/login', json={'email': 'test@example.com', 'password': 'secret'})
    assert response.status_code == 200
    mock_login.assert_called_once_with('test@example.com', b'secret')

@patch('main.logout')
def test_logout(mock_logout, client):
    """Tests logging out (POST method)"""
    mock_logout.return_value = ({"message": "Logout successful"}, 200)
    response = client.post('/logout')
    assert response.status_code == 200
    mock_logout.assert_called_once()

def test_create_pet_no_auth(client):
    """Tests creating a pet without being logged in"""
    response = client.post('/api/pets', json={})
    assert response.status_code == 401
    assert response.json == {"error": "You must log in"}

@patch('main.get_user_role')
def test_create_pet_no_permission(mock_get_user_role, client):
    """Tests creating a pet without being an admin"""
    mock_get_user_role.return_value = Role.USER
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    response = client.post('/api/pets', json={})
    assert response.status_code == 403
    assert response.json == {"error": "You do not have permission to access this resource"}
