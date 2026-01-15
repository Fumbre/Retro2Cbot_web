from dotenv import load_dotenv
import os
from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from fastapi import FastAPI,Request

# load value of configurations from .env file
load_dotenv()
#get database information.
DB_IP = os.environ.get("DB_IP")
DB_PORT = os.environ.get("DB_PORT")
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_CONFIGURATION = os.environ.get("DB_CONFIGURATION")

DATABASE_URL = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_IP}:{DB_PORT}/{DB_NAME}{DB_CONFIGURATION}"

# create database connection engine
engine = create_engine(
    DATABASE_URL, # database url
    echo=False, # print SQL in log file
    pool_size=10, # the size of connection pool
    max_overflow=20 # if number that connect to database is greater than pool_size, it allow to create the max number of connection
)

# db session factory
SessionLocal = sessionmaker(
    bind=engine, # database engine
    autocommit=False, # commit data to database. if it is false, it need to use db.commit() function
    autoflush=False # update, delete and create data in database temporaily. if it need to change or create data into database really, it should execute commit function.
)

# SQLAlchemy ORM basic class
class Base(DeclarativeBase):
    pass # mention there is no other properties. In this case, it just extend DeclarativeBase class.


@asynccontextmanager # it is a kind of async application context management container.
async def lifeSpan(app:FastAPI):
    # create tables in database when application starting
    Base.metadata.create_all(bind=engine)
    print("Database tables created")
    yield # there is nothing to execute when application is running.
    print("Server shutdown") # execute this code when application is closing.

# create FastAPI instance. It is a kind of application starter variable.
app = FastAPI(lifespan=lifeSpan)

# http request filter. it means if clients want to request some APIs, before requesting these API, it should execute this part.
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal() # create db session for every client before requesting API
    try:
        response = await call_next(request) # execute next filter. In this case, it has only this filter. Therefore, call_next should execute real API.
    finally:
        request.state.db.close() # execute db connection close function when finished API request.
    return response