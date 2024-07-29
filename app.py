from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from openai import OpenAI
import os

# Initialize SQLAlchemy outside of create_app to make it globally accessible
db = SQLAlchemy()

def create_app(test_config=None):
    """
    Factory function to create and configure the Flask application.

    Args:
        test_config (dict, optional): Optional dictionary for test configuration settings.

    Returns:
        Flask: Configured Flask application instance.

    This function sets up the Flask application with configurations, initializes
    database connections, registers blueprints, and defines the main routes.
    It supports loading configurations from a `config.Config` object or a provided
    test configuration dictionary.

    The following features are configured:
    - SQLAlchemy: Database management.
    - Flask-Migrate: Database migrations.
    - OpenAI: Optional initialization of the OpenAI client.

    Routes:
    - `/`: Renders the home page.
    - `/get_started`: Redirects to the thumbnail generator or login page based on user session.
    - `/thumbnail_generator`: Renders the thumbnail generator page, requires user login.
    - `/pricing`: Renders the pricing page.
    - `/contact`: Renders the contact page.
    """
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object('config.Config')
    
    # Initialize db with the app
    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        db.create_all()

    if not app.config.get('TESTING', False):
        client = OpenAI(api_key=app.config.get('DALLE_API_KEY', 'optional-default-key'))

    from auth.routes import auth_bp
    from blog.routes import blog_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(blog_bp, url_prefix='/blog')

    @app.route('/')
    def home():
        """
        Home page route.

        Returns:
            str: Rendered HTML template for the home page.
        """
        return render_template('index.html')

    @app.route('/get_started')
    def get_started():
        """
        Get Started page route.

        Redirects to the thumbnail generator page if the user is logged in,
        otherwise redirects to the login page.

        Returns:
            werkzeug.wrappers.Response: Redirect response.
        """
        if 'user' in session:
            return redirect(url_for('thumbnail_generator'))
        return redirect(url_for('auth.login'))

    @app.route('/thumbnail_generator', methods=['GET', 'POST'])
    def thumbnail_generator():
        """
        Thumbnail generator page route.

        Requires user login. Handles both GET and POST requests.
        For POST requests, handles thumbnail generation logic.

        Returns:
            str: Rendered HTML template for the thumbnail generator page or redirect response.
        """
        if 'user' not in session:
            flash('Please log in to access the thumbnail generator.', 'warning')
            return redirect(url_for('auth.login'))
        # Similar setup for handling POST with thumbnail generation logic
        return render_template('thumbnail_generator.html')

    @app.route('/pricing')
    def pricing():
        """
        Pricing page route.

        Returns:
            str: Rendered HTML template for the pricing page.
        """
        return render_template('pricing.html')

    @app.route('/contact')
    def contact():
        """
        Contact page route.

        Returns:
            str: Rendered HTML template for the contact page.
        """
        return render_template('contact.html')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
