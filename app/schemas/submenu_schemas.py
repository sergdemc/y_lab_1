import uuid
from typing import Optional
from pydantic import BaseModel

from schemas.dish_schemas import DishScheme


class SubmenuSchemeCreate(BaseModel):
    title: str
    description: str


class SubmenuScheme(SubmenuSchemeCreate):
    id: Optional[uuid.UUID]

    class Config:
        orm_mode = True


class SubmenuWithDishes(SubmenuScheme):
    dishes: list[DishScheme]
