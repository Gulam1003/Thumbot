import pytest
from flask import session
from werkzeug.security import generate_password_hash

from app import create_app  
from models import db, User

@pytest.fixture
def app():
    """Create and configure a new app instance for testing."""
    _app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'your_secret_key'  
    })
    with _app.app_context():
        db.init_app(_app)
        db.create_all()
        yield _app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Provide a client to simulate requests to the app."""
    return app.test_client()

@pytest.fixture
def init_database(app):
    """Set up the database with initial test users."""
    with app.app_context():
        user1 = User(email='user@example.com', name='User', surname='Test')
        user1.set_password('123456')
        user2 = User(email='admin@example.com', name='Admin', surname='User')
        user2.set_password('121212')
        db.session.add_all([user1, user2])
        db.session.commit()
        yield
        db.session.close()

def test_login(client, init_database):
    """Test logging in with the correct credentials."""
    with client:
        response = client.post('/auth/login', data={'email': 'user@example.com', 'password': '123456'}, follow_redirects=True)
        assert response.status_code == 200
        assert session.get('user') == 'user@example.com'
        assert "Login successful!" in response.get_data(as_text=True)

def test_login_failure(client, init_database):
    """Test logging in with incorrect credentials."""
    with client:
        response = client.post('/auth/login', data={'email': 'user@example.com', 'password': 'wrong'}, follow_redirects=True)
        assert response.status_code == 200
        assert 'user' not in session
        assert "Login failed. Please check your credentials and try again." in response.get_data(as_text=True)

def test_signup(client, init_database):
    """Test signing up a new user."""
    with client:
        response = client.post('/auth/signup', data={
            'name': 'New', 'surname': 'User', 'email': 'new@example.com', 'password': 'newpassword'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert "Signup successful! Please log in." in response.get_data(as_text=True)

def test_logout(client, init_database):
    """Test logging out a user."""
    with client:
        client.post('/auth/login', data={'email': 'user@example.com', 'password': '123456'}, follow_redirects=True)
        response = client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200
        assert 'user' not in session
        assert "You have been logged out." in response.get_data(as_text=True)

def test_admin_access(client, init_database):
    """Test that an admin user can access the home page."""
    with client:
        login_response = client.post('/auth/login', data={'email': 'admin@example.com', 'password': '121212'}, follow_redirects=True)
        assert login_response.status_code == 200
        assert "Login successful!" in login_response.get_data(as_text=True)
        assert session.get('is_admin') == True
        
        response = client.get('/', follow_redirects=True)
        assert response.status_code == 200
        assert "Struggling to Make Kickass YouTube Thumbnails?" in response.get_data(as_text=True)
