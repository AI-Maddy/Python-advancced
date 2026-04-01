"""Day 14 — Exercises: Descriptors"""
from __future__ import annotations
from typing import Any, TypeVar, Generic
T = TypeVar("T")

# Ex 1: TypedAttribute[T] descriptor with __set_name__
class TypedAttribute(Generic[T]):
    def __set_name__(self, owner: type, name: str) -> None: pass  # TODO
    def __get__(self, obj: object | None, objtype: type) -> Any: pass  # TODO
    def __set__(self, obj: object, value: T) -> None: pass  # TODO

# Ex 2: Clamped descriptor — clamp to [min_val, max_val]
class Clamped:
    def __init__(self, min_val: float, max_val: float) -> None:
        self._min = min_val; self._max = max_val
    def __set_name__(self, owner: type, name: str) -> None: pass  # TODO
    def __get__(self, obj: object | None, objtype: type) -> Any: pass  # TODO
    def __set__(self, obj: object, value: float) -> None: pass  # TODO

# Ex 3: LazyProperty non-data descriptor
class LazyProperty:
    def __init__(self, func: Any) -> None: self._func = func
    def __set_name__(self, owner: type, name: str) -> None: pass  # TODO
    def __get__(self, obj: object | None, objtype: type) -> Any: pass  # TODO

if __name__ == "__main__":
    class Person:
        name = TypedAttribute(str)
        age = TypedAttribute(int)
        def __init__(self, name: str, age: int) -> None:
            self.name = name; self.age = age
    p = Person("Alice", 30)
    print(p.name, p.age)
