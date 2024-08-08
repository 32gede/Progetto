import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from models import Base
from contextlib import contextmanager

DATABASE_URL = 'postgresql+psycopg2://prova:1234@localhost/Prova'

engine = sa.create_engine(
    DATABASE_URL,
    pool_size=10,  # Configura il pool di connessioni
    max_overflow=5
)
Session = sessionmaker(bind=engine)

@contextmanager
def get_db_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()

def init_db():
    Base.metadata.create_all(engine)
