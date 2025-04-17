from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL") # local SQLite DB

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args= {"check_same_thread": False}
)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


