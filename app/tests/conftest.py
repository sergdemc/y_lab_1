from enum import Enum

import pytest
from config import POSTGRES_URL
from database.db import Base, get_session
from database.models import Dish, Menu, Submenu
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine_test = create_engine(POSTGRES_URL)
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base.metadata.create_all(bind=engine_test)


def override_get_session():
    with session_factory() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


client = TestClient(app)


@pytest.fixture
def base_url():
    return 'http://localhost:8000/api/v1'


@pytest.fixture(scope='module')
def get_session():
    with session_factory() as session:
        yield session


@pytest.fixture(scope='module', autouse=True)
def clear_db(get_session):
    db = get_session
    yield db
    db.query(Dish).delete()
    db.query(Submenu).delete()
    db.query(Menu).delete()
    db.commit()
    db.close()


class EntityType(Enum):
    MENU = Menu
    SUBMENU = Submenu
    DISH = Dish


def create_test_entity(model: EntityType, **data):
    session = session_factory()
    model_class = model.value
    entity = model_class(**data)
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity
