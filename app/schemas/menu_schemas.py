import uuid

from pydantic import BaseModel


class MenuSchemeCreate(BaseModel):
    title: str
    description: str


class MenuScheme(MenuSchemeCreate):
    id: uuid.UUID

    class Config:
        orm_mode = True


class MenuWithDetailsScheme(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    submenus_count: int
    dishes_count: int
