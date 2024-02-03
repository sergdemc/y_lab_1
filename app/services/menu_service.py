import uuid

from database.models import Menu, Submenu, Dish
from repositories import MenuORMRepository
from typing import List, Union
from sqlalchemy import func
from sqlalchemy.orm import Session

from schemas.menu_schemas import MenuWithDetailsScheme


class MenuService:
    def __init__(self, session: Session, repository=MenuORMRepository):
        self._menu_repository = repository(session)

    def _get_menu_details(self,
                          menu_id: uuid.UUID) -> tuple[Menu, int, int] | None:
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

    def is_menu_exists(self, unic_field: Union[str, uuid.UUID]) -> bool:
        if isinstance(unic_field, uuid.UUID):
            return self._menu_repository.get_by_id(unic_field) is not None
        return self._menu_repository.get_by_title(unic_field) is not None

    def get_all_menus(self) -> List[MenuWithDetailsScheme]:
        menus_with_details = []
        menus = self._menu_repository.get_all()
        for menu in menus:
            menu_details = self._get_menu_details(menu.id)
            if not menu_details:
                continue
            menu, submenu_count, dish_count = menu_details

            menus_with_details.append(MenuWithDetailsScheme(
                id=menu.id,
                title=menu.title,
                description=menu.description,
                submenus_count=submenu_count,
                dishes_count=dish_count
            ))
        return menus_with_details

    def get_menu_by_id(self,
                       menu_id: uuid.UUID) -> MenuWithDetailsScheme | None:
        menu_details = self._get_menu_details(menu_id)
        if not menu_details:
            return None
        menu, submenu_count, dish_count = menu_details
        return MenuWithDetailsScheme(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=submenu_count,
            dishes_count=dish_count
        )

    def create_menu(self, menu_data: dict) -> Menu | None:
        new_menu = self._menu_repository.create(menu_data)
        return new_menu if new_menu else None

    def update_menu(self, menu_id: uuid.UUID,
                    new_menu_data: dict) -> Menu | None:
        updated_menu = self._menu_repository.update(menu_id, new_menu_data)
        return updated_menu if updated_menu else None

    def delete_menu(self, menu_id: uuid.UUID) -> Menu:
        return self._menu_repository.delete(menu_id)
