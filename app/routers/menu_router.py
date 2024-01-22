import uuid

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.db import get_session
from database.models import Menu
from schemas.menu_schemas import MenuSchemeCreate, MenuScheme

menu_router = APIRouter(prefix="/menus", tags=["Menu"])


@menu_router.post("/", response_model=MenuScheme, status_code=201)
def create_menu(menu: MenuSchemeCreate, session: Session = Depends(get_session)):
    db_menu = Menu(**menu.model_dump())
    session.add(db_menu)
    session.commit()
    session.refresh(db_menu)
    return db_menu


@menu_router.get("/{menu_id}", response_model=MenuScheme)
def read_menu(menu_id: uuid.UUID, session: Session = Depends(get_session)):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


@menu_router.get("/", response_model=list[MenuScheme])
def read_menus(session: Session = Depends(get_session)):
    menus = session.query(Menu).all()
    return menus


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
