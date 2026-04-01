"""
Singleton Pattern — three idiomatic Python approaches.

1. __new__ override (thread-safe with threading.Lock)
2. Module-level singleton (most Pythonic)
3. @singleton decorator
"""
from __future__ import annotations

import threading
from typing import Any, TypeVar

F = TypeVar("F", bound=type)


# ---------------------------------------------------------------------------
# Approach 1: __new__ with threading.Lock
# ---------------------------------------------------------------------------
class SingletonMeta(type):
    """Thread-safe Singleton metaclass."""

    _instances: dict[type, Any] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class DatabasePool(metaclass=SingletonMeta):
    """Thread-safe connection pool — only one instance ever created.

    Args:
        max_connections: Maximum number of simultaneous DB connections.
    """

    def __init__(self, max_connections: int = 10) -> None:
        self.max_connections = max_connections
        self._pool: list[str] = []

    def acquire(self) -> str:
        """Acquire a connection handle."""
        handle = f"conn-{len(self._pool)}"
        self._pool.append(handle)
        return handle

    def release(self, handle: str) -> None:
        """Release a connection back to the pool."""
        self._pool.remove(handle)

    def __repr__(self) -> str:
        return f"DatabasePool(max={self.max_connections}, active={len(self._pool)})"


# ---------------------------------------------------------------------------
# Approach 2: __new__ override directly on a class
# ---------------------------------------------------------------------------
_singleton_lock = threading.Lock()


class ConfigRegistry:
    """Application-wide config store using __new__-based singleton.

    Only one ConfigRegistry will ever exist regardless of how many
    times ConfigRegistry() is called.
    """

    _instance: ConfigRegistry | None = None

    def __new__(cls) -> ConfigRegistry:
        with _singleton_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._data: dict[str, Any] = {}
        return cls._instance

    def set(self, key: str, value: Any) -> None:
        """Store a configuration value."""
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a configuration value."""
        return self._data.get(key, default)

    def __repr__(self) -> str:
        return f"ConfigRegistry({self._data})"


# ---------------------------------------------------------------------------
# Approach 3: @singleton decorator
# ---------------------------------------------------------------------------
def singleton(cls: type[F]) -> type[F]:
    """Class decorator that turns any class into a singleton.

    Usage::

        @singleton
        class MyService:
            ...
    """
    instances: dict[type, Any] = {}
    lock = threading.Lock()

    def get_instance(*args: Any, **kwargs: Any) -> F:
        with lock:
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
        return instances[cls]  # type: ignore[return-value]

    return get_instance  # type: ignore[return-value]


@singleton
class AppLogger:
    """Application-wide logger (singleton via decorator)."""

    def __init__(self) -> None:
        self.entries: list[str] = []

    def log(self, message: str) -> None:
        """Append a log entry."""
        self.entries.append(message)

    def __repr__(self) -> str:
        return f"AppLogger(entries={len(self.entries)})"


# ---------------------------------------------------------------------------
# Module-level singleton (most Pythonic — just use a module attribute)
# ---------------------------------------------------------------------------
class _ModuleSingleton:
    """Backing class — users import ``module_singleton``, not this."""

    def __init__(self) -> None:
        self.value: int = 0

    def increment(self) -> None:
        self.value += 1


module_singleton = _ModuleSingleton()
"""The one-and-only module-level singleton instance.  Import and use it
directly — no instantiation required."""


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # DatabasePool (metaclass)
    p1 = DatabasePool(max_connections=5)
    p2 = DatabasePool(max_connections=99)
    print(f"Same pool? {p1 is p2}")  # True
    print(p1)

    # ConfigRegistry (__new__)
    r1 = ConfigRegistry()
    r1.set("debug", True)
    r2 = ConfigRegistry()
    print(f"debug via r2: {r2.get('debug')}")  # True
    print(f"Same registry? {r1 is r2}")  # True

    # AppLogger (decorator)
    lg1 = AppLogger()
    lg2 = AppLogger()
    lg1.log("hello")
    print(f"lg2 entries: {lg2.entries}")  # ['hello']
    print(f"Same logger? {lg1 is lg2}")  # True

    # Module singleton
    module_singleton.increment()
    print(f"module_singleton.value = {module_singleton.value}")  # 1
