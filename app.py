from flask import Flask
from models import User
from flask_session import Session
from routes import main_routes
from database import init_db, get_db_session
from flask_login import LoginManager

app = Flask(__name__, template_folder='templates')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Inizializza il database
init_db()

# Configure the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'


# Define the user_loader function
@login_manager.user_loader
def load_user(user_id):
    db_session = get_db_session()
    return db_session.query(User).get(int(user_id))


# Registra i blueprint
app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(debug=True)
