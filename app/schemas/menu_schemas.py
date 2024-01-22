import uuid
from typing import List

from pydantic import BaseModel
from schemas.submenu_schemas import SubmenuScheme


class MenuSchemeCreate(BaseModel):
    title: str
    description: str


class MenuScheme(MenuSchemeCreate):
    id: uuid.UUID

    class Config:
        orm_mode = True


class MenuWithSubmenus(MenuScheme):
    submenus: List[SubmenuScheme]


class MenuWithDetailsScheme(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    submenus_count: int
    dishes_count: int
