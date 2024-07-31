from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from openai import OpenAI
import os

import openai

# Initialize SQLAlchemy outside of create_app to make it globally accessible
db = SQLAlchemy()

def create_app(test_config=None):
    """
    Create and configure the Flask application.

    Args:
        test_config (dict, optional): Optional settings for testing.

    Returns:
        Flask: Configured Flask application instance.

    This function sets up the Flask app, configures the database, registers blueprints,
    and defines the main routes. It loads configurations from a `config.Config` object
    or a provided test configuration dictionary.
    """
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object('config.Config')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
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
        Handle thumbnail generation and show the generator page.

        Methods:
            GET: Render the thumbnail generator page.
            POST: Generate a thumbnail based on user input and return the image URL as JSON.

        Returns:
            Response: The rendered thumbnail generator template or JSON response with the generated thumbnail URL.
        """
        if 'user' not in session:
            flash('Please log in to access the thumbnail generator.', 'warning')
            return redirect(url_for('auth.login'))
        if request.method == 'POST':
            data = request.get_json()
            prompt = data.get('prompt')
            if not prompt:
                return jsonify({'error': 'Prompt is required'}), 400
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    n=1
                )
                image_url = response.data[0].url
                return jsonify({'image_url': image_url})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
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
