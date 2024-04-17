import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = sq.create_engine('postgresql+psycopg2://Prova:1234@localhost/Prova')  
class User(Base):
    __tablename__ = 'login'  # Specify the table name
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False)
    pssw = Column(String(255), nullable=False)
Session = sessionmaker(bind=engine)

try:
    # Connect to the database (implicit with session creation)
    session = Session()

    # Fetch all users (assuming you want to retrieve all data)
    users = session.query(User).all()

    for user in users:
        print(f"ID:{user.id} Email: {user.email}, Password (hashed): {user.pssw}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    session.close()


def connect():
  Base = declarative_base()
  engine = sq.create_engine('postgresql+psycopg2://Prova:1234@localhost/Prova')  
  class User(Base):
      __tablename__ = 'login'  # Specify the table name
      id = Column(Integer, primary_key=True, nullable=False)
      email = Column(String(255), nullable=False)
      pssw = Column(String(255), nullable=False)
  return sessionmaker(bind=engine)

