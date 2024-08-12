import os
from flask import Flask
from models import User
from flask_session import Session
from routes import main_routes
from database import init_db, get_db_session
from flask_login import LoginManager
from flask_wtf import CSRFProtect

app = Flask(__name__, template_folder='templates')
app.jinja_env.autoescape = True

# Configure the upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize database
init_db()


# Configure login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    with get_db_session() as db_session:
        return db_session.query(User).get(int(user_id))

# Register the main blueprint
app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(debug=True)
