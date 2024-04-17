from flask import Flask,render_template,request
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
def index():
    if request.method == 'POST':
        # Handle login form submission
        username = request.form['username']
        password = request.form['password']
        session=connect()
        if session.query(User).filter_by(email=username, pssw=password).first():
          return render_template('index.html')
        else:
            return render_template('login.html', error='Invalid username or password')

    else:
        # Handle GET request (display login page)
        return render_template('login.html')