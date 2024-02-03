import pickle
import redis
import uuid


class RedisCacheRepository:
    def __init__(self, redis_client: redis.Redis) -> None:
        self._redis_client = redis_client

    def set(self, key: str, value: object) -> None:
        self._redis_client.set(key, pickle.dumps(value))

    def get(self, key: str) -> object | None:
        if (cached_value := self._redis_client.get(key)) is not None:
            return pickle.loads(cached_value)
        return None

    def delete(self, key: str) -> None:
        self._redis_client.delete(key)
