"""
Metaclass Idiom.

Demonstrates:
* SingletonMeta — enforces singleton pattern at the metaclass level.
* RegistryMeta  — auto-registers every subclass.
* AbstractMeta  — blocks instantiation of 'abstract' classes.
* __init_subclass__ — lighter alternative to a full metaclass.
"""
from __future__ import annotations

import threading
from abc import ABCMeta
from typing import Any


# ---------------------------------------------------------------------------
# 1. SingletonMeta
# ---------------------------------------------------------------------------
class SingletonMeta(type):
    """Metaclass that makes any class a thread-safe singleton.

    Example::

        class AppState(metaclass=SingletonMeta):
            ...
    """

    _instances: dict[type, Any] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class AppState(metaclass=SingletonMeta):
    """Application-wide state singleton."""

    def __init__(self) -> None:
        self.counter: int = 0


# ---------------------------------------------------------------------------
# 2. RegistryMeta
# ---------------------------------------------------------------------------
class RegistryMeta(type):
    """Metaclass that auto-registers every concrete subclass by name.

    The base class itself (abstract=True) is excluded.

    Example::

        class Plugin(metaclass=RegistryMeta):
            abstract = True

        class MyPlugin(Plugin):
            ...

        Plugin.registry["MyPlugin"]   # → MyPlugin
    """

    def __init__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> None:
        super().__init__(name, bases, namespace)
        if not hasattr(cls, "registry"):
            cls.registry: dict[str, type] = {}
        if not namespace.get("abstract", False):
            cls.registry[name] = cls


class Plugin(metaclass=RegistryMeta):
    abstract = True

    def run(self) -> str:
        return "base"


class PluginA(Plugin):
    def run(self) -> str:
        return "PluginA output"


class PluginB(Plugin):
    def run(self) -> str:
        return "PluginB output"


# ---------------------------------------------------------------------------
# 3. AbstractMeta — blocks instantiation if required methods are missing
# ---------------------------------------------------------------------------
class AbstractMeta(ABCMeta):
    """Metaclass that raises TypeError if a required class attribute is absent."""

    _required: tuple[str, ...] = ()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        for attr in getattr(cls, "_required", ()):
            if not hasattr(cls, attr) or getattr(cls, attr) is None:
                raise TypeError(
                    f"Cannot instantiate {cls.__name__!r}: "
                    f"required attribute {attr!r} is missing."
                )
        return super().__call__(*args, **kwargs)


# ---------------------------------------------------------------------------
# 4. __init_subclass__ — lighter alternative
# ---------------------------------------------------------------------------
class Serializable:
    """Base class that uses __init_subclass__ to enforce a 'schema' attribute."""

    schema: dict[str, type] = {}

    def __init_subclass__(cls, schema: dict[str, type] | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if schema is None:
            raise TypeError(
                f"{cls.__name__} must pass schema= keyword when subclassing Serializable"
            )
        cls.schema = schema

    def serialize(self) -> dict[str, Any]:
        return {
            k: getattr(self, k, None)
            for k in self.schema
        }


class UserRecord(Serializable, schema={"id": int, "name": str}):
    def __init__(self, id_: int, name: str) -> None:
        self.id = id_
        self.name = name


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # SingletonMeta
    s1 = AppState()
    s2 = AppState()
    s1.counter = 42
    print(f"Same singleton? {s1 is s2}")   # True
    print(f"s2.counter = {s2.counter}")    # 42

    # RegistryMeta
    print(f"\nPlugin registry: {list(Plugin.registry.keys())}")
    for name, cls in Plugin.registry.items():
        print(f"  {name}: {cls().run()}")

    # __init_subclass__
    u = UserRecord(1, "Alice")
    print(f"\nUserRecord schema: {UserRecord.schema}")
    print(f"Serialized: {u.serialize()}")

    # Missing schema raises TypeError
    try:
        class BadRecord(Serializable):  # type: ignore[call-arg]
            pass
    except TypeError as e:
        print(f"\n__init_subclass__ enforced: {e}")
