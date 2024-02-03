import redis

from config import REDIS_SERVER, REDIS_PORT


def cache():
    return redis.Redis(
        host=REDIS_SERVER,
        port=REDIS_PORT,
    )
