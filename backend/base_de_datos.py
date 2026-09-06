import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

session_factory = sessionmaker(bind=engine)

def get_db_session():
    session = session_factory()

    try:
        yield session
    finally:
        session.close()


class Base(DeclarativeBase):
    pass