from flask import Flask
from models import User
from flask_session import Session
from routes import main_routes
from database import init_db, get_db_session
from flask_login import LoginManager
from flask_wtf import CSRFProtect
# from flask_talisman import Talisman - Permette di configurare Content Security Policy (CSP) per proteggere
#                                       l'applicazione da attacchi XSS (Cross-Site Scripting) e per configurare altre
#                                       politiche di sicurezza (tipo https).

app = Flask(__name__, template_folder='templates')
app.jinja_env.autoescape = True
app.config['SESSION_TYPE'] = 'filesystem'
# csrf = CSRFProtect(app)
Session(app)

'''
# Configura CSP per permettere stili e script da specifiche fonti
csp = {
    'default-src': "'self'",
    'script-src': ["'self'", 'https://cdn.jsdelivr.net'],
    'style-src': ["'self'", 'https://cdn.jsdelivr.net'],
    'font-src': ["'self'", 'https://cdn.jsdelivr.net'],
}

Talisman(app, content_security_policy=csp)  # Configura Talisman con la tua CSP personalizzata
'''

init_db()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'


@login_manager.user_loader
def load_user(user_id):
    with get_db_session() as db_session:
        return db_session.query(User).get(int(user_id))


app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(debug=True)
