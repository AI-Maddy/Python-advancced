"""
Day 20 — Solutions: Metaclasses & Class Internals
===================================================
"""
from __future__ import annotations

import math
from collections import OrderedDict
from typing import Any, ClassVar


# ---------------------------------------------------------------------------
# Solution 1 — RegistryMeta
# ---------------------------------------------------------------------------

class RegistryMeta(type):
    """Auto-register concrete subclasses (non-_ prefix)."""

    def __init__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> None:
        super().__init__(name, bases, namespace)
        if not hasattr(cls, "_registry"):
            cls._registry: dict[str, type] = {}
        elif not name.startswith("_"):
            cls._registry[name] = cls


class _Formatter(metaclass=RegistryMeta):
    """Abstract base formatter — not registered."""

    def format(self, data: dict[str, Any]) -> str:
        raise NotImplementedError

    @classmethod
    def get(cls, name: str) -> type[_Formatter]:
        """Retrieve registered class by name."""
        return cls._registry[name]


class HtmlFormatter(_Formatter):
    def format(self, data: dict[str, Any]) -> str:
        items = "".join(f"<li>{k}: {v}</li>" for k, v in data.items())
        return f"<ul>{items}</ul>"


class PlainFormatter(_Formatter):
    def format(self, data: dict[str, Any]) -> str:
        return ", ".join(f"{k}={v}" for k, v in data.items())


def exercise1_registry() -> tuple[str, str]:
    data = {"name": "Alice", "age": 30}
    html = _Formatter.get("HtmlFormatter")().format(data)
    plain = _Formatter.get("PlainFormatter")().format(data)
    return (html, plain)


# ---------------------------------------------------------------------------
# Solution 2 — SingletonMeta
# ---------------------------------------------------------------------------

class SingletonMeta(type):
    """Singleton metaclass."""

    _instances: ClassVar[dict[type, Any]] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in SingletonMeta._instances:
            SingletonMeta._instances[cls] = super().__call__(*args, **kwargs)
        return SingletonMeta._instances[cls]


class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self, dsn: str = "sqlite:///:memory:") -> None:
        self.dsn = dsn
        self.connected: bool = True


def exercise2_singleton() -> tuple[bool, str]:
    # Clear singleton cache for test isolation
    SingletonMeta._instances.pop(DatabaseConnection, None)
    conn1 = DatabaseConnection("postgres://localhost/db")
    conn2 = DatabaseConnection("ignored")
    conn1.dsn = "mysql://server/db"
    return (conn1 is conn2, conn2.dsn)


# ---------------------------------------------------------------------------
# Solution 3 — Ordered attribute tracking
# ---------------------------------------------------------------------------

class OrderedFieldMeta(type):
    """Track attribute definition order."""

    @classmethod
    def __prepare__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        **kwargs: Any,
    ) -> OrderedDict[str, Any]:
        return OrderedDict()

    def __new__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        namespace: OrderedDict[str, Any],
        **kwargs: Any,
    ) -> OrderedFieldMeta:
        cls = super().__new__(mcs, name, bases, dict(namespace))
        cls._field_order: list[str] = [
            k for k in namespace if not k.startswith("__")
        ]
        return cls


class FormFields(metaclass=OrderedFieldMeta):
    first_name: str = ""
    last_name: str = ""
    email: str = ""


def exercise3_ordered_fields() -> list[str]:
    return FormFields._field_order


# ---------------------------------------------------------------------------
# Solution 4 — __init_subclass__ validation
# ---------------------------------------------------------------------------

class Model:
    """Base ORM model with table_name enforcement."""

    table_name: ClassVar[str] = ""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if not getattr(cls, "table_name", ""):
            raise TypeError(
                f"Class {cls.__name__} must define 'table_name' class variable"
            )


class UserModel(Model):
    table_name = "users"
    name: str = ""


def exercise4_init_subclass() -> tuple[str, bool]:
    raised = False
    try:
        class BadModel(Model):
            pass
    except TypeError:
        raised = True
    return (UserModel.table_name, raised)


# ---------------------------------------------------------------------------
# Solution 5 — Dynamic class creation with type()
# ---------------------------------------------------------------------------

def exercise5_dynamic_class() -> tuple[str, float]:
    def _init(self: Any, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def _distance(self: Any) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def _repr(self: Any) -> str:
        return f"Point(x={self.x}, y={self.y})"

    Point = type(
        "Point",
        (object,),
        {"__init__": _init, "distance": _distance, "__repr__": _repr},
    )

    p = Point(3, 4)  # type: ignore[call-arg]
    return (type(Point).__name__, p.distance())


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Solution 1:", exercise1_registry())
    print("Solution 2:", exercise2_singleton())
    print("Solution 3:", exercise3_ordered_fields())
    print("Solution 4:", exercise4_init_subclass())
    print("Solution 5:", exercise5_dynamic_class())
