import pickle
import uuid

import redis
from database.models import Dish, Menu, Submenu
from repositories import MenuORMRepository, RedisCacheRepository
from schemas.menu_schemas import MenuWithDetailsScheme
from sqlalchemy import func
from sqlalchemy.orm import Session


class MenuService:
    def __init__(
            self,
            session: Session,
            redis_client: redis.Redis,
            repository=MenuORMRepository,
            cache_repository=RedisCacheRepository
    ) -> None:
        self._menu_repository = repository(session)
        self._cache_repository = cache_repository(redis_client)

    def _get_menu_details(
            self,
            menu_id: uuid.UUID
    ) -> tuple[Menu, int, int] | None:
        try:
            menu_details = (
                self._menu_repository.session.query(
                    Menu,
                    func.count(func.distinct(Submenu.id)),
                    func.count(Dish.id)
                )
                .outerjoin(Submenu, Submenu.menu_id == Menu.id)
                .outerjoin(Dish, Dish.submenu_id == Submenu.id)
                .filter(Menu.id == menu_id)
                .group_by(Menu.id)
                .first()
            )
            return menu_details
        except Exception as e:
            print(e)
            return None

    def is_menu_exists(
            self,
            unic_field: str | uuid.UUID
    ) -> bool:
        if isinstance(unic_field, uuid.UUID):
            return self._menu_repository.get_by_id(unic_field) is not None
        return self._menu_repository.get_by_title(unic_field) is not None

    def get_all_menus(self) -> list[MenuWithDetailsScheme]:
        menus_with_details = []
        menus = self._menu_repository.get_all()
        for menu in menus:
            menu_details = self.get_menu_by_id(menu.id)
            if not menu_details:
                continue

            menus_with_details.append(menu_details)
        return menus_with_details

    def get_menu_by_id(
            self,
            menu_id: uuid.UUID
    ) -> MenuWithDetailsScheme | None:

        if cached_menu := self._cache_repository.get(f'menu_{menu_id}'):
            return MenuWithDetailsScheme(**pickle.loads(cached_menu))

        menu_details = self._get_menu_details(menu_id)
        if not menu_details:
            return None

        menu, submenu_count, dish_count = menu_details
        menu_with_details = MenuWithDetailsScheme(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=submenu_count,
            dishes_count=dish_count
        )
        self._cache_repository.set(
            f'menu_{menu_id}',
            pickle.dumps(menu_with_details.model_dump())
        )
        return menu_with_details

    def create_menu(self, menu_data: dict) -> Menu | None:
        new_menu = self._menu_repository.create(menu_data)
        return new_menu if new_menu else None

    def update_menu(self, menu_id: uuid.UUID,
                    new_menu_data: dict) -> Menu | None:
        updated_menu = self._menu_repository.update(menu_id, new_menu_data)
        if updated_menu:
            self._cache_repository.delete(f'menu_{menu_id}')
        return updated_menu if updated_menu else None

    def delete_menu(self, menu_id: uuid.UUID) -> Menu:
        submenus = self._menu_repository.get_by_id(menu_id).submenus
        dishes = []
        for submenu in submenus:
            dishes.extend(submenu.dishes)

        deleted_menu = self._menu_repository.delete(menu_id)
        if deleted_menu:
            self._cache_repository.delete(f'menu_{menu_id}')

            for submenu in submenus:
                self._cache_repository.delete(f'submenu_{submenu.id}')

            for dish in dishes:
                self._cache_repository.delete(f'dish_{dish.id}')

        return deleted_menu if deleted_menu else None
