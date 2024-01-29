import uuid

from database.db import get_session
from database.models import Dish, Menu, Submenu
from fastapi import APIRouter, Depends, HTTPException
from schemas.submenu_schemas import (SubmenuScheme, SubmenuSchemeCreate,
                                     SubmenuWithDishCountScheme)
from sqlalchemy.orm import Session

submenu_router = APIRouter(prefix="/menus", tags=["Submenu"])


@submenu_router.post("/{menu_id}/submenus", response_model=SubmenuScheme, status_code=201)
def create_submenu(
        menu_id: uuid.UUID,
        submenu: SubmenuSchemeCreate,
        session: Session = Depends(get_session)
):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    if session.query(Submenu).filter(Submenu.title == submenu.title).first() is not None:
        raise HTTPException(status_code=400, detail="submenu exists")
    db_submenu = Submenu(**submenu.model_dump(), menu_id=menu_id)
    session.add(db_submenu)
    session.commit()
    session.refresh(db_submenu)
    return db_submenu


@submenu_router.get("/{menu_id}/submenus/{submenu_id}", response_model=SubmenuWithDishCountScheme)
def read_submenu(
        submenu_id: uuid.UUID,
        session: Session = Depends(get_session)
):
    submenu = session.query(Submenu).filter(Submenu.id == submenu_id).first()
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    dish_count = session.query(Dish).filter(Dish.submenu_id == submenu.id).count()

    submenu = SubmenuWithDishCountScheme(
        id=submenu.id,
        title=submenu.title,
        description=submenu.description,
        dishes_count=dish_count
    )

    return submenu


@submenu_router.get("/{menu_id}/submenus", response_model=list[SubmenuWithDishCountScheme])
def read_submenus(
        menu_id: uuid.UUID,
        session: Session = Depends(get_session)
):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    submenus = session.query(Submenu).filter(Submenu.menu_id == menu_id).all()
    submenus_with_dish_count = []

    for submenu in submenus:
        dish_count = session.query(Dish).filter(Dish.submenu_id == submenu.id).count()

        submenu_info = SubmenuWithDishCountScheme(
            id=submenu.id,
            title=submenu.title,
            description=submenu.description,
            dishes_count=dish_count
        )
        submenus_with_dish_count.append(submenu_info)

    return submenus_with_dish_count


@submenu_router.patch("/{menu_id}/submenus/{submenu_id}", response_model=SubmenuScheme)
def update_submenu(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    updated_submenu: SubmenuSchemeCreate,
    session: Session = Depends(get_session)
):

    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    submenu = session.query(Submenu).filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id).first()
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    for key, value in updated_submenu.model_dump().items():
        setattr(submenu, key, value)

    session.commit()
    session.refresh(submenu)
    return submenu


@submenu_router.delete("/{menu_id}/submenus/{submenu_id}", response_model=SubmenuScheme)
def delete_submenu(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        session: Session = Depends(get_session)
):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    submenu = session.query(Submenu).filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id).first()
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    session.query(Dish).filter(Dish.submenu_id == submenu_id).delete()
    session.delete(submenu)
    session.commit()

    return SubmenuScheme.model_validate(submenu)
