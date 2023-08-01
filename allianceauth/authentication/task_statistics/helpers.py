"""Helpers for Task Statistics."""

from typing import Optional

from django.core.cache import cache


class ItemCounter:
    """A process safe item counter."""

    CACHE_KEY_BASE = "allianceauth-item-counter"
    DEFAULT_CACHE_TIMEOUT = 24 * 3600

    def __init__(self, name: str) -> None:
        if not name:
            raise ValueError("Must define a name")

        self._name = str(name)

    @property
    def _cache_key(self) -> str:
        return f"{self.CACHE_KEY_BASE}-{self._name}"

    def reset(self, init_value: int = 0):
        """Reset counter to initial value."""
        cache.set(self._cache_key, init_value, self.DEFAULT_CACHE_TIMEOUT)

    def incr(self, delta: int = 1):
        """Increment counter by delta."""
        try:
            cache.incr(self._cache_key, delta)
        except ValueError:
            pass

    def decr(self, delta: int = 1):
        """Decrement counter by delta."""
        try:
            cache.decr(self._cache_key, delta)
        except ValueError:
            pass

    def value(self) -> Optional[int]:
        """Return current value or None if not yet initialized."""
        return cache.get(self._cache_key)
