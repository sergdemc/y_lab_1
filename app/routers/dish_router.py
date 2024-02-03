import uuid

from fastapi import APIRouter, Depends, HTTPException
from schemas.dish_schemas import DishScheme, DishSchemeCreate
from sqlalchemy.orm import Session

from database.db import get_session
from services.menu_service import MenuService
from services.submenu_service import SubmenuService
from services.dish_service import DishService
from dependencies.redis import cache

dish_router = APIRouter(prefix="/menus", tags=["Dish"])


@dish_router.post("/{menu_id}/submenus/{submenu_id}/dishes",
                  response_model=DishScheme, status_code=201)
def create_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish: DishSchemeCreate,
        session: Session = Depends(get_session),
        redis_client: cache = Depends(cache)
):
    menu_service = MenuService(session)
    if not menu_service.is_menu_exists(menu_id):
        raise HTTPException(status_code=404, detail="menu not found")

    submenu_service = SubmenuService(session)
    if not submenu_service.is_submenu_exists(submenu_id):
        raise HTTPException(status_code=404, detail="submenu not found")

    dish_service = DishService(session, redis_client)
    if dish_service.is_dish_exists(dish.title):
        raise HTTPException(status_code=400, detail="dish exists")

    return dish_service.create_dish(submenu_id, dish.model_dump())


@dish_router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                 response_model=DishScheme)
def read_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        session: Session = Depends(get_session),
        redis_client: cache = Depends(cache)
):
    menu_service = MenuService(session)
    if not menu_service.is_menu_exists(menu_id):
        raise HTTPException(status_code=404, detail="menu not found")

    submenu_service = SubmenuService(session)
    if not submenu_service.is_submenu_exists_in_menu(menu_id, submenu_id):
        raise HTTPException(status_code=404, detail="submenu not found")

    dish_service = DishService(session, redis_client)
    if not dish_service.is_dish_exists_in_submenu(submenu_id, dish_id):
        raise HTTPException(status_code=404, detail="dish not found")

    return dish_service.get_dish_by_id(dish_id)


@dish_router.get("/{menu_id}/submenus/{submenu_id}/dishes",
                 response_model=list[DishScheme])
def read_dishes(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        session: Session = Depends(get_session),
        redis_client: cache = Depends(cache)
) -> list[DishScheme]:
    menu_service = MenuService(session)
    if not menu_service.is_menu_exists(menu_id):
        raise HTTPException(status_code=404, detail="menu not found")

    submenu_service = SubmenuService(session)
    if not submenu_service.is_submenu_exists_in_menu(menu_id, submenu_id):
        # raise HTTPException(status_code=404, detail="submenu not found")
        return []

    dish_service = DishService(session, redis_client)
    return dish_service.get_all_dishes(submenu_id)


@dish_router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                   response_model=DishScheme)
def update_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        updated_dish: DishSchemeCreate,
        session: Session = Depends(get_session),
        redis_client: cache = Depends(cache)
):
    menu_service = MenuService(session)
    if not menu_service.is_menu_exists(menu_id):
        raise HTTPException(status_code=404, detail="menu not found")

    submenu_service = SubmenuService(session)
    if not submenu_service.is_submenu_exists_in_menu(menu_id, submenu_id):
        raise HTTPException(status_code=404, detail="submenu not found")

    dish_service = DishService(session, redis_client)
    if not dish_service.is_dish_exists_in_submenu(submenu_id, dish_id):
        raise HTTPException(status_code=404, detail="dish not found")

    return dish_service.update_dish(dish_id, updated_dish.model_dump())


@dish_router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                    response_model=DishScheme)
def delete_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        session: Session = Depends(get_session),
        redis_client: cache = Depends(cache)
):
    menu_service = MenuService(session)
    if not menu_service.is_menu_exists(menu_id):
        raise HTTPException(status_code=404, detail="menu not found")

    submenu_service = SubmenuService(session)
    if not submenu_service.is_submenu_exists_in_menu(menu_id, submenu_id):
        raise HTTPException(status_code=404, detail="submenu not found")

    dish_service = DishService(session, redis_client)
    if not dish_service.is_dish_exists_in_submenu(submenu_id, dish_id):
        raise HTTPException(status_code=404, detail="dish not found")

    return dish_service.delete_dish(dish_id)
