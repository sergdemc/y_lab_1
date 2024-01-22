import datetime
import uuid
from typing import List
from typing_extensions import Annotated
from sqlalchemy import ForeignKey, text, UUID, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.db import Base


intpk = Annotated[uuid.UUID, mapped_column(primary_key=True, index=True, default=uuid.uuid4, unique=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', NOW())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', NOW())"),
        onupdate=datetime.datetime.utcnow
    )]


class Menu(Base):
    __tablename__ = "menus"

    id: Mapped[intpk]
    title: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    submenus: Mapped[List["Submenu"]] = relationship(back_populates="menu")


class Submenu(Base):
    __tablename__ = "submenus"

    id: Mapped[intpk]
    title: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    menu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("menus.id", ondelete="CASCADE"))
    menu: Mapped["Menu"] = relationship("Menu", back_populates="submenus")

    dishes: Mapped[List["Dish"]] = relationship(back_populates="submenu")


class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[intpk]
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    submenu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("submenus.id", ondelete="CASCADE"))
    submenu: Mapped["Submenu"] = relationship(back_populates="dishes")
