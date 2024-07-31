"""
Admin User Creation Script

This script is used to create an admin user for the Thumbot application.
It checks if the admin user already exists in the database and creates one if not.

Modules:
- app: The Flask application instance.
- models: Contains the SQLAlchemy models including the User model.

Usage:
Run this script to create an admin user with the specified email and password.

Variables:
- admin_email (str): The email address of the admin user.
- admin_password (str): The password for the admin user.

Note:
Replace the admin_email and admin_password variables with the desired admin email and password.
"""

from app import app
from models import db, User

with app.app_context():
    admin_email = 'admin@example.com'
    admin_password = 'adminpassword'  

    # Check if the admin user already exists
    admin_user = User.query.filter_by(email=admin_email).first()
    if not admin_user:
        # Create the admin user
        admin_user = User(email=admin_email)
        admin_user.set_password(admin_password)
        db.session.add(admin_user)
        db.session.commit()
        print(f'Admin user {admin_email} created successfully.')
    else:
        print(f'Admin user {admin_email} already exists.')
