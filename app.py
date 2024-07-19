from flask import Flask, make_response, render_template, request, redirect, session
from flask_session import Session
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Integer

# Definisci il modello User
Base = declarative_base()

class User(Base):
    __tablename__ = 'login'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False)
    pssw = Column(String(255), nullable=False)

# Funzione per connettersi al database
def connect():
    engine = sq.create_engine('postgresql+psycopg2://prova:1234@localhost/Prova')
    Base.metadata.create_all(engine)  # Crea le tabelle se non esistono
    Session = sessionmaker(bind=engine)
    return Session()

# Configurazione dell'app Flask
app = Flask(__name__, template_folder='templates')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def index():
    if session.get('id'):
        print(session.get('id'))
    else:
        print('NESSUN cookie')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        db_session = connect()
        result = db_session.query(User).filter_by(email=username, pssw=password)
        if result.first():
            user_id = result.first().id
            session['id'] = user_id
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

@app.route('/set_data', methods=['POST'])
def set_data():
    if request.method == 'POST':
        user_id = request.json['id']
        response = make_response('')
        response.set_cookie('id', str(user_id))
        return response
    else:
        return render_template('login.html')

def getcookie():
    id = request.cookies.get('id')
    return id

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User(email=email, pssw=password)
        db_session = connect()
        result = db_session.query(User).filter_by(email=email)
        if not result.first():
            db_session.add(user)
            db_session.commit()
            return redirect('/login')
        else:
            return render_template('registration.html', error='User already exists')
    else:
        return render_template('registration.html')

if __name__ == '__main__':
    app.run(debug=True)
