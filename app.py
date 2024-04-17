from flask import Flask,render_template,request,redirect
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer
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
  return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        print(username, password)
        session=connect()
        if session.query(User).filter_by(email=username, pssw=password).first():
          return redirect('/')
        else:
          print('NO')
          return redirect('/')
        

    else:
        # Handle GET request (display login page)
        return render_template('login.html')