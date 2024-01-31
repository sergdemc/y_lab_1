import uuid

from database.db import get_session
from database.models import Dish, Menu, Submenu
from fastapi import APIRouter, Depends, HTTPException
from schemas.menu_schemas import (MenuScheme, MenuSchemeCreate,
                                  MenuWithDetailsScheme)
from sqlalchemy import func
from sqlalchemy.orm import Session

menu_router = APIRouter(prefix="/menus", tags=["Menu"])


def get_menu_details(menu, session):
    menu_details = (
        session.query(Menu, func.count(func.distinct(Submenu.id)), func.count(Dish.id))
        .outerjoin(Submenu, Submenu.menu_id == Menu.id)
        .outerjoin(Dish, Dish.submenu_id == Submenu.id)
        .filter(Menu.id == menu.id)
        .group_by(Menu.id)
        .first()
    )
    return menu_details


@menu_router.post("/", response_model=MenuScheme, status_code=201)
def create_menu(
        menu: MenuSchemeCreate,
        session: Session = Depends(get_session)
):
    db_menu = session.query(Menu).filter(Menu.title == menu.title).first()
    if db_menu is not None:
        raise HTTPException(status_code=400, detail="menu exists")
    db_menu = Menu(**menu.model_dump())
    session.add(db_menu)
    session.commit()
    session.refresh(db_menu)
    return db_menu


@menu_router.get("/{menu_id}", response_model=MenuWithDetailsScheme)
def read_menu(
        menu_id: uuid.UUID,
        session: Session = Depends(get_session)
):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    # submenu_count = session.query(Submenu).filter(Submenu.menu_id == menu.id).count()
    # dish_count = session.query(Dish).join(Submenu).filter(Submenu.menu_id == menu.id).count()

    menu_details = get_menu_details(menu, session)

    if menu_details is None:
        raise HTTPException(status_code=404, detail="menu not found")

    menu, submenu_count, dish_count = menu_details

    menu = MenuWithDetailsScheme(
        id=menu.id,
        title=menu.title,
        description=menu.description,
        submenus_count=submenu_count,
        dishes_count=dish_count
    )

    return menu


@menu_router.get("/", response_model=list[MenuWithDetailsScheme])
def read_menus(session: Session = Depends(get_session)):
    menus = session.query(Menu).all()
    menus_with_details = []

    for menu in menus:

        menu_details = get_menu_details(menu, session)

        if menu_details is None:
            raise HTTPException(status_code=404, detail="menu not found")

        menu, submenu_count, dish_count = menu_details

        menu_info = MenuWithDetailsScheme(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=submenu_count,
            dishes_count=dish_count
        )
        menus_with_details.append(menu_info)

    return menus_with_details


@menu_router.patch("/{menu_id}", response_model=MenuScheme)
def update_menu(
        menu_id: uuid.UUID,
        updated_menu: MenuSchemeCreate,
        session: Session = Depends(get_session)
):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()

    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    print(menu.title)
    for key, value in updated_menu.model_dump().items():
        setattr(menu, key, value)
    print(menu.title)
    session.commit()
    session.refresh(menu)
    return menu


@menu_router.delete("/{menu_id}", response_model=MenuScheme)
def delete_menu(
        menu_id: uuid.UUID,
        session: Session = Depends(get_session)
):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    session.delete(menu)
    session.commit()

    return menu
