from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import db, User

auth_bp = Blueprint('auth', __name__)

def admin_required(f):
    """
    Decorator to ensure that the user has admin privileges.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function which checks if the user is an admin.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'is_admin' not in session or not session['is_admin']:
            flash('Unauthorized access.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login. Renders the login template and processes login form submissions.

    If the login is successful, sets the user session and redirects to the home page.
    Otherwise, it flashes an error message.

    Returns:
        Response: The rendered login template or a redirect to another route.
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user'] = user.email
            session['username'] = f"{user.name} {user.surname}"  # Store the user's name and surname in the session
            if email == 'admin@example.com':  # Replace with your admin email
                session['is_admin'] = True
            else:
                session['is_admin'] = False
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check your credentials and try again.', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handle user signup. Renders the signup template and processes signup form submissions.

    If the signup is successful, creates a new user and redirects to the login page.
    Otherwise, it flashes an error message.

    Returns:
        Response: The rendered signup template or a redirect to another route.
    """
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(email=email).first():
            flash('Email address already exists.', 'danger')
            return redirect(url_for('auth.signup'))
        
        new_user = User(
            name=name,
            surname=surname,
            email=email
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('signup.html')

@auth_bp.route('/logout')
def logout():
    """
    Handle user logout. Clears the user session and redirects to the login page.

    Returns:
        Response: A redirect to the login page.
    """
    session.pop('user', None)
    session.pop('username', None)
    session.pop('is_admin', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
