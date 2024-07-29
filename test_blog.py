import pytest
from app import create_app
from models import User, db, BlogPost

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'your_test_secret_key'
    }
    app = create_app(test_config)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    """Initialize the database with some test data."""
    with app.app_context():
        # Create an admin user
        admin_email = 'admin@example.com'
        admin_password = '121212'
        admin_user = User(email=admin_email, name='Admin', surname='User')
        admin_user.set_password(admin_password)
        db.session.add(admin_user)

        # Create some blog posts
        post1 = BlogPost(title='Test Post', content='This is a test post.', author='Admin')
        post2 = BlogPost(title='Test Post 2', content='This is another test post.', author='Guest')
        db.session.add(post1)
        db.session.add(post2)

        db.session.commit()
        yield
        db.session.remove()
        db.drop_all()

def test_blog_page(client, init_database):
    """Test the blog index page can display posts."""
    response = client.get('/blog/blog')
    assert response.status_code == 200
    assert 'Test Post' in response.get_data(as_text=True)
    assert 'This is a test post.' in response.get_data(as_text=True)

def test_single_post(client, init_database):
    """Test a single post page loads from the blog."""
    post = BlogPost.query.first()
    response = client.get(f'/blog/post/{post.id}')
    assert response.status_code == 200
    assert post.title in response.get_data(as_text=True)
    assert post.content in response.get_data(as_text=True)

def login(client, email, password):
    """Helper function to log in a user."""
    # First, GET the login page to retrieve the CSRF token if applicable
    client.get('/auth/login')
    # Then, POST the login form data
    return client.post('/auth/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)



def test_add_post(client, init_database):
    """Test adding a new blog post."""
    login(client, 'admin@example.com', '121212')
    response = client.post('/blog/add', data={
        'title': 'New Post',
        'content': 'Content for new post',
        'author': 'Admin'
    }, follow_redirects=True)
    assert 'New Post' in response.get_data(as_text=True)
    assert 'Post created successfully!' in response.get_data(as_text=True)

def test_edit_post(client, init_database):
    """Test editing an existing blog post."""
    login(client, 'admin@example.com', '121212')
    post = BlogPost.query.first()
    response = client.post(f'/blog/edit/{post.id}', data={
        'title': 'Updated Post',
        'content': 'Updated content here.'
    }, follow_redirects=True)
    assert 'Updated Post' in response.get_data(as_text=True)
    assert 'Post updated successfully!' in response.get_data(as_text=True)

def test_delete_post(client, init_database):
    """Test deleting a blog post."""
    login(client, 'admin@example.com', '121212')
    post = BlogPost.query.first()
    response = client.post(f'/blog/delete/{post.id}', follow_redirects=True)
    assert 'Post deleted successfully!' in response.get_data(as_text=True)
    assert BlogPost.query.get(post.id) is None
