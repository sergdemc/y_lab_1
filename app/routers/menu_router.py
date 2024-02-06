import uuid

from database.db import get_session
from database.models import Menu
from dependencies.redis import cache
from fastapi import APIRouter, Depends, HTTPException
from schemas.menu_schemas import MenuScheme, MenuSchemeCreate, MenuWithDetailsScheme
from services.menu_service import MenuService
from sqlalchemy.orm import Session

menu_router = APIRouter(prefix='/menus', tags=['Menu'])


@menu_router.post(
    '/',
    response_model=MenuScheme,
    responses={400: {'detail': 'menu exists'}},
    status_code=201,
    name='create_menu'
)
def create_menu(
        menu: MenuSchemeCreate,
        session: Session = Depends(get_session),
        redis_client: cache = Depends(cache)
) -> Menu:
    menu_service = MenuService(session, redis_client)
    if menu_service.is_menu_exists(menu.title):
        raise HTTPException(status_code=400, detail='menu exists')
    return menu_service.create_menu(menu.model_dump())


@menu_router.get(
    '/{menu_id}',
    response_model=MenuWithDetailsScheme,
    responses={404: {'detail': 'menu not found'}},
    status_code=200,
    name='read_menu'
)
def read_menu(
        menu_id: uuid.UUID,
        session: Session = Depends(get_session),
        redis_client: cache = Depends(cache)
) -> MenuWithDetailsScheme:
    menu_service = MenuService(session, redis_client)
    menu = menu_service.get_menu_by_id(menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail='menu not found')

    return menu


@menu_router.get(
    '/',
    response_model=list[MenuWithDetailsScheme],
    status_code=200,
    name='read_menus'
)
def read_menus(
        session: Session = Depends(get_session),
        redis_client: cache = Depends(cache)
) -> list[MenuWithDetailsScheme]:
    menu_service = MenuService(session, redis_client)
    return menu_service.get_all_menus()


@menu_router.patch(
    '/{menu_id}',
    response_model=MenuScheme,
    responses={404: {'': 'menu not found'}},
    status_code=200,
    name='update_menu'
)
def update_menu(
        menu_id: uuid.UUID,
        updated_menu: MenuSchemeCreate,
        session: Session = Depends(get_session),
        redis_client: cache = Depends(cache)
) -> Menu:
    menu_service = MenuService(session, redis_client)
    menu = menu_service.update_menu(menu_id, updated_menu.model_dump())
    if not menu:
        raise HTTPException(status_code=404, detail='menu not found')

    return menu


@menu_router.delete(
    '/{menu_id}',
    response_model=MenuScheme,
    responses={404: {'detail': 'menu not found'}},
    status_code=200,
    name='delete_menu'
)
def delete_menu(
        menu_id: uuid.UUID,
        session: Session = Depends(get_session),
        redis_client: cache = Depends(cache)
) -> Menu:
    menu_service = MenuService(session, redis_client)
    menu = menu_service.delete_menu(menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail='menu not found')

    return menu
