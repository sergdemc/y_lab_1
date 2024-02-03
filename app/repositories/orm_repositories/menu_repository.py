import uuid
from database.db import get_session
from database.models import Menu
from repositories.repositories_interface import IRepository


class MenuORMRepository(IRepository):
    def __init__(self, session=None):
        self.session = session

    def get_all(self) -> list[Menu]:
        try:
            return self.session.query(Menu).all()
        except Exception as e:
            print(e)
            return []

    def get_by_id(self, menu_id: uuid.UUID) -> Menu | None:
        try:
            return self.session.query(Menu).filter(Menu.id == menu_id).first()
        except Exception as e:
            print(e)
            return None

    def get_by_title(self, title: str) -> Menu | None:
        try:
            return self.session.query(Menu).filter(Menu.title == title).first()
        except Exception as e:
            print(e)
            return None

    def create(self, data: dict) -> Menu | None:
        try:
            menu = Menu(**data)
            self.session.add(menu)
            self.session.commit()
            self.session.refresh(menu)
            return menu
        except Exception as e:
            print(e)
            return None

    def update(self, menu_id: uuid.UUID, data: dict) -> Menu | None:
        try:
            menu = self.session.query(Menu).filter(Menu.id == menu_id).first()
            menu.title = data['title']
            menu.description = data['description']
            self.session.commit()
            self.session.refresh(menu)
            return menu
        except Exception as e:
            print(e)
            return None

    def delete(self, menu_id: uuid.UUID) -> Menu | None:
        try:
            menu = self.session.query(Menu).filter(Menu.id == menu_id).first()
            self.session.delete(menu)
            self.session.commit()
            return menu
        except Exception as e:
            print(e)
            return None
