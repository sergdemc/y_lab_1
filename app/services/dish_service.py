import uuid

from database.models import Dish
from repositories import DishORMRepository
from typing import List, Union
from sqlalchemy.orm import Session

from schemas.dish_schemas import DishScheme

dish_repository = DishORMRepository()


class DishService:
    def __init__(self, session: Session, repository=DishORMRepository):
        self._dish_repository = repository(session)

    def is_dish_exists(self, unic_field: Union[str, uuid.UUID]) -> bool:
        if isinstance(unic_field, uuid.UUID):
            return self._dish_repository.get_by_id(unic_field) is not None
        return self._dish_repository.get_by_title(unic_field) is not None

    def is_dish_exists_in_submenu(self, submenu_id: uuid.UUID,
                                  dish_id: uuid.UUID) -> bool:
        dish = self._dish_repository.get_by_id(dish_id)
        return dish.submenu_id == submenu_id if dish else False

    def get_all_dishes(self, submenu_id: uuid.UUID) -> List[DishScheme]:
        dishes_list = []
        dishes = self._dish_repository.get_all(submenu_id)

        for dish in dishes:
            dishes_list.append(DishScheme(
                id=dish.id,
                title=dish.title,
                description=dish.description,
                price="{:.2f}".format(float(dish.price))
            ))
        return dishes_list

    def get_dish_by_id(self, dish_id: uuid.UUID) -> Dish | None:
        return self._dish_repository.get_by_id(dish_id)

    def create_dish(self, submenu_id: uuid.UUID, data: dict) -> Dish | None:
        return self._dish_repository.create(data, submenu_id)

    def update_dish(self, dish_id: uuid.UUID, data: dict) -> Dish | None:
        return self._dish_repository.update(dish_id, data)

    def delete_dish(self, dish_id: uuid.UUID) -> Dish | None:
        return self._dish_repository.delete(dish_id)
