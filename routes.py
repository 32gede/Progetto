from flask import Blueprint, render_template, request, redirect, session, url_for
from models import User
from database import get_db_session

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    if session.get('id'):
        print(session.get('id'))
    else:
        print('NESSUN cookie')
    return render_template('index.html')

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db_session = get_db_session()
        result = db_session.query(User).filter_by(email=email, password=password).first()
        if result:
            session['id'] = result.id
            return redirect(url_for('main.index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@main_routes.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db_session = get_db_session()
        existing_user = db_session.query(User).filter_by(email=email).first()
        if not existing_user:
            new_user = User(email=email, password=password)
            db_session.add(new_user)
            db_session.commit()
            return redirect(url_for('main.login'))
        return render_template('registration.html', error='User already exists')
    return render_template('registration.html')
