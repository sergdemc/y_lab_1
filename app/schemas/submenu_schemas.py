import uuid

from pydantic import BaseModel, ConfigDict


class SubmenuSchemeCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str


class SubmenuScheme(SubmenuSchemeCreate):
    id: uuid.UUID

    class Config:
        orm_mode = True


class SubmenuWithDishCountScheme(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    dishes_count: int
