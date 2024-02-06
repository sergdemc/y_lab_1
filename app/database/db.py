from typing import Generator

from config import POSTGRES_URL
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm.session import Session

engine: Engine = create_engine(POSTGRES_URL)
session_factory: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_session() -> Generator[Session, None, None]:
    with session_factory() as session:
        yield session
