from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
import os
from dotenv import load_dotenv, dotenv_values
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("db_url")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

class Base(DeclarativeBase):
    pass

## Create a session / Dependency injection 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()