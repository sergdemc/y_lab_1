from typing import Generator

import pytest
from database.models import Dish, Menu
from sqlalchemy.orm import Session
from tests.conftest import EntityType, client, create_test_entity


class TestDish:
    @pytest.fixture
    def prepare_test_data(self, get_db) -> Generator[tuple[Session, Menu, Menu, Dish, Dish], None, None]:
        session = get_db
        menu = create_test_entity(
            EntityType.MENU,
            title='menu1',
            description='description menu1'
        )
        submenu = create_test_entity(
            EntityType.SUBMENU,
            title='submenu1',
            description='description submenu1',
            menu_id=menu.id
        )
        dish_1 = create_test_entity(
            EntityType.DISH,
            title='dish1',
            description='description dish1',
            price='100.00',
            submenu_id=submenu.id
        )
        dish_2 = create_test_entity(
            EntityType.DISH,
            title='dish2',
            description='description dish2',
            price='200.00',
            submenu_id=submenu.id
        )
        yield session, menu, submenu, dish_1, dish_2
        session.query(Menu).delete()
        session.commit()

    def test_read_empty_dishes(self, get_app) -> None:
        menu = create_test_entity(
            EntityType.MENU,
            title='menu1',
            description='description menu1'
        )
        submenu = create_test_entity(
            EntityType.SUBMENU,
            title='submenu1',
            description='description submenu1',
            menu_id=menu.id
        )
        assert submenu.menu_id == menu.id

        response = client.get(
            url=get_app.url_path_for('read_dishes', menu_id=menu.id, submenu_id=submenu.id)
        )
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_create_dish(self, get_app, get_db) -> None:
        menu = create_test_entity(
            EntityType.MENU,
            title='menu1',
            description='description menu1'
        )
        submenu = create_test_entity(
            EntityType.SUBMENU,
            title='submenu1',
            description='description submenu1',
            menu_id=menu.id
        )
        dish_data = {
            'title': 'dish1',
            'description': 'description dish1',
            'price': '100'
        }
        response = client.post(
            url=get_app.url_path_for('create_dish', menu_id=menu.id, submenu_id=submenu.id),
            json=dish_data
        )
        assert response.status_code == 201
        assert response.json()['title'] == dish_data['title']
        assert response.json()['description'] == dish_data['description']
        assert response.json()['price'] == dish_data['price']

        session = get_db
        db_dish = session.query(Dish).filter(Dish.id == response.json()['id']).first()
        assert db_dish.title == dish_data['title']
        assert db_dish.description == dish_data['description']
        assert db_dish.price == dish_data['price']

    def test_create_dish_with_existing_title(self, get_app, prepare_test_data) -> None:
        session, menu, submenu, dish1, *_ = prepare_test_data
        dish_data = {
            'title': dish1.title,
            'description': 'description new dish1',
            'price': '150'
        }
        response = client.post(
            url=get_app.url_path_for('create_dish', menu_id=menu.id, submenu_id=submenu.id),
            json=dish_data
        )
        assert response.status_code == 400
        assert response.json()['detail'] == 'dish exists'

    def test_read_dish(self, get_app, prepare_test_data) -> None:
        session, menu, submenu, dish, *_ = prepare_test_data
        response = client.get(
            url=get_app.url_path_for('read_dish', menu_id=menu.id, submenu_id=submenu.id, dish_id=dish.id)
        )
        assert response.status_code == 200
        assert response.json()['id'] == str(dish.id)
        assert response.json()['title'] == dish.title

    def test_read_dish_with_invalid_id(self, get_app, prepare_test_data) -> None:
        invalid_id = 'c11907df-84fe-481c-94fa-fdc9fcab34b0'
        session, menu, submenu, dish, *_ = prepare_test_data
        response = client.get(
            url=get_app.url_path_for('read_dish', menu_id=menu.id, submenu_id=submenu.id, dish_id=invalid_id)
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'dish not found'

    def test_read_dish_with_not_uuid_id(self, get_app, prepare_test_data) -> None:
        session, menu, submenu, *_ = prepare_test_data
        response = client.get(
            url=get_app.url_path_for('read_dish', menu_id=menu.id, submenu_id=submenu.id, dish_id='123')
        )
        assert response.status_code == 422
        assert response.json()['detail'][0]['type'] == 'uuid_parsing'

    def test_read_dishes(self, get_app, prepare_test_data) -> None:
        session, menu, submenu, dish1, dish2 = prepare_test_data
        response = client.get(
            url=get_app.url_path_for('read_dishes', menu_id=menu.id, submenu_id=submenu.id)
        )
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]['id'] == str(dish1.id)
        assert response.json()[0]['title'] == dish1.title
        assert response.json()[0]['description'] == dish1.description
        assert response.json()[0]['price'] == dish1.price

        assert response.json()[1]['id'] == str(dish2.id)
        assert response.json()[1]['title'] == dish2.title
        assert response.json()[1]['description'] == dish2.description
        assert response.json()[1]['price'] == dish2.price

    def test_update_dish(self, get_app, prepare_test_data) -> None:
        session, menu, submenu, dish, *_ = prepare_test_data
        dish_data = {
            'title': 'updated dish1',
            'description': 'updated description dish1',
            'price': '200'
        }
        response = client.patch(
            url=get_app.url_path_for('update_dish', menu_id=menu.id, submenu_id=submenu.id, dish_id=dish.id),
            json=dish_data
        )
        assert response.status_code == 200
        assert response.json()['id'] == str(dish.id)
        assert response.json()['title'] == dish_data['title']
        assert response.json()['description'] == dish_data['description']
        assert response.json()['price'] == dish_data['price']

        db_dish = session.query(Dish).filter(Dish.id == dish.id).first()
        assert db_dish.title == dish_data['title']
        assert db_dish.description == dish_data['description']
        assert db_dish.price == dish_data['price']

    def test_update_dish_with_invalid_id(self, get_app, prepare_test_data) -> None:
        session, menu, submenu, dish, *_ = prepare_test_data
        invalid_id = 'c11907df-84fe-481c-94fa-fdc9fcab34b0'
        dish_data = {
            'title': 'updated dish1',
            'description': 'updated description dish1',
            'price': '200'
        }
        response = client.patch(
            url=get_app.url_path_for('update_dish', menu_id=menu.id, submenu_id=submenu.id, dish_id=invalid_id),
            json=dish_data
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'dish not found'

    def test_update_dish_with_invalid_menu_id(self, get_app, prepare_test_data) -> None:
        session, menu, submenu, dish, *_ = prepare_test_data
        invalid_id = 'c11907df-84fe-481c-94fa-fdc9fcab34b0'
        dish_data = {
            'title': 'updated dish1',
            'description': 'updated description dish1',
            'price': '200'
        }
        response = client.patch(
            url=get_app.url_path_for('update_dish', menu_id=invalid_id, submenu_id=submenu.id, dish_id=dish.id),
            json=dish_data
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'menu not found'

    def test_update_dish_with_invalid_submenu_id(self, get_app, prepare_test_data) -> None:
        session, menu, submenu, dish, *_ = prepare_test_data
        invalid_id = 'c11907df-84fe-481c-94fa-fdc9fcab34b0'
        dish_data = {
            'title': 'updated dish1',
            'description': 'updated description dish1',
            'price': '200'
        }
        response = client.patch(
            url=get_app.url_path_for('update_dish', menu_id=menu.id, submenu_id=invalid_id, dish_id=dish.id),
            json=dish_data
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'submenu not found'

    def test_delete_dish(self, get_app, prepare_test_data) -> None:
        session, menu, submenu, dish1, dish2 = prepare_test_data
        response = client.delete(
            url=get_app.url_path_for('delete_dish', menu_id=menu.id, submenu_id=submenu.id, dish_id=dish1.id)
        )
        assert response.status_code == 200
        assert response.json()['id'] == str(dish1.id)

        response = client.delete(
            url=get_app.url_path_for('delete_dish', menu_id=menu.id, submenu_id=submenu.id, dish_id=dish2.id)
        )
        assert response.status_code == 200
        assert response.json()['id'] == str(dish2.id)

        response = client.get(
            url=get_app.url_path_for('read_dishes', menu_id=menu.id, submenu_id=submenu.id)
        )
        assert response.status_code == 200
        assert response.json() == []
