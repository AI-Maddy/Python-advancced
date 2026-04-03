"""Day 14 — Exercises: Descriptors"""
from __future__ import annotations
from typing import Any, TypeVar, Generic
T = TypeVar("T")

# Ex 1: TypedAttribute[T] descriptor with __set_name__
class TypedAttribute(Generic[T]):
    def __init__(self, expected_type: type[T]) -> None:
        self._type = expected_type
        self._name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name

    def __get__(self, obj: object | None, objtype: type) -> Any:
        if obj is None:
            return self
        value = obj.__dict__.get(self._name)
        if value is None:
            raise AttributeError(f"{self._name!r} not set")
        return value

    def __set__(self, obj: object, value: T) -> None:
        if not isinstance(value, self._type):
            raise TypeError(
                f"{self._name!r} must be {self._type.__name__}, "
                f"got {type(value).__name__}"
            )
        obj.__dict__[self._name] = value

# Ex 2: Clamped descriptor — clamp to [min_val, max_val]
class Clamped:
    def __init__(self, min_val: float, max_val: float) -> None:
        self._min = min_val; self._max = max_val
        self._name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name

    def __get__(self, obj: object | None, objtype: type) -> Any:
        if obj is None:
            return self
        return obj.__dict__.get(self._name, self._min)

    def __set__(self, obj: object, value: float) -> None:
        obj.__dict__[self._name] = max(self._min, min(self._max, value))

# Ex 3: LazyProperty non-data descriptor
class LazyProperty:
    def __init__(self, func: Any) -> None:
        self._func = func
        self.__doc__ = func.__doc__
        self._name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name

    def __get__(self, obj: object | None, objtype: type) -> Any:
        if obj is None:
            return self
        value = self._func(obj)
        obj.__dict__[self._name] = value
        return value

if __name__ == "__main__":
    class Person:
        name = TypedAttribute(str)
        age = TypedAttribute(int)
        def __init__(self, name: str, age: int) -> None:
            self.name = name; self.age = age
    p = Person("Alice", 30)
    print(p.name, p.age)
