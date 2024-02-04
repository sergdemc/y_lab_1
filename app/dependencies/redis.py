import redis
from config import REDIS_PORT, REDIS_SERVER


def cache():
    return redis.Redis(
        host=REDIS_SERVER,
        port=REDIS_PORT,
    )
