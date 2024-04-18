from flask import Flask, make_response,render_template,request,redirect
import requests
from flask_session import Session
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, select
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class User(Base):
      __tablename__ = 'login'  # Specify the table name
      id = Column(Integer, primary_key=True, nullable=False)
      email = Column(String(255), nullable=False)
      pssw = Column(String(255), nullable=False)
def connect():
  engine = sq.create_engine('postgresql+psycopg2://Prova:1234@localhost/Prova')  
  session= sessionmaker(bind=engine)
  return session()

app=Flask(__name__,template_folder='templates')
@app.route('/')
def index():
  if request.cookies.get('id') :
     print (request.cookies.get('id'))
  else:
    print('NO')
  return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        print(username, password)
        session=connect()
        result=session.query(User).filter_by(email=username, pssw=password)
        if result.first():
          user_id = result.first().id
          url = 'http://localhost:5000/set_data'
          data = {'id': user_id}
          requests.post(url, json=data)
          return redirect('/')
        else:
          print('NO')
          return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

@app.route('/set_data',methods=['POST']) 
def set_data(): 
    if request.method == 'POST':
      user_id = request.json['id']
      response=make_response('')
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
        session = connect()
        result=session.query(User).filter_by(email=email)
        if not result.first():
            session.add(user)
            session.commit()
            return redirect('/login')
        else:
            return render_template('registration.html', error='User already exists')
   else:
       return render_template('registration.html')