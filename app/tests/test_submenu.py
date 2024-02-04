from typing import Generator

import pytest
from database.models import Menu, Submenu
from sqlalchemy.orm import Session
from tests.conftest import EntityType, client, create_test_entity


class TestSubmenu:
    @pytest.fixture
    def prepare_test_data(
            self,
            get_db
    ) -> Generator[tuple[Session, Menu, Submenu], None, None]:

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
        yield session, menu, submenu
        session.query(Menu).delete()
        session.commit()

    def test_read_empty_submenus(self, base_url) -> None:
        menu = create_test_entity(
            EntityType.MENU,
            title='menu1',
            description='description menu1'
        )
        response = client.get(
            f'{base_url}/menus/{menu.id}/submenus'
        )
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_create_submenu(self, base_url, get_db: Session) -> None:
        menu = create_test_entity(
            EntityType.MENU,
            title='menu1',
            description='description menu1'
        )
        submenu_data = {
            'title': 'submenu1',
            'description': 'description submenu1'
        }
        response = client.post(
            f'{base_url}/menus/{menu.id}/submenus',
            json=submenu_data
        )
        assert response.status_code == 201
        created_submenu = response.json()
        assert created_submenu['title'] == submenu_data['title']
        assert created_submenu['description'] == submenu_data['description']

        session = get_db
        db_submenu = (session.query(Submenu)
                      .filter(Submenu.id == created_submenu['id']).first())
        assert db_submenu.title == submenu_data['title']
        assert db_submenu.description == submenu_data['description']

    def test_create_submenu_with_existing_title(
            self, base_url, prepare_test_data
    ) -> None:
        session, menu, *_ = prepare_test_data
        response = client.post(
            f'{base_url}/menus/{menu.id}/submenus',
            json={
                'title': 'submenu1',
                'description': 'description new submenu1'
            }
        )
        assert response.status_code == 400
        assert response.json()['detail'] == 'submenu exists'

    def test_read_submenu(self, base_url, prepare_test_data) -> None:
        session, menu, submenu = prepare_test_data
        response = client.get(
            f'{base_url}/menus/{menu.id}/submenus/{submenu.id}'
        )
        assert response.status_code == 200
        assert response.json()['id'] == str(submenu.id)
        assert response.json()['title'] == submenu.title
        assert response.json()['description'] == submenu.description

    def test_read_submenu_with_invalid_id(self, base_url, prepare_test_data) -> None:
        session, menu, submenu = prepare_test_data
        invalid_id = 'c11907df-84fe-481c-94fa-fdc9fcab34b0'
        response = client.get(
            f'{base_url}/menus/{menu.id}/submenus/{invalid_id}'
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'submenu not found'

    def test_read_submenu_with_not_uuid_id(self, base_url, prepare_test_data) -> None:
        session, menu, submenu = prepare_test_data
        response = client.get(
            f'{base_url}/menus/{menu.id}/submenus/123'
        )
        assert response.status_code == 422
        assert response.json()['detail'][0]['type'] == 'uuid_parsing'

    def test_read_submenus(self, base_url, prepare_test_data):
        session, menu, submenu = prepare_test_data
        response = client.get(
            f'{base_url}/menus/{menu.id}/submenus'
        )
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_update_submenu(self, base_url, prepare_test_data) -> None:
        session, menu, submenu = prepare_test_data
        submenu_data = {
            'title': 'updated submenu1',
            'description': 'updated description submenu1'
        }
        response = client.patch(
            f'{base_url}/menus/{menu.id}/submenus/{submenu.id}',
            json=submenu_data
        )
        assert response.status_code == 200
        assert response.json()['title'] == submenu_data['title']
        assert response.json()['description'] == submenu_data['description']

        db_submenu = session.query(Submenu).filter(Submenu.id == submenu.id).first()
        assert db_submenu.title == submenu_data['title']
        assert db_submenu.description == submenu_data['description']

    def test_update_submenu_with_invalid_id(self, base_url, prepare_test_data) -> None:
        session, menu, submenu = prepare_test_data
        invalid_id = 'c11907df-84fe-481c-94fa-fdc9fcab34b0'
        submenu_data = {
            'title': 'updated submenu1',
            'description': 'updated description submenu1'
        }
        response = client.patch(
            f'{base_url}/menus/{menu.id}/submenus/{invalid_id}',
            json=submenu_data
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'submenu not found'

    def test_update_submenu_with_invalid_menu_id(
            self, base_url, prepare_test_data
    ) -> None:
        session, menu, submenu = prepare_test_data
        invalid_id = 'c11907df-84fe-481c-94fa-fdc9fcab34b0'
        submenu_data = {
            'title': 'updated submenu1',
            'description': 'updated description submenu1'
        }
        response = client.patch(
            f'{base_url}/menus/{invalid_id}/submenus/{submenu.id}',
            json=submenu_data
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'menu not found'

    def test_delete_submenu(self, base_url, prepare_test_data) -> None:
        session, menu, submenu = prepare_test_data
        response = client.delete(
            f'{base_url}/menus/{menu.id}/submenus/{submenu.id}'
        )
        assert response.status_code == 200
        assert response.json()['id'] == str(submenu.id)
        assert response.json()['title'] == submenu.title

        db_submenu = session.query(Submenu).filter(Submenu.id == submenu.id).first()
        assert db_submenu is None
