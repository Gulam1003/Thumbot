"""
Models Module

This module defines the database models for the Thumbot application using SQLAlchemy.
It includes models for User and BlogPost with relevant fields and methods.

Modules:
- flask_sqlalchemy: Provides support for SQLAlchemy in Flask applications.
- werkzeug.security: Provides password hashing and checking utilities.
- datetime: Provides classes for manipulating dates and times.

Classes:
- User: Represents a user in the application with fields for email, password hash, name, and surname.
    - set_password(password): Sets the user's password hash.
    - check_password(password): Checks the user's password against the stored hash.
- BlogPost: Represents a blog post in the application with fields for title, content, author, and date posted.
    - __repr__(): Returns a string representation of the blog post.

Usage:
Import this module to interact with the database models for users and blog posts.

Example:
    from models import db, User, BlogPost

    # Create a new user
    user = User(email='example@example.com', name='John', surname='Doe')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """
    User Model

    Represents a user in the application.

    Fields:
    - id (int): Primary key, unique identifier for the user.
    - email (str): Unique email address of the user.
    - password_hash (str): Hashed password of the user.
    - name (str): First name of the user.
    - surname (str): Surname of the user.

    Methods:
    - set_password(password): Sets the user's password hash.
    - check_password(password): Checks the user's password against the stored hash.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)

    def set_password(self, password):
        """
        Sets the user's password hash.

        Args:
            password (str): The password to be hashed and stored.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks the user's password against the stored hash.

        Args:
            password (str): The password to be checked.

        Returns:
            bool: True if the password matches the stored hash, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

class BlogPost(db.Model):
    """
    BlogPost Model

    Represents a blog post in the application.

    Fields:
    - id (int): Primary key, unique identifier for the blog post.
    - title (str): Title of the blog post.
    - content (str): Content of the blog post.
    - author (str): Author of the blog post.
    - date_posted (datetime): Date and time the blog post was created.

    Methods:
    - __repr__(): Returns a string representation of the blog post.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """
        Returns a string representation of the blog post.

        Returns:
            str: String representation of the blog post.
        """
        return f'<Post {self.title}>'
