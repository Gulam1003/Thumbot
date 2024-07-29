import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class for the Thumbot application.

    This class loads configuration settings for the application, including database
    settings, secret keys, and API keys. Environment variables are loaded from a .env file.

    Attributes:
    - SQLALCHEMY_DATABASE_URI (str): URI for the SQLAlchemy database.
    - SQLALCHEMY_TRACK_MODIFICATIONS (bool): Flag to disable tracking modifications in SQLAlchemy.
    - SECRET_KEY (str): Secret key for session management and other security-related operations.
    - DALLE_API_KEY (str): API key for accessing the DALLE service.
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///yourdatabase.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key'
    DALLE_API_KEY = 'actual-api-key'
