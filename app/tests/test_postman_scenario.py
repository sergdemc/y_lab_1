from typing import Callable, Generator

import pytest
from database.models import Dish, Menu, Submenu
from sqlalchemy.orm import Session
from tests.conftest import EntityType, client, create_test_entity


class TestPostmanScenario:
    @pytest.fixture(scope='module', autouse=True)
    def clear_db(self, get_db: Session) -> Generator[Session, None, None]:
        db = get_db
        yield db
        db.query(Dish).delete()
        db.query(Submenu).delete()
        db.query(Menu).delete()
        db.commit()
        db.close()

    @pytest.fixture(scope='module', autouse=True)
    def prepare_test_data(self, get_db: Session) -> Generator[tuple[Session, Menu, Submenu, Dish, Dish], None, None]:

        session = get_db
        menu: Menu = create_test_entity(
            EntityType.MENU,
            title='menu1',
            description='description menu1'
        )
        submenu: Submenu = create_test_entity(
            EntityType.SUBMENU,
            title='submenu1',
            description='description submenu1',
            menu_id=menu.id
        )
        dish_1: Dish = create_test_entity(
            EntityType.DISH,
            title='dish1',
            description='description dish1',
            price='100',
            submenu_id=submenu.id
        )
        dish_2: Dish = create_test_entity(
            EntityType.DISH,
            title='dish2',
            description='description dish2',
            price='200',
            submenu_id=submenu.id
        )
        yield session, menu, submenu, dish_1, dish_2
        session.query(Menu).delete()
        session.commit()

    def test_read_menu(
            self,
            get_reverse: Callable,
            prepare_test_data: tuple[Session, Menu, Submenu, Dish, Dish]
    ) -> None:
        session, menu, *_ = prepare_test_data
        response = client.get(url=get_reverse('read_menu', menu_id=menu.id))
        assert response.status_code == 200
        assert response.json()['id'] == str(menu.id)
        assert response.json()['submenus_count'] == 1
        assert response.json()['dishes_count'] == 2

    def test_read_submenu(
            self,
            get_reverse: Callable,
            prepare_test_data: tuple[Session, Menu, Submenu, Dish, Dish]
    ) -> None:
        session, menu, submenu, *_ = prepare_test_data
        response = client.get(
            url=get_reverse('read_submenu', menu_id=menu.id, submenu_id=submenu.id)
        )
        assert response.status_code == 200
        assert response.json()['id'] == str(submenu.id)
        assert response.json()['dishes_count'] == 2

    def test_delete_submenu(
            self,
            get_reverse: Callable,
            prepare_test_data: tuple[Session, Menu, Submenu, Dish, Dish]
    ) -> None:
        session, menu, submenu, *_ = prepare_test_data
        response = client.delete(
            url=get_reverse('delete_submenu', menu_id=menu.id, submenu_id=submenu.id)
        )
        assert response.status_code == 200
        assert response.json()['id'] == str(submenu.id)

        response = client.get(
            url=get_reverse('read_submenus', menu_id=menu.id)
        )
        assert response.status_code == 200
        assert response.json() == []

    def test_read_dishes(
            self,
            get_reverse: Callable,
            prepare_test_data: tuple[Session, Menu, Submenu, Dish, Dish]
    ) -> None:
        session, menu, submenu, *_ = prepare_test_data
        response = client.get(
            url=get_reverse('read_dishes', menu_id=menu.id, submenu_id=submenu.id)
        )
        assert response.status_code == 200
        assert response.json() == []

    def test_delete_menu(
            self,
            get_reverse: Callable,
            prepare_test_data: tuple[Session, Menu, Submenu, Dish, Dish]
    ) -> None:
        session, menu, *_ = prepare_test_data
        response = client.delete(
            url=get_reverse('delete_menu', menu_id=menu.id)
        )
        assert response.status_code == 200
        assert response.json()['id'] == str(menu.id)

        response = client.get(
            url=get_reverse('read_menus')
        )
        assert response.status_code == 200
        assert response.json() == []
