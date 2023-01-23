from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'sqlite://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:8460@localhost/pma"

# engine is responsible for SQLAlchemy to connect with PostgreSQL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
# when we are using SQLlite database we have to pass connect_args parameter
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# when we actualy want to talk to the SQL database we have to use a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():  # Dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# if we don't want to use sqlalchemy then we can connect to the database in the following way
# cursor_factory = RealDictCursor (from psycopg2.extras import RealDictCursor)
# Above parameter will give the column name as well.
# psycopg2 library does not return the column name from a query so we need to add this parameter.
# cursor_factory = RealDictCursor

# import psycopg
# import time

# while True:
#     try:
#         # Connect to an existing database
#         conn = psycopg.connect(host='localhost', dbname='pma',
#                                user='postgres', password='8460')
#         # Open a cursor to perform database operations
#         cursor = conn.cursor()
#         print("Database connection was succesfull")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(4)
