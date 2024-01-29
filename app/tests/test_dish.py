from database.models import Dish, Menu, Submenu
from tests.conftest import EntityType, client, create_test_entity


class TestDish:

    def test_read_empty_dishes(self, base_url):
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
            f'{base_url}/menus/{menu.id}/submenus/{submenu.id}/dishes'
        )
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_create_dish(self, base_url, get_session):
        session = get_session
        menu = session.query(Menu).first()
        submenu = session.query(Submenu).first()
        dish_data = {
            "title": "dish1",
            "description": "description dish1",
            "price": "100"
        }
        response = client.post(
            f'{base_url}/menus/{menu.id}/submenus/{submenu.id}/dishes',
            json=dish_data
        )
        assert response.status_code == 201
        assert response.json()["title"] == dish_data["title"]
        assert response.json()["description"] == dish_data["description"]
        assert response.json()["price"] == dish_data["price"]

        db_dish = session.query(Dish).filter(Dish.id == response.json()['id']).first()
        assert str(db_dish.id) == response.json()['id']
        assert db_dish.title == dish_data['title']

    def test_create_dish_with_existing_title(self, base_url, get_session):
        session = get_session
        menu = session.query(Menu).first()
        submenu = session.query(Submenu).first()
        dish_data = {
            "title": "dish1",
            "description": "description dish1",
            "price": "100"
        }
        response = client.post(
            f'{base_url}/menus/{menu.id}/submenus/{submenu.id}/dishes',
            json=dish_data
        )
        assert response.status_code == 400
        assert response.json()['detail'] == 'dish exists'

    def test_read_dish(self, base_url, get_session):
        session = get_session
        menu = session.query(Menu).first()
        submenu = session.query(Submenu).first()
        dish = session.query(Dish).first()
        response = client.get(
            f'{base_url}/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}'
        )
        assert response.status_code == 200
        assert response.json()["id"] == str(dish.id)
        assert response.json()["title"] == dish.title

    def test_read_dish_with_invalid_id(self, base_url, get_session):
        invalid_id = 'c11907df-84fe-481c-94fa-fdc9fcab34b0'
        session = get_session
        menu = session.query(Menu).first()
        submenu = session.query(Submenu).first()
        response = client.get(
            f'{base_url}/menus/{menu.id}/submenus/{submenu.id}/dishes/{invalid_id}'
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'dish not found'

    def test_read_dish_with_not_uuid_id(self, base_url, get_session):
        session = get_session
        menu = session.query(Menu).first()
        submenu = session.query(Submenu).first()
        response = client.get(
            f'{base_url}/menus/{menu.id}/submenus/{submenu.id}/dishes/123'
        )
        assert response.status_code == 422
        assert response.json()['detail'][0]['type'] == 'uuid_parsing'

    def test_read_dishes(self, base_url, get_session):
        session = get_session
        menu = session.query(Menu).first()
        submenu = session.query(Submenu).first()
        dish = session.query(Dish).first()
        response = client.get(
            f'{base_url}/menus/{menu.id}/submenus/{submenu.id}/dishes'
        )
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["id"] == str(dish.id)
        assert response.json()[0]["title"] == dish.title

    def test_update_dish(self, base_url, get_session):
        session = get_session
        menu = session.query(Menu).first()
        submenu = session.query(Submenu).first()
        dish = session.query(Dish).first()
        dish_data = {
            "title": "updated dish1",
            "description": "updated description dish1",
            "price": "200"
        }
        response = client.patch(
            f'{base_url}/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}',
            json=dish_data
        )
        assert response.status_code == 200
        assert response.json()['id'] == str(dish.id)
        assert response.json()['title'] == dish_data['title']
        assert response.json()['description'] == dish_data['description']
        assert response.json()['price'] == dish_data['price']

    def test_update_dish_with_invalid_id(self, base_url, get_session):
        session = get_session
        menu = session.query(Menu).first()
        submenu = session.query(Submenu).first()
        invalid_id = 'c11907df-84fe-481c-94fa-fdc9fcab34b0'
        dish_data = {
            "title": "updated dish1",
            "description": "updated description dish1",
            "price": "200"
        }
        response = client.patch(
            f'{base_url}/menus/{menu.id}/submenus/{submenu.id}/dishes/{invalid_id}',
            json=dish_data
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'dish not found'

    def test_update_dish_with_invalid_menu_id(self, base_url, get_session):
        session = get_session
        invalid_id = 'c11907df-84fe-481c-94fa-fdc9fcab34b0'
        submenu = session.query(Submenu).first()
        dish = session.query(Dish).first()
        dish_data = {
            "title": "updated dish1",
            "description": "updated description dish1",
            "price": "200"
        }
        response = client.patch(
            f'{base_url}/menus/{invalid_id}/submenus/{submenu.id}/dishes/{dish.id}',
            json=dish_data
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'menu not found'

    def test_update_dish_with_invalid_submenu_id(self, base_url, get_session):
        session = get_session
        invalid_id = 'c11907df-84fe-481c-94fa-fdc9fcab34b0'
        menu = session.query(Menu).first()
        dish = session.query(Dish).first()
        dish_data = {
            "title": "updated dish1",
            "description": "updated description dish1",
            "price": "200"
        }
        response = client.patch(
            f'{base_url}/menus/{menu.id}/submenus/{invalid_id}/dishes/{dish.id}',
            json=dish_data
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'submenu not found'
