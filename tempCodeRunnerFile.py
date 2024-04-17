import sqlalchemy as sq
from sqlalchemy import table
from sqlalchemy.orm import sessionmaker


engine = sq.create_engine('postgresql+psycopg2://Prova:1234@localhost/Prova')  
base=table('login', sq.MetaData(), autoload=True, autoload_with=engine)
Session = sessionmaker(bind=engine)

try:
    # Connect to the database (implicit with session creation)
    session = Session()

    # Fetch all users (assuming you want to retrieve all data)
    users = session.query(base).all()

    for user in users:
        print(f"Email: {user.email}, Password (hashed): {user.pssw}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the session to release resources
    session.close()
