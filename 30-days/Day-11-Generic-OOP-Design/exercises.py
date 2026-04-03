"""Day 11 — Exercises: Generic OOP Design"""
from __future__ import annotations
from typing import Generic, TypeVar
T = TypeVar("T")
ID = TypeVar("ID")
E = TypeVar("E", bound=Exception)

# Ex 1: Generic Repository[T, ID] with save, find_by_id, find_all, delete, count
class Repository(Generic[T, ID]):
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

# Ex 2: Ok[T] and Err[E] Result types with is_ok, is_err, unwrap, map
class Ok(Generic[T]):
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
        return Ok(f(self._value))  # type: ignore[operator]

    def __repr__(self) -> str:
        return f"Ok({self._value!r})"

class Err(Generic[E]):
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

# Ex 3: safe_divide and safe_parse_int returning Ok/Err
def safe_divide(a: float, b: float) -> "Ok[float] | Err[Exception]":
    if b == 0:
        return Err(ZeroDivisionError("division by zero"))
    return Ok(a / b)

def safe_parse_int(s: str) -> "Ok[int] | Err[Exception]":
    try:
        return Ok(int(s))
    except ValueError as e:
        return Err(e)

if __name__ == "__main__":
    repo: Repository[str, int] = Repository()  # type: ignore
