"""
Mixin Idiom — cooperative multiple inheritance.

Demonstrates:
* LoggingMixin
* ValidationMixin
* SerializationMixin
* MRO (Method Resolution Order) with super()
"""
from __future__ import annotations

import json
import logging
from typing import Any


# ---------------------------------------------------------------------------
# Mixins
# ---------------------------------------------------------------------------
class LoggingMixin:
    """Adds a ``logger`` attribute and ``log()`` helper to any class.

    The logger name is set to the class's fully-qualified name.
    """

    @property
    def logger(self) -> logging.Logger:
        return logging.getLogger(type(self).__qualname__)

    def log(self, level: str, message: str) -> None:
        """Log a message at the given level (debug/info/warning/error)."""
        getattr(self.logger, level.lower())(message)


class ValidationMixin:
    """Adds ``validate()`` hook; subclasses override ``_rules()``."""

    def _rules(self) -> list[tuple[bool, str]]:
        """Return a list of (condition, error_message) pairs.

        Override in subclasses to add validation rules.
        """
        return []

    def validate(self) -> None:
        """Run all validation rules and raise ValueError for the first failure.

        Raises:
            ValueError: if any rule condition is False.
        """
        for condition, message in self._rules():
            if not condition:
                raise ValueError(message)


class SerializationMixin:
    """Adds ``to_json()`` and ``from_json()`` to any class.

    Relies on instance ``__dict__`` for serialisation; requires that the
    class has a matching ``__init__`` or ``from_dict`` classmethod.
    """

    def to_json(self) -> str:
        """Serialise public attributes to a JSON string."""
        return json.dumps(
            {k: v for k, v in self.__dict__.items() if not k.startswith("_")},
            default=str,
        )

    @classmethod
    def from_json(cls, json_str: str) -> Any:
        """Deserialise from a JSON string (uses ``**kwargs`` constructor)."""
        data = json.loads(json_str)
        # Remap 'id' → 'id_' if constructor uses 'id_' parameter name
        if "id" in data and "id_" not in data:
            data["id_"] = data.pop("id")
        return cls(**data)


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------
class Entity:
    """Base domain entity."""

    def __init__(self, id_: int) -> None:
        self.id = id_

    def __repr__(self) -> str:
        return f"{type(self).__name__}(id={self.id})"


# ---------------------------------------------------------------------------
# Combined classes
# ---------------------------------------------------------------------------
class User(LoggingMixin, ValidationMixin, SerializationMixin, Entity):
    """A user entity with logging, validation, and serialisation.

    MRO: User → LoggingMixin → ValidationMixin → SerializationMixin → Entity → object
    """

    def __init__(self, id_: int, name: str, age: int) -> None:
        super().__init__(id_)
        self.name = name
        self.age = age

    def _rules(self) -> list[tuple[bool, str]]:
        return [
            (isinstance(self.name, str) and len(self.name) > 0, "name must be non-empty"),
            (isinstance(self.age, int) and self.age >= 0, "age must be non-negative"),
        ]

    def save(self) -> None:
        """Validate, log, and simulate persistence."""
        self.validate()
        self.log("info", f"Saving user id={self.id}")


class AuditedUser(User):
    """Extends User with extra audit trail.

    MRO: AuditedUser → LoggingMixin → User → … → object
    """

    def __init__(self, id_: int, name: str, age: int) -> None:
        super().__init__(id_=id_, name=name, age=age)
        self.audit_log: list[str] = []

    def save(self) -> None:
        self.audit_log.append(f"save:id={self.id}")
        super().save()


# ---------------------------------------------------------------------------
# MRO demonstration
# ---------------------------------------------------------------------------
def show_mro(cls: type) -> list[str]:
    """Return the class names in MRO order."""
    return [c.__name__ for c in cls.__mro__]


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")

    u = User(1, "Alice", 30)
    u.save()
    print(f"JSON: {u.to_json()}")

    restored = User.from_json(u.to_json())
    print(f"Restored: {restored!r}")

    try:
        bad = User(2, "", 25)
        bad.validate()
    except ValueError as e:
        print(f"Validation: {e}")

    print(f"\nUser MRO: {show_mro(User)}")
    print(f"AuditedUser MRO: {show_mro(AuditedUser)}")

    au = AuditedUser(3, "Bob", 25)
    au.save()
    print(f"Audit log: {au.audit_log}")
