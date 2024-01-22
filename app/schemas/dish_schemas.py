import uuid
from typing import Optional

from pydantic import BaseModel


class DishSchemeCreate(BaseModel):
    title: str
    description: str
    price: str


class DishScheme(DishSchemeCreate):
    id: Optional[uuid.UUID]

    class Config:
        orm_mode = True


class DishWithSubmenu(DishScheme):
    submenu_id: int
