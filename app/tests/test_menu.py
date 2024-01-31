import pytest
from database.models import Menu
from tests.conftest import EntityType, client, create_test_entity


class TestMenu:
    @pytest.fixture
    def prepare_test_data(self, get_session):
        session = get_session
        menu = create_test_entity(
            EntityType.MENU,
            title='menu1',
            description='description menu1'
        )
        yield session, menu
        session.query(Menu).delete()
        session.commit()

    def test_read_empty_menus(self, base_url):
        response = client.get(
            f'{base_url}/menus'
        )
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_create_menu(self, base_url, get_session):
        menu_data = {
            "title": "menu1",
            "description": "description menu1"
        }
        response = client.post(
            f"{base_url}/menus",
            json=menu_data
        )
        assert response.status_code == 201
        created_menu = response.json()
        assert created_menu["title"] == menu_data["title"]
        assert created_menu["description"] == menu_data["description"]

        session = get_session
        db_menu = session.query(Menu).filter(Menu.id == created_menu['id']).first()
        assert str(db_menu.id) == created_menu['id']
        assert db_menu.title == menu_data['title']
        assert db_menu.description == menu_data['description']

    def test_create_menu_with_existing_title(self, base_url, prepare_test_data):
        session, menu = prepare_test_data
        response = client.post(
            f'{base_url}/menus',
            json={
                'title': 'menu1',
                'description': 'description new menu1'
            }
        )
        assert response.status_code == 400
        assert response.json()['detail'] == 'menu exists'

    def test_read_menu(self, base_url, get_session, prepare_test_data):
        session, menu = prepare_test_data
        response = client.get(f"{base_url}/menus/{menu.id}")
        assert response.status_code == 200
        assert response.json()["id"] == str(menu.id)
        assert response.json()["title"] == menu.title

    def test_read_menu_with_invalid_id(self, base_url):
        invalid_id = 'c11907df-84fe-481c-94fa-fdc9fcab34b0'
        response = client.get(
            f'{base_url}/menus/{invalid_id}'
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'menu not found'

    def test_read_menu_with_not_uuid_id(self, base_url):
        response = client.get(
            f'{base_url}/menus/123'
        )
        assert response.status_code == 422
        assert response.json()['detail'][0]['type'] == 'uuid_parsing'

    def test_read_menus(self, base_url, prepare_test_data):
        session, menu = prepare_test_data
        response = client.get(
            f'{base_url}/menus'
        )
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]['id'] == str(menu.id)
        assert response.json()[0]['title'] == 'menu1'
        assert response.json()[0]['description'] == 'description menu1'

    def test_update_menu(self, base_url, get_session, prepare_test_data):
        session, menu = prepare_test_data
        menu_data = {
            "title": "updated menu1",
            "description": "updated description menu1"
        }
        response = client.patch(
            f'{base_url}/menus/{menu.id}',
            json=menu_data
        )
        assert response.status_code == 200
        assert response.json()['id'] == str(menu.id)
        assert response.json()['title'] == menu_data['title']
        assert response.json()['description'] == menu_data['description']

        db_menu = session.query(Menu).filter(Menu.id == menu.id).first()
        assert db_menu.title == menu_data['title']
        assert db_menu.description == menu_data['description']

    def test_update_menu_with_invalid_id(self, base_url):
        invalid_id = 'c11907df-84fe-481c-94fa-fdc9fcab34b0'

        menu_data = {
            "title": "updated menu1",
            "description": "updated description menu1"
        }

        response = client.patch(
            f'{base_url}/menus/{invalid_id}',
            json=menu_data
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'menu not found'

    def test_delete_menu(self, base_url, prepare_test_data):
        session, menu = prepare_test_data
        response = client.delete(
            f'{base_url}/menus/{menu.id}'
        )
        assert response.status_code == 200
        assert response.json()['id'] == str(menu.id)

        db_menu = session.query(Menu).filter(Menu.id == menu.id).first()
        assert db_menu is None
