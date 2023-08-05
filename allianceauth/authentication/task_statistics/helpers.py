"""Helpers for Task Statistics."""

import logging
from typing import Optional

from redis import Redis, RedisError

from django.core.cache import cache

from allianceauth.utils.cache import get_redis_client

logger = logging.getLogger(__name__)


class _RedisStub:
    """Stub of a Redis client.

    It's purpose is to prevent EventSeries objects from trying to access Redis
    when it is not available. e.g. when the Sphinx docs are rendered by readthedocs.org.
    """

    IS_STUB = True

    def delete(self, *args, **kwargs):
        pass

    def incr(self, *args, **kwargs):
        return 0

    def zadd(self, *args, **kwargs):
        pass

    def zcount(self, *args, **kwargs):
        pass

    def zrangebyscore(self, *args, **kwargs):
        pass


class ItemCounter:
    """A process safe item counter.

    Args:
        - name: Unique name for the counter
        - minimum: Counter can not go below the minimum, when set
        - redis: A Redis client. Will use AA's cache client by default
    """

    CACHE_KEY_BASE = "allianceauth-item-counter"
    DEFAULT_CACHE_TIMEOUT = 24 * 3600

    def __init__(
        self, name: str, minimum: Optional[int] = None, redis: Optional[Redis] = None
    ) -> None:
        if not name:
            raise ValueError("Must define a name")

        self._name = str(name)
        self._minimum = minimum
        self._redis = get_redis_client_or_stub() if not redis else redis

    @property
    def _cache_key(self) -> str:
        return f"{self.CACHE_KEY_BASE}-{self._name}"

    def reset(self, init_value: int = 0):
        """Reset counter to initial value."""
        with self._redis.lock(f"{self.CACHE_KEY_BASE}-reset"):
            if self._minimum is not None and init_value < self._minimum:
                raise ValueError("Can not reset below minimum")

            cache.set(self._cache_key, init_value, self.DEFAULT_CACHE_TIMEOUT)

    def incr(self, delta: int = 1):
        """Increment counter by delta."""
        try:
            cache.incr(self._cache_key, delta)
        except ValueError:
            pass

    def decr(self, delta: int = 1):
        """Decrement counter by delta."""
        with self._redis.lock(f"{self.CACHE_KEY_BASE}-decr"):
            if self._minimum is not None and self.value() == self._minimum:
                return
            try:
                cache.decr(self._cache_key, delta)
            except ValueError:
                pass

    def value(self) -> Optional[int]:
        """Return current value or None if not yet initialized."""
        return cache.get(self._cache_key)


def get_redis_client_or_stub() -> Redis:
    """Return AA's default cache client or a stub if Redis is not available."""
    redis = get_redis_client()
    try:
        if not redis.ping():
            raise RuntimeError()
    except (AttributeError, RedisError, RuntimeError):
        logger.exception(
            "Failed to establish a connection with Redis. "
            "This EventSeries object is disabled.",
        )
        return _RedisStub()
    return redis
