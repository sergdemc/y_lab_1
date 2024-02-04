import uuid

from database.db import get_session
from database.models import Submenu
from dependencies.redis import cache
from fastapi import APIRouter, Depends, HTTPException
from schemas.submenu_schemas import (
    SubmenuScheme,
    SubmenuSchemeCreate,
    SubmenuWithDishCountScheme,
)
from services.menu_service import MenuService
from services.submenu_service import SubmenuService
from sqlalchemy.orm import Session

submenu_router = APIRouter(prefix='/menus', tags=['Submenu'])


@submenu_router.post(
    '/{menu_id}/submenus',
    response_model=SubmenuScheme,
    name='create_submenu',
    status_code=201
)
def create_submenu(
        menu_id: uuid.UUID,
        submenu: SubmenuSchemeCreate,
        session: Session = Depends(get_session),
        redis_client: cache = Depends(cache),
) -> Submenu:
    menu_service = MenuService(session, redis_client)
    if not menu_service.is_menu_exists(menu_id):
        raise HTTPException(status_code=404, detail='menu not found')

    submenu_service = SubmenuService(session, redis_client)
    if submenu_service.is_submenu_exists(submenu.title):
        raise HTTPException(status_code=400, detail='submenu exists')

    return submenu_service.create_submenu(menu_id, submenu.model_dump())


@submenu_router.get(
    '/{menu_id}/submenus/{submenu_id}',
    response_model=SubmenuWithDishCountScheme,
    name='read_submenu',
    status_code=200
)
def read_submenu(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        session: Session = Depends(get_session),
        redis_client: cache = Depends(cache)
) -> SubmenuWithDishCountScheme:
    menu_service = MenuService(session, redis_client)
    if not menu_service.is_menu_exists(menu_id):
        raise HTTPException(status_code=404, detail='menu not found')

    submenu_service = SubmenuService(session, redis_client)
    if not submenu_service.is_submenu_exists_in_menu(menu_id, submenu_id):
        raise HTTPException(status_code=404, detail='submenu not found')

    submenu = submenu_service.get_submenu_by_id(submenu_id)
    if not submenu:
        raise HTTPException(status_code=404, detail='submenu not found')

    return submenu


@submenu_router.get(
    '/{menu_id}/submenus',
    response_model=list[SubmenuWithDishCountScheme],
    name='read_submenus',
    status_code=200
)
def read_submenus(
        menu_id: uuid.UUID,
        session: Session = Depends(get_session),
        redis_client: cache = Depends(cache)
) -> list[SubmenuWithDishCountScheme]:
    menu_service = MenuService(session, redis_client)
    if not menu_service.is_menu_exists(menu_id):
        raise HTTPException(status_code=404, detail='menu not found')

    submenu_service = SubmenuService(session, redis_client)
    return submenu_service.get_all_submenus(menu_id)


@submenu_router.patch(
    '/{menu_id}/submenus/{submenu_id}',
    response_model=SubmenuScheme,
    name='update_submenu',
    status_code=200
)
def update_submenu(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        updated_submenu: SubmenuSchemeCreate,
        session: Session = Depends(get_session),
        redis_client: cache = Depends(cache)
) -> Submenu:
    menu_service = MenuService(session, redis_client)
    if not menu_service.is_menu_exists(menu_id):
        raise HTTPException(status_code=404, detail='menu not found')

    submenu_service = SubmenuService(session, redis_client)
    if not submenu_service.is_submenu_exists_in_menu(menu_id, submenu_id):
        raise HTTPException(status_code=404, detail='submenu not found')

    return submenu_service.update_submenu(submenu_id, updated_submenu.model_dump())


@submenu_router.delete(
    '/{menu_id}/submenus/{submenu_id}',
    response_model=SubmenuScheme,
    name='delete_submenu',
    status_code=200
)
def delete_submenu(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        session: Session = Depends(get_session),
        redis_client: cache = Depends(cache)
) -> Submenu:
    menu_service = MenuService(session, redis_client)
    if not menu_service.is_menu_exists(menu_id):
        raise HTTPException(status_code=404, detail='menu not found')

    submenu_service = SubmenuService(session, redis_client)
    if not submenu_service.is_submenu_exists_in_menu(menu_id, submenu_id):
        raise HTTPException(status_code=404, detail='submenu not found')

    return submenu_service.delete_submenu(submenu_id)
