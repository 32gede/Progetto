import os
from flask import Flask
from models import User
from flask_session import Session
from routes import main_routes
from database import init_db, get_db_session
from flask_login import LoginManager
from flask_wtf import CSRFProtect

# Create a Flask application instance
app = Flask(__name__, template_folder='templates')
app.jinja_env.autoescape = True

# Configure the upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure session to use the filesystem
app.config['SESSION_TYPE'] = 'filesystem'

# Enable CSRF protection and configure the secret key
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change to a secure and complex secret key
csrf = CSRFProtect(app)
Session(app)

# Initialize the database
init_db()

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'


@login_manager.user_loader
def load_user(user_id):
    """
    Load a user from the database by user ID.

    Args:
        user_id (int): The ID of the user to load.

    Returns:
        User: The user instance, detached from the session.
    """
    with get_db_session() as db_session:
        user = db_session.get(User, int(user_id))
        db_session.expunge(user)  # Detach the user instance from the session
        return user


# Register the main routes blueprint
app.register_blueprint(main_routes)

if __name__ == '__main__':
    # Run the Flask application
    app.run(host='0.0.0.0', port=5000, debug=True)