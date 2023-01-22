from fastapi import FastAPI
import psycopg
import time
from . import models
from .database import engine, get_db
from .routers import task, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# cursor_factory = RealDictCursor (from psycopg2.extras import RealDictCursor)
# Above parameter will give the column name as well.
# psycopg2 library does not return the column name from a query so we need to add this parameter.
# cursor_factory = RealDictCursor
while True:
    try:
        # Connect to an existing database
        conn = psycopg.connect(host='localhost', dbname='pma',
                               user='postgres', password='8460')
        # Open a cursor to perform database operations
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(4)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(task.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
