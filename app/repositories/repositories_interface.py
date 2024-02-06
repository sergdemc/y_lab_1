import uuid
from abc import ABC, abstractmethod


class IRepository(ABC):
    @abstractmethod
    def get_all(self, item_id: uuid.UUID | None) -> list[dict] | dict:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, item_id: uuid.UUID) -> dict:
        raise NotImplementedError

    @abstractmethod
    def create(self, data: dict, item_id: uuid.UUID | None) -> dict:
        raise NotImplementedError

    @abstractmethod
    def update(self, item_id: uuid.UUID | None, data: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    def delete(self, item_id: uuid.UUID) -> dict:
        raise NotImplementedError
