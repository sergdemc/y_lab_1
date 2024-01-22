import uuid

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.db import get_session
from database.models import Menu, Submenu, Dish
from schemas.dish_schemas import DishScheme, DishSchemeCreate

dish_router = APIRouter(prefix="/menus", tags=["Dish"])


@dish_router.post("/{menu_id}/submenus/{submenu_id}/dishes", response_model=DishScheme, status_code=201)
def create_dish(menu_id: uuid.UUID, submenu_id: uuid.UUID, dish: DishSchemeCreate, db: Session = Depends(get_session)):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    submenu = db.query(Submenu).filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id).first()
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found or does not belong to the specified menu")

    db_dish = Dish(**dish.model_dump(), submenu_id=submenu_id)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
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
        raise HTTPException(status_code=404, detail="submenu not found or does not belong to the specified menu")

    dish = session.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish


@dish_router.get("/{menu_id}/submenus/{submenu_id}/dishes", response_model=list[DishScheme])
def read_dishes(menu_id: uuid.UUID, submenu_id: uuid.UUID, session: Session = Depends(get_session)):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    submenu = session.query(Submenu).filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id).first()
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found or does not belong to the specified menu")

    dishes = session.query(Dish).filter(Dish.submenu_id == submenu_id).all()
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
        raise HTTPException(status_code=404, detail="submenu not found or does not belong to the specified menu")

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
        raise HTTPException(status_code=404, detail="submenu not found or does not belong to the specified menu")

    dish = session.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=404, detail="dish not found")

    session.delete(dish)
    session.commit()
    return dish
