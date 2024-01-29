import uuid

from database.db import get_session
from database.models import Dish, Menu, Submenu
from fastapi import APIRouter, Depends, HTTPException
from schemas.dish_schemas import DishScheme, DishSchemeCreate
from sqlalchemy.orm import Session

dish_router = APIRouter(prefix="/menus", tags=["Dish"])


@dish_router.post("/{menu_id}/submenus/{submenu_id}/dishes", response_model=DishScheme, status_code=201)
def create_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish: DishSchemeCreate,
        session: Session = Depends(get_session)
):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    submenu = session.query(Submenu).filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id).first()
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    if session.query(Dish).filter(Dish.title == dish.title).first() is not None:
        raise HTTPException(status_code=400, detail="dish exists")

    db_dish = Dish(**dish.model_dump(), submenu_id=submenu_id)
    session.add(db_dish)
    session.commit()
    session.refresh(db_dish)
    return db_dish


@dish_router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishScheme)
def read_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        session: Session = Depends(get_session)
):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    submenu = session.query(Submenu).filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id).first()
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    dish = session.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    dish.price = "{:.2f}".format(float(dish.price))
    return dish


@dish_router.get("/{menu_id}/submenus/{submenu_id}/dishes", response_model=list[DishScheme])
def read_dishes(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        session: Session = Depends(get_session)
):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    submenu = session.query(Submenu).filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id).first()
    if submenu is None:
        return []

    dishes = session.query(Dish).filter(Dish.submenu_id == submenu_id).all()
    for dish in dishes:
        dish.price = "{:.2f}".format(float(dish.price))

    return dishes


@dish_router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishScheme)
def update_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        updated_dish: DishSchemeCreate,
        session: Session = Depends(get_session)
):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    submenu = session.query(Submenu).filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id).first()
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    dish = session.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=404, detail="dish not found")

    for key, value in updated_dish.model_dump().items():
        setattr(dish, key, value)

    session.commit()
    session.refresh(dish)
    return dish


@dish_router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishScheme)
def delete_dish(
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        session: Session = Depends(get_session)
):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    submenu = session.query(Submenu).filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id).first()
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    dish = session.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=404, detail="dish not found")

    dish_data = DishScheme.model_validate(dish)
    session.delete(dish)
    session.commit()

    return dish_data
