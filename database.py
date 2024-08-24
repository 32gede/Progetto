import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from models import Base
from contextlib import contextmanager

# Database connection URL
DATABASE_URL = 'postgresql://Progetto_owner:pQxVqHj8hG7R@ep-aged-snow-a24c6vx8.eu-central-1.aws.neon.tech/Progetto?sslmode=require'

# Create an SQLAlchemy engine with connection pooling
engine = sa.create_engine(
    DATABASE_URL,
    pool_size=10,  # Configure the connection pool size
    max_overflow=5  # Allow up to 5 connections to overflow
)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)


@contextmanager
def get_db_session():
    """
    Provide a transactional scope around a series of operations.

    Yields:
        Session: A SQLAlchemy session object.
    """
    session = Session()
    try:
        yield session
    finally:
        session.close()


def init_db():
    """
    Initialize the database by creating all tables defined in the metadata.

    This function uses the metadata from the Base class to create all tables
    in the database if they do not already exist.
    """
    Base.metadata.create_all(engine)