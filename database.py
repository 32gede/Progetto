import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from models import Base
from contextlib import contextmanager

DATABASE_URL = 'postgresql://Progetto_owner:pQxVqHj8hG7R@ep-aged-snow-a24c6vx8.eu-central-1.aws.neon.tech/Progetto?sslmode=require'

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
