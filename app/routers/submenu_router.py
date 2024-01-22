import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database.db import get_session
from database.models import Menu, Submenu, Dish
from schemas.submenu_schemas import SubmenuScheme, SubmenuSchemeCreate

submenu_router = APIRouter(prefix="/menus", tags=["Submenu"])


@submenu_router.post("/{menu_id}/submenus", response_model=SubmenuScheme, status_code=201)
def create_submenu(menu_id: uuid.UUID, submenu: SubmenuSchemeCreate, session: Session = Depends(get_session)):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    db_submenu = Submenu(**submenu.model_dump(), menu_id=menu_id)
    session.add(db_submenu)
    session.commit()
    session.refresh(db_submenu)
    return db_submenu


@submenu_router.get("/{menu_id}/submenus/{submenu_id}", response_model=SubmenuScheme)
def read_submenu(submenu_id: uuid.UUID, session: Session = Depends(get_session)):
    submenu = session.query(Submenu).filter(Submenu.id == submenu_id).first()
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return submenu


@submenu_router.get("/{menu_id}/submenus", response_model=list[SubmenuScheme])
def read_submenus(menu_id: uuid.UUID, session: Session = Depends(get_session)):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    submenus = menu.submenus
    return submenus


@submenu_router.patch("/{menu_id}/submenus/{submenu_id}", response_model=SubmenuScheme)
def update_submenu(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    updated_submenu: SubmenuSchemeCreate,
    db: Session = Depends(get_session)
):

    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    submenu = db.query(Submenu).filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id).first()
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found or does not belong to the specified menu")

    for key, value in updated_submenu.model_dump().items():
        setattr(submenu, key, value)

    db.commit()
    db.refresh(submenu)
    return submenu


@submenu_router.delete("/{menu_id}/submenus/{submenu_id}", response_model=SubmenuScheme)
def delete_submenu(menu_id: uuid.UUID, submenu_id: uuid.UUID, db: Session = Depends(get_session)):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    submenu = db.query(Submenu).filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id).first()
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found or does not belong to the specified menu")

    submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    db.delete(submenu)
    db.commit()
    return submenu
