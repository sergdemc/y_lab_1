import pickle
import uuid

import redis
from database.models import Dish, Submenu
from repositories import RedisCacheRepository, SubmenuORMRepository
from schemas.submenu_schemas import SubmenuWithDishCountScheme
from sqlalchemy import func
from sqlalchemy.orm import Session


class SubmenuService:
    def __init__(
            self,
            session: Session,
            redis_client: redis.Redis,
            repository=SubmenuORMRepository,
            cache_repository=RedisCacheRepository
    ) -> None:
        self._submenu_repository: SubmenuORMRepository = repository(session)
        self._cache_repository: RedisCacheRepository = cache_repository(redis_client)

    def _get_submenu_details(self, submenu_id: uuid.UUID) -> tuple[Submenu, int] | None:
        try:
            submenu_details: tuple[Submenu, int] = (
                self._submenu_repository.session.
                query(Submenu, func.count(func.distinct(Dish.id)))
                .outerjoin(Dish, Dish.submenu_id == Submenu.id)
                .group_by(Submenu)
                .filter(Submenu.id == submenu_id)
                .first()
            )
            return submenu_details
        except Exception as e:
            print(e)
            return None

    def is_submenu_exists_in_menu(self, menu_id: uuid.UUID, submenu_id: uuid.UUID) -> bool:
        submenu: Submenu | None = self._submenu_repository.get_by_id(submenu_id)
        return submenu.menu_id == menu_id if submenu else False

    def is_submenu_exists(self, unic_field: str | uuid.UUID) -> bool:
        if isinstance(unic_field, uuid.UUID):
            return self._submenu_repository.get_by_id(unic_field) is not None
        return self._submenu_repository.get_by_title(unic_field) is not None

    def get_all_submenus(self, menu_id: uuid.UUID) -> list[SubmenuWithDishCountScheme]:

        submenus_with_details: list = []
        submenus: list[Submenu] = self._submenu_repository.get_all(menu_id)

        for submenu in submenus:
            submenu_details: SubmenuWithDishCountScheme = self.get_submenu_by_id(submenu.id)
            if not submenu_details:
                continue

            submenus_with_details.append(submenu_details)

        return submenus_with_details

    def get_submenu_by_id(self, submenu_id: uuid.UUID) -> SubmenuWithDishCountScheme | None:
        cached_submenu: object | None

        if cached_submenu := self._cache_repository.get(f'menu_{submenu_id}'):
            return SubmenuWithDishCountScheme(**pickle.loads(cached_submenu))

        submenu_details: tuple[Submenu, int] | None = self._get_submenu_details(submenu_id)

        if not submenu_details:
            return None

        submenu, dish_count = submenu_details
        submenu_with_detail = SubmenuWithDishCountScheme(
            id=submenu.id,
            title=submenu.title,
            description=submenu.description,
            dishes_count=dish_count
        )
        self._cache_repository.set(
            f'submenu_{submenu_id}',
            pickle.dumps(submenu_with_detail.model_dump())
        )
        return submenu_with_detail

    def create_submenu(self, menu_id: uuid.UUID, data: dict) -> Submenu | None:
        submenu: Submenu | None = self._submenu_repository.create(data, menu_id)
        if submenu:
            self._cache_repository.delete(f'menu_{menu_id}')

        return submenu

    def update_submenu(self, submenu_id: uuid.UUID, data: dict) -> Submenu | None:
        updated_submenu: Submenu | None = self._submenu_repository.update(submenu_id, data)
        if updated_submenu:
            self._cache_repository.delete(f'submenu_{submenu_id}')

        return updated_submenu

    def delete_submenu(self, submenu_id: uuid.UUID) -> Submenu | None:

        menu_id: uuid.UUID = self._submenu_repository.get_by_id(submenu_id).menu_id
        dishes: list[Dish] = self._submenu_repository.get_by_id(submenu_id).dishes
        deleted_submenu: Submenu | None = self._submenu_repository.delete(submenu_id)
        if deleted_submenu:
            self._cache_repository.delete(f'menu_{menu_id}')

            for dish in dishes:
                self._cache_repository.delete(f'dish_{dish.id}')

        return deleted_submenu
