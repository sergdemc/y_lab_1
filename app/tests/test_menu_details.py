import pytest
from database.models import Menu
from tests.conftest import EntityType, client, create_test_entity


class TestMenu:

    @pytest.fixture(scope='module', autouse=True)
    def prepare_test_data(self, get_session):
        session = get_session
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
            price=100,
            submenu_id=submenu.id
        )
        dish_2 = create_test_entity(
            EntityType.DISH,
            title='dish2',
            description='description dish2',
            price=200,
            submenu_id=submenu.id
        )
        yield session, menu, submenu, dish_1, dish_2
        session.query(Menu).delete()
        session.commit()

    def test_read_menu(self, base_url, prepare_test_data):
        session, menu, *_ = prepare_test_data
        response = client.get(f"{base_url}/menus/{menu.id}")
        assert response.status_code == 200
        assert response.json()["id"] == str(menu.id)
        assert response.json()["submenus_count"] == 1
        assert response.json()["dishes_count"] == 2

    def test_read_submenu(self, base_url, prepare_test_data):
        session, menu, submenu, *_ = prepare_test_data
        response = client.get(
            f'{base_url}/menus/{menu.id}/submenus/{submenu.id}'
        )
        assert response.status_code == 200
        assert response.json()["id"] == str(submenu.id)
        assert response.json()["dishes_count"] == 2

    def test_delete_submenu(self, base_url, prepare_test_data):
        session, menu, submenu, *_ = prepare_test_data
        response = client.delete(
            f'{base_url}/menus/{menu.id}/submenus/{submenu.id}'
        )
        assert response.status_code == 200
        assert response.json()["id"] == str(submenu.id)

        response = client.get(
            f'{base_url}/menus/{menu.id}/submenus'
        )
        assert response.status_code == 200
        assert response.json() == []

    def test_read_dishes(self, base_url, prepare_test_data):
        session, menu, submenu, *_ = prepare_test_data
        response = client.get(
            f'{base_url}/menus/{menu.id}/submenus/{submenu.id}/dishes'
        )
        assert response.status_code == 200
        assert response.json() == []

    def test_delete_menu(self, base_url, prepare_test_data):
        session, menu, *_ = prepare_test_data
        response = client.delete(
            f'{base_url}/menus/{menu.id}'
        )
        assert response.status_code == 200
        assert response.json()["id"] == str(menu.id)

        response = client.get(
            f'{base_url}/menus'
        )
        assert response.status_code == 200
        assert response.json() == []
