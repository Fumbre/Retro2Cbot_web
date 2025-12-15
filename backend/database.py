from dotenv import load_dotenv
import os
from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from fastapi import FastAPI,Request

# load .env file
load_dotenv()
DB_IP = os.environ.get("DB_IP")
DB_PORT = os.environ.get("DB_PORT")
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_CONFIGURATION = os.environ.get("DB_CONFIGURATION")


DATABASE_URL = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_IP}:{DB_PORT}/{DB_NAME}{DB_CONFIGURATION}"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

class Base(DeclarativeBase):
    pass


@asynccontextmanager
async def lifeSpan(app:FastAPI):
    # create table
    Base.metadata.create_all(bind=engine)
    print("Database tables created")
    yield
    print("Server shutdown")

app = FastAPI(lifespan=lifeSpan)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    try:
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response