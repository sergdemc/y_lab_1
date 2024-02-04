import uuid

from database.models import Dish
from repositories.repositories_interface import IRepository


class DishORMRepository(IRepository):
    def __init__(self, session=None) -> None:
        self.session = session

    def get_all(self, submenu_id: uuid.UUID) -> list[Dish]:
        try:
            return (self.session.query(Dish)
                    .filter(Dish.submenu_id == submenu_id).all())
        except Exception as e:
            print(e)
            return []

    def get_by_id(self, dish_id: uuid.UUID) -> Dish | None:
        try:
            return self.session.query(Dish).filter(Dish.id == dish_id).first()
        except Exception as e:
            print(e)
            return None

    def get_by_title(self, title: str) -> Dish | None:
        try:
            return self.session.query(Dish).filter(Dish.title == title).first()
        except Exception as e:
            print(e)
            return None

    def create(self, data: dict, submenu_id: uuid.UUID) -> Dish | None:
        try:
            dish = Dish(**data, submenu_id=submenu_id)
            self.session.add(dish)
            self.session.commit()
            self.session.refresh(dish)
            return dish
        except Exception as e:
            print(e)
            return None

    def update(self, dish_id: uuid.UUID, data: dict) -> Dish | None:
        try:
            dish = self.session.query(Dish).filter(Dish.id == dish_id).first()
            dish.title = data['title']
            dish.description = data['description']
            dish.price = data['price']
            self.session.commit()
            self.session.refresh(dish)
            return dish
        except Exception as e:
            print(e)
            return None

    def delete(self, dish_id) -> Dish | None:
        try:
            dish = self.session.query(Dish).filter(Dish.id == dish_id).first()
            self.session.delete(dish)
            self.session.commit()
            return dish
        except Exception as e:
            print(e)
            return None
