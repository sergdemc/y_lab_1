import uuid

from database.db import get_session
from fastapi import APIRouter, Depends, HTTPException
from schemas.menu_schemas import (MenuScheme, MenuSchemeCreate,
                                  MenuWithDetailsScheme)
from sqlalchemy.orm import Session
from services.menu_service import MenuService

menu_router = APIRouter(prefix="/menus", tags=["Menu"])


@menu_router.post("/", response_model=MenuScheme, status_code=201)
def create_menu(
        menu: MenuSchemeCreate,
        session: Session = Depends(get_session)
):
    menu_service = MenuService(session)
    if menu_service.is_menu_exists(menu.title):
        raise HTTPException(status_code=400, detail="menu exists")
    return menu_service.create_menu(menu.model_dump())


@menu_router.get("/{menu_id}", response_model=MenuWithDetailsScheme)
def read_menu(
        menu_id: uuid.UUID,
        session: Session = Depends(get_session)
):
    menu_service = MenuService(session)
    menu = menu_service.get_menu_by_id(menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")

    return menu


@menu_router.get("/", response_model=list[MenuWithDetailsScheme])
def read_menus(
        session: Session = Depends(get_session)
):
    menu_service = MenuService(session)
    return menu_service.get_all_menus()


@menu_router.patch("/{menu_id}", response_model=MenuScheme)
def update_menu(
        menu_id: uuid.UUID,
        updated_menu: MenuSchemeCreate,
        session: Session = Depends(get_session)
):
    menu_service = MenuService(session)
    menu = menu_service.update_menu(menu_id, updated_menu.model_dump())
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")

    return menu


@menu_router.delete("/{menu_id}", response_model=MenuScheme)
def delete_menu(
        menu_id: uuid.UUID,
        session: Session = Depends(get_session)
):
    menu_service = MenuService(session)
    menu = menu_service.delete_menu(menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")

    return menu
