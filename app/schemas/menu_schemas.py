import uuid
from typing import Optional, List
from pydantic import BaseModel

from schemas.submenu_schemas import SubmenuScheme


class MenuSchemeCreate(BaseModel):
    title: str
    description: str


class MenuScheme(MenuSchemeCreate):
    id: Optional[uuid.UUID]

    class Config:
        orm_mode = True


class MenuWithSubmenus(MenuScheme):
    submenus: List[SubmenuScheme]

