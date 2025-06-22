import os
from functools import lru_cache

import redis


class CacheConfig:
    """Configuration for Redis cache connection."""

    def __init__(self):
        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = int(os.getenv("REDIS_PORT", 6379))
        self.db = int(os.getenv("REDIS_DB", 0))
        self.uri = os.getenv("REDIS_URI", None)


class RedisCache:
    """Redis cache client wrapper."""

    def __init__(self, config: CacheConfig = None):
        if config is None:
            config = CacheConfig()

        # Initialize Redis connection
        if config.uri:
            self.cache = redis.Redis.from_url(config.uri)
        else:
            self.cache = redis.Redis(
                host=config.host,
                port=config.port,
                db=config.db
            )

        # Test connection
        try:
            self.cache.ping()
        except redis.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Redis: {e}") from e

    def get_cache(self):
        """Get the Redis client instance."""
        return self.cache


@lru_cache(maxsize=1)
def get_cache():
    """Get a cached Redis client instance."""
    return RedisCache().get_cache()
