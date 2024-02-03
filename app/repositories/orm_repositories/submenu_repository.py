import uuid

from database.models import Submenu
from repositories.repositories_interface import IRepository


class SubmenuORMRepository(IRepository):
    def __init__(self, session=None):
        self.session = session

    def get_all(self, menu_id: uuid.UUID = None) -> list[Submenu]:
        try:
            return self.session.query(Submenu).filter(Submenu.menu_id == menu_id).all()
        except Exception as e:
            print(e)
            return []

    def get_by_id(self, submenu_id: uuid.UUID) -> Submenu | None:
        try:
            return (self.session.query(Submenu).
                    filter(Submenu.id == submenu_id).first())
        except Exception as e:
            print(e)
            return None

    def get_by_title(self, title: str) -> Submenu | None:
        try:
            return (self.session.query(Submenu)
                    .filter(Submenu.title == title).first())
        except Exception as e:
            print(e)
            return None

    def create(self, data: dict, menu_id: uuid.UUID = None) -> Submenu | None:
        try:
            submenu = Submenu(**data, menu_id=menu_id)
            self.session.add(submenu)
            self.session.commit()
            self.session.refresh(submenu)
            return submenu
        except Exception as e:
            print(e)
            return None

    def update(self, submenu_id: uuid.UUID, data: dict) -> Submenu | None:
        try:
            submenu = (self.session.query(Submenu).
                       filter(Submenu.id == submenu_id).first())
            submenu.title = data['title']
            submenu.description = data['description']
            self.session.commit()
            self.session.refresh(submenu)
            return submenu
        except Exception as e:
            print(e)
            return None

    def delete(self, submenu_id: uuid.UUID) -> Submenu | None:
        try:
            submenu = (self.session.query(Submenu).
                       filter(Submenu.id == submenu_id).first())

            for dish in submenu.dishes:
                self.session.delete(dish)

            self.session.delete(submenu)
            self.session.commit()
            return submenu
        except Exception as e:
            print(e)
            return None
