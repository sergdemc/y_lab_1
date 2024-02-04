import pickle
import uuid

import redis
from database.models import Dish
from repositories import DishORMRepository, RedisCacheRepository
from schemas.dish_schemas import DishScheme
from sqlalchemy.orm import Session

dish_repository = DishORMRepository()


class DishService:
    def __init__(
            self,
            session: Session,
            redis_client: redis.Redis,
            repository=DishORMRepository,
            cache_repository=RedisCacheRepository
    ) -> None:
        self._dish_repository = repository(session)
        self._cache_repository = cache_repository(redis_client)

    def is_dish_exists(self, unic_field: str | uuid.UUID) -> bool:
        if isinstance(unic_field, uuid.UUID):
            return self._dish_repository.get_by_id(unic_field) is not None
        return self._dish_repository.get_by_title(unic_field) is not None

    def is_dish_exists_in_submenu(
            self, submenu_id: uuid.UUID, dish_id: uuid.UUID
    ) -> bool:
        dish = self._dish_repository.get_by_id(dish_id)
        return dish.submenu_id == submenu_id if dish else False

    def get_all_dishes(self, submenu_id: uuid.UUID) -> list[DishScheme]:
        dishes_list = []
        dishes = self._dish_repository.get_all(submenu_id)

        for dish in dishes:
            dish_scheme = self.get_dish_by_id(dish.id)
            if not dish_scheme:
                continue

            dishes_list.append(dish_scheme)
        return dishes_list

    def get_dish_by_id(self, dish_id: uuid.UUID) -> DishScheme | None:
        if cached_submenu := self._cache_repository.get(f'menu_{dish_id}'):
            return DishScheme(**pickle.loads(cached_submenu))

        dish = self._dish_repository.get_by_id(dish_id)
        if not dish:
            return None

        dish_scheme = DishScheme(
            id=dish.id,
            title=dish.title,
            description=dish.description,
            price=f'{float(dish.price):.2f}'
        )
        self._cache_repository.set(f'dish_{dish_id}', pickle.dumps(dish_scheme))
        return dish_scheme

    def create_dish(self, submenu_id: uuid.UUID, data: dict) -> Dish | None:
        dish = self._dish_repository.create(data, submenu_id)
        if dish:
            menu_id = dish.submenu.menu_id
            self._cache_repository.delete(f'menu_{menu_id}')
            self._cache_repository.delete(f'submenu_{submenu_id}')
        return dish

    def update_dish(self, dish_id: uuid.UUID, data: dict) -> Dish | None:
        dish = self._dish_repository.update(dish_id, data)
        if dish:
            self._cache_repository.delete(f'dish_{dish_id}')
        return dish

    def delete_dish(self, dish_id: uuid.UUID) -> Dish | None:
        menu_id = self._dish_repository.get_by_id(dish_id).submenu.menu_id
        submenu_id = self._dish_repository.get_by_id(dish_id).submenu_id
        dish = self._dish_repository.delete(dish_id)
        if dish:
            self._cache_repository.delete(f'menu_{menu_id}')
            self._cache_repository.delete(f'submenu_{submenu_id}')
            self._cache_repository.delete(f'dish_{dish_id}')
        return dish
