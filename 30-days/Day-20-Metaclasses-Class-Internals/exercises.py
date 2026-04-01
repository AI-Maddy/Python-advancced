"""
Day 20 — Exercises: Metaclasses & Class Internals
===================================================
Complete each TODO.
"""
from __future__ import annotations

from collections import OrderedDict
from typing import Any, ClassVar


# ---------------------------------------------------------------------------
# Exercise 1 — RegistryMeta for plugin system
# ---------------------------------------------------------------------------
# TODO: Implement a RegistryMeta metaclass.
#       All non-abstract subclasses are auto-registered in a dict by class name.
#       Abstract classes have a name starting with '_' (excluded from registry).
#       Implement get(name) classmethod on the base class.

class RegistryMeta(type):
    """TODO: Auto-register concrete subclasses."""

    def __init__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> None:
        # TODO
        ...


class _Formatter(metaclass=RegistryMeta):
    """Abstract base formatter — not registered."""

    def format(self, data: dict[str, Any]) -> str:
        raise NotImplementedError

    @classmethod
    def get(cls, name: str) -> type[_Formatter]:
        """TODO: retrieve registered class by name."""
        # TODO
        ...
        raise KeyError(name)


class HtmlFormatter(_Formatter):
    """Formats as HTML."""

    def format(self, data: dict[str, Any]) -> str:
        items = "".join(f"<li>{k}: {v}</li>" for k, v in data.items())
        return f"<ul>{items}</ul>"


class PlainFormatter(_Formatter):
    """Formats as plain key=value pairs."""

    def format(self, data: dict[str, Any]) -> str:
        return ", ".join(f"{k}={v}" for k, v in data.items())


def exercise1_registry() -> tuple[str, str]:
    """
    Return (html_output, plain_output) for {"name": "Alice", "age": 30}.
    Expected: ('<ul><li>name: Alice</li><li>age: 30</li></ul>', 'name=Alice, age=30')
    """
    # TODO
    ...
    return ("", "")


# ---------------------------------------------------------------------------
# Exercise 2 — SingletonMeta
# ---------------------------------------------------------------------------
# TODO: Implement SingletonMeta so that:
#   - Only one instance per class is ever created.
#   - DatabaseConnection() is DatabaseConnection() → True

class SingletonMeta(type):
    """TODO: implement singleton behaviour."""

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        # TODO
        ...


class DatabaseConnection(metaclass=SingletonMeta):
    """Singleton database connection."""

    def __init__(self, dsn: str = "sqlite:///:memory:") -> None:
        self.dsn = dsn
        self.connected: bool = True


def exercise2_singleton() -> tuple[bool, str]:
    """
    Return (is_same_instance, dsn_after_change).
    Create two DatabaseConnections, verify same instance, change dsn on one,
    check the other reflects the change.
    """
    # TODO
    ...
    return (False, "")


# ---------------------------------------------------------------------------
# Exercise 3 — Ordered attribute tracking with __prepare__
# ---------------------------------------------------------------------------
# TODO: Implement an OrderedFieldMeta metaclass that:
#   - Uses OrderedDict as namespace in __prepare__
#   - After class creation, stores non-dunder attribute names in _field_order
#   - Verify FormFields._field_order == ["first_name", "last_name", "email"]

class OrderedFieldMeta(type):
    """TODO: track attribute definition order."""

    @classmethod
    def __prepare__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        **kwargs: Any,
    ) -> OrderedDict[str, Any]:
        # TODO
        ...
        return OrderedDict()

    def __new__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        namespace: OrderedDict[str, Any],
        **kwargs: Any,
    ) -> OrderedFieldMeta:
        # TODO: create class and attach _field_order
        ...
        return super().__new__(mcs, name, bases, dict(namespace))


class FormFields(metaclass=OrderedFieldMeta):
    """HTML form fields (defined in order)."""
    first_name: str = ""
    last_name: str = ""
    email: str = ""


def exercise3_ordered_fields() -> list[str]:
    """Return FormFields._field_order. Expected: ['first_name', 'last_name', 'email']."""
    # TODO
    ...
    return []


# ---------------------------------------------------------------------------
# Exercise 4 — __init_subclass__ validation
# ---------------------------------------------------------------------------
# TODO: Create a base class Model that:
#   - Uses __init_subclass__ to enforce every subclass has a 'table_name' class var.
#   - Raises TypeError at class definition time if 'table_name' is missing.

class Model:
    """Base ORM model."""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        # TODO: check cls.table_name exists; raise TypeError if missing
        ...

    table_name: ClassVar[str] = ""


class UserModel(Model):
    """TODO: uncomment and set table_name = 'users'."""
    table_name = "users"
    name: str = ""


def exercise4_init_subclass() -> tuple[str, bool]:
    """
    Return (UserModel.table_name, missing_raises_TypeError).
    """
    # Check missing table_name raises
    raised = False
    try:
        class BadModel(Model):
            pass  # no table_name!
    except TypeError:
        raised = True

    return (UserModel.table_name, raised)


# ---------------------------------------------------------------------------
# Exercise 5 — Dynamic class creation with type()
# ---------------------------------------------------------------------------
# TODO: Use type() to dynamically create a class 'Point' with:
#   - __init__(self, x: float, y: float) storing self.x and self.y
#   - distance(self) method returning sqrt(x^2 + y^2)
#   - __repr__ returning "Point(x=..., y=...)"
# Return type(PointClass).__name__ and Point(3, 4).distance()

def exercise5_dynamic_class() -> tuple[str, float]:
    """Return (metaclass_name, distance_for_3_4). Expected: ('type', 5.0)."""
    import math
    # TODO: build Point with type()
    ...
    return ("", 0.0)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Exercise 1:", exercise1_registry())
    print("Exercise 2:", exercise2_singleton())
    print("Exercise 3:", exercise3_ordered_fields())
    print("Exercise 4:", exercise4_init_subclass())
    print("Exercise 5:", exercise5_dynamic_class())
