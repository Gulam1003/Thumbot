"""
Configuration Module

This module loads environment variables and provides the application configuration
through the Config class.

Modules:
- os: Provides a portable way of using operating system-dependent functionality.
- dotenv: Loads environment variables from a .env file.

Classes:
- Config: A configuration class that stores various configuration settings loaded
  from environment variables.

Environment Variables:
- SECRET_KEY: The secret key for the Flask application.
- SQLALCHEMY_DATABASE_URI: The database URI for SQLAlchemy.
- ADMIN_EMAIL: The email address of the admin user.
- DALLE_API_KEY: The API key for accessing OpenAI's DALL-E model.

Usage:
This module should be imported and the Config class should be used to access the
configuration settings.

Example:
    from config import Config

    app.config.from_object(Config)
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    A configuration class that loads and stores environment variables.
    """
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    DALLE_API_KEY = os.getenv('DALLE_API_KEY')
