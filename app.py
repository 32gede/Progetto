from flask import Flask
from flask_session import Session
from routes import main_routes
from database import init_db

app = Flask(__name__, template_folder='templates')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Inizializza il database
init_db()

# Registra i blueprint
app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(debug=True)
