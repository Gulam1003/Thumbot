import pytest
from flask import session
from werkzeug.security import generate_password_hash

from app import create_app  # Make sure to have a factory function for creating your Flask app
from models import db, User

@pytest.fixture
def app():
    """Create and configure a new app instance for testing."""
    _app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'your_secret_key'  # Ensure the secret key is set
    })
    with _app.app_context():
        db.init_app(_app)
        db.create_all()
        yield _app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        # Insert user data
        user1 = User(email='user@example.com', name='User', surname='Test')
        user1.set_password('123456')
        user2 = User(email='admin@example.com', name='Admin', surname='User')
        user2.set_password('121212')
        db.session.add_all([user1, user2])
        db.session.commit()
        yield
        db.session.close()

def test_login(client, init_database):
    """Testing user login with correct credentials."""
    with client:
        response = client.post('/auth/login', data={'email': 'user@example.com', 'password': '123456'}, follow_redirects=True)
        assert response.status_code == 200
        assert session.get('user') == 'user@example.com'
        assert b"Login successful!" in response.data

def test_login_failure(client, init_database):
    """Testing login with incorrect credentials."""
    with client:
        response = client.post('/auth/login', data={'email': 'user@example.com', 'password': 'wrong'}, follow_redirects=True)
        assert response.status_code == 200
        assert 'user' not in session
        assert b"Login failed. Please check your credentials and try again." in response.data

def test_signup(client, init_database):
    """Testing user signup."""
    with client:
        response = client.post('/auth/signup', data={
            'name': 'New', 'surname': 'User', 'email': 'new@example.com', 'password': 'newpassword'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b"Signup successful! Please log in." in response.data

def test_logout(client, init_database):
    """Testing user logout."""
    with client:
        client.post('/auth/login', data={'email': 'user@example.com', 'password': '123456'}, follow_redirects=True)
        response = client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200
        assert 'user' not in session
        assert b"You have been logged out." in response.data

def test_admin_access(client, init_database):
    """Testing admin user can access the home page."""
    with client:
        # Log in as admin
        login_response = client.post('/auth/login', data={'email': 'admin@example.com', 'password': '121212'}, follow_redirects=True)
        assert login_response.status_code == 200
        assert b'Login successful!' in login_response.data
        assert session.get('is_admin') == True
        
        # Access the home page
        response = client.get('/', follow_redirects=True)
        assert response.status_code == 200
        assert b'Struggling to Make Kickass YouTube Thumbnails?' in response.data
