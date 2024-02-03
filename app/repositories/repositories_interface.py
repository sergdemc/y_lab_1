import uuid
from abc import ABC, abstractmethod


class IRepository(ABC):
    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: uuid.UUID):
        raise NotImplementedError

    @abstractmethod
    def create(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    def update(self, id: uuid.UUID, data: dict):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: uuid.UUID):
        raise NotImplementedError
