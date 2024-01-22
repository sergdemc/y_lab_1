import uuid

from database.db import get_session
from database.models import Dish, Menu, Submenu
from fastapi import APIRouter, Depends, HTTPException
from schemas.menu_schemas import (MenuScheme, MenuSchemeCreate,
                                  MenuWithDetailsScheme)
from sqlalchemy.orm import Session

menu_router = APIRouter(prefix="/menus", tags=["Menu"])


@menu_router.post("/", response_model=MenuScheme, status_code=201)
def create_menu(menu: MenuSchemeCreate, session: Session = Depends(get_session)):
    db_menu = Menu(**menu.model_dump())
    session.add(db_menu)
    session.commit()
    session.refresh(db_menu)
    return db_menu


@menu_router.get("/{menu_id}", response_model=MenuWithDetailsScheme)
def read_menu(menu_id: uuid.UUID, session: Session = Depends(get_session)):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    submenu_count = session.query(Submenu).filter(Submenu.menu_id == menu.id).count()
    dish_count = session.query(Dish).join(Submenu).filter(Submenu.menu_id == menu.id).count()

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
        submenu_count = session.query(Submenu).filter(Submenu.menu_id == menu.id).count()
        dish_count = session.query(Dish).join(Submenu).filter(Submenu.menu_id == menu.id).count()

        menu_info = MenuWithDetailsScheme(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=submenu_count,
            dishes_count=dish_count
        )
        menus_with_details.append(menu_info)

    return menus_with_details


# @menu_router.get("/", response_model=list[MenuWithDetailsScheme])
# def read_menus(session: Session = Depends(get_session)):
#     menus = session.query(Menu).all()
#     return menus


@menu_router.put("/{menu_id}", response_model=MenuScheme)
def update_menu(menu_id: uuid.UUID, updated_menu: MenuSchemeCreate, session: Session = Depends(get_session)):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    for key, value in updated_menu.model_dump().items():
        setattr(menu, key, value)
    session.commit()
    session.refresh(menu)
    return menu


@menu_router.patch("/{menu_id}", response_model=MenuScheme)
def patch_menu(menu_id: uuid.UUID, updated_menu: MenuSchemeCreate, session: Session = Depends(get_session)):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    for key, value in updated_menu.model_dump().items():
        setattr(menu, key, value)
    session.commit()
    session.refresh(menu)
    return menu


@menu_router.delete("/{menu_id}", response_model=MenuScheme)
def delete_menu(menu_id: uuid.UUID, session: Session = Depends(get_session)):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    session.delete(menu)
    session.commit()

    return menu
