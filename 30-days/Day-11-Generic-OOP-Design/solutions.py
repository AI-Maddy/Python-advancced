"""Day 11 — Solutions: Generic OOP Design"""
from __future__ import annotations

from typing import Generic, TypeVar, Protocol
from abc import abstractmethod

T = TypeVar("T")
ID = TypeVar("ID")
E = TypeVar("E", bound=Exception)


# ---------------------------------------------------------------------------
# Generic Repository Pattern
# ---------------------------------------------------------------------------

class Repository(Generic[T, ID]):
    """In-memory generic repository."""

    def __init__(self) -> None:
        self._store: dict[ID, T] = {}  # type: ignore[type-arg]

    def save(self, entity_id: "ID", entity: T) -> None:  # type: ignore[type-arg]
        self._store[entity_id] = entity  # type: ignore[index]

    def find_by_id(self, entity_id: "ID") -> T | None:  # type: ignore[type-arg]
        return self._store.get(entity_id)  # type: ignore[arg-type]

    def find_all(self) -> list[T]:
        return list(self._store.values())

    def delete(self, entity_id: "ID") -> bool:  # type: ignore[type-arg]
        if entity_id in self._store:  # type: ignore[operator]
            del self._store[entity_id]  # type: ignore[arg-type]
            return True
        return False

    def count(self) -> int:
        return len(self._store)


# ---------------------------------------------------------------------------
# Result[T, E] — Railway-oriented programming
# ---------------------------------------------------------------------------

class Ok(Generic[T]):
    """Successful result."""
    def __init__(self, value: T) -> None:
        self._value = value

    @property
    def value(self) -> T:
        return self._value

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self._value

    def map(self, f: "object") -> "Ok[object]":
        from typing import Callable
        return Ok(f(self._value))  # type: ignore[operator]

    def __repr__(self) -> str:
        return f"Ok({self._value!r})"


class Err(Generic[E]):
    """Failed result."""
    def __init__(self, error: E) -> None:
        self._error = error

    @property
    def error(self) -> E:
        return self._error

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def unwrap(self) -> "object":
        raise self._error

    def map(self, f: "object") -> "Err[E]":
        return self  # errors pass through

    def __repr__(self) -> str:
        return f"Err({self._error!r})"


Result = Ok[T] | Err[Exception]


def safe_divide(a: float, b: float) -> "Ok[float] | Err[Exception]":
    if b == 0:
        return Err(ZeroDivisionError("division by zero"))
    return Ok(a / b)


def safe_parse_int(s: str) -> "Ok[int] | Err[Exception]":
    try:
        return Ok(int(s))
    except ValueError as e:
        return Err(e)


# ---------------------------------------------------------------------------
# Generic Event System
# ---------------------------------------------------------------------------

class EventBus(Generic[T]):
    """Type-safe event bus."""

    def __init__(self) -> None:
        from typing import Callable
        self._handlers: list[Callable[[T], None]] = []

    def subscribe(self, handler: "object") -> None:
        self._handlers.append(handler)  # type: ignore[arg-type]

    def publish(self, event: T) -> None:
        for h in self._handlers:
            h(event)  # type: ignore[operator]

    def handler_count(self) -> int:
        return len(self._handlers)


if __name__ == "__main__":
    from dataclasses import dataclass

    @dataclass
    class User:
        name: str
        email: str

    repo: Repository[User, int] = Repository()  # type: ignore[type-arg]
    repo.save(1, User("Alice", "a@example.com"))
    repo.save(2, User("Bob", "b@example.com"))
    print(repo.find_by_id(1))
    print(repo.find_all())
    print(repo.count())

    r1 = safe_divide(10.0, 3.0)
    r2 = safe_divide(10.0, 0.0)
    print(r1, r1.is_ok())
    print(r2, r2.is_ok())

    bus: EventBus[str] = EventBus()
    bus.subscribe(lambda e: print(f"Handler 1: {e}"))
    bus.publish("UserCreated")
