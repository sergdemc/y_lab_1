import uuid
from abc import ABC, abstractmethod


class IRepository(ABC):
    @abstractmethod
    def get_all(self, item_id: uuid.UUID | None):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, item_id: uuid.UUID):
        raise NotImplementedError

    @abstractmethod
    def create(self, data: dict, item_id: uuid.UUID | None):
        raise NotImplementedError

    @abstractmethod
    def update(self, item_id: uuid.UUID | None, data: dict):
        raise NotImplementedError

    @abstractmethod
    def delete(self, item_id: uuid.UUID):
        raise NotImplementedError
