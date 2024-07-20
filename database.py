import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = 'postgresql+psycopg2://prova:1234@localhost/Prova'

def init_db():
    engine = sq.create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

def get_db_session():
    engine = sq.create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()
