from enum import Enum
from typing import Callable, Generator

import pytest
from config import POSTGRES_URL
from database.db import Base, get_session
from database.models import Dish, Menu, Submenu
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

engine_test = create_engine(POSTGRES_URL)
session_factory = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test
)

Base.metadata.create_all(bind=engine_test)


def override_get_session() -> Generator[Session, None, None]:
    with session_factory() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


client: TestClient = TestClient(app)


@pytest.fixture
def get_reverse() -> Callable:
    return reverse


def reverse(route_name: str, **path_params) -> str:
    for route in app.router.routes:
        if route.name == route_name:
            return route.path_format.format_map(path_params)
    raise ValueError(f"No route found with name '{route_name}'")


@pytest.fixture
def base_url() -> str:
    return 'http://localhost:8000/api/v1'


@pytest.fixture(scope='module')
def get_db() -> sessionmaker:
    with session_factory() as session:
        yield session


@pytest.fixture(autouse=True)
def clear_db(get_db: Generator[Session, None, None]) -> Generator[Session, None, None]:
    db = get_db  # type: Session
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


def create_test_entity(model: EntityType, **data: str) -> Menu | Submenu | Dish:
    session = session_factory()
    model_class = model.value
    entity = model_class(**data)
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity
