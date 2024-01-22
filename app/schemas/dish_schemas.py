import uuid

from pydantic import BaseModel, ConfigDict


class DishSchemeCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str
    price: str


class DishScheme(DishSchemeCreate):
    id: uuid.UUID

    class Config:
        orm_mode = True
