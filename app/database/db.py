from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import POSTGRES_URL

engine = create_engine(POSTGRES_URL)
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_session():
    with session_factory() as session:
        yield session
