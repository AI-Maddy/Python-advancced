"""Day 14 — Solutions: Descriptors and Properties"""
from __future__ import annotations
from typing import Any, TypeVar, Generic, overload

T = TypeVar("T")


class TypedAttribute(Generic[T]):
    """Descriptor: validates type on assignment."""

    def __init__(self, expected_type: type[T]) -> None:
        self._type = expected_type
        self._name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name

    @overload
    def __get__(self, obj: None, objtype: type) -> "TypedAttribute[T]": ...
    @overload
    def __get__(self, obj: object, objtype: type) -> T: ...

    def __get__(self, obj: object | None, objtype: type) -> "TypedAttribute[T] | T":
        if obj is None:
            return self
        value = obj.__dict__.get(self._name)
        if value is None:
            raise AttributeError(f"{self._name!r} not set")
        return value  # type: ignore[return-value]

    def __set__(self, obj: object, value: T) -> None:
        if not isinstance(value, self._type):
            raise TypeError(
                f"{self._name!r} must be {self._type.__name__}, "
                f"got {type(value).__name__}"
            )
        obj.__dict__[self._name] = value

    def __delete__(self, obj: object) -> None:
        obj.__dict__.pop(self._name, None)


class Clamped:
    """Descriptor: clamps numeric value to [min_val, max_val]."""

    def __init__(self, min_val: float, max_val: float) -> None:
        self._min = min_val
        self._max = max_val
        self._name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name

    def __get__(self, obj: object | None, objtype: type) -> float | "Clamped":
        if obj is None:
            return self
        return obj.__dict__.get(self._name, self._min)  # type: ignore[return-value]

    def __set__(self, obj: object, value: float) -> None:
        obj.__dict__[self._name] = max(self._min, min(self._max, value))


class LazyProperty:
    """Non-data descriptor: computes value once, then caches on instance."""

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
        # Cache on the instance dict — next access won't call __get__
        obj.__dict__[self._name] = value
        return value


class Person:
    name = TypedAttribute(str)
    age = TypedAttribute(int)

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        return f"Person(name={self.name!r}, age={self.age})"


class Clipped:
    value = Clamped(0.0, 100.0)
    volume = Clamped(0.0, 1.0)

    def __init__(self, value: float, volume: float) -> None:
        self.value = value
        self.volume = volume


class ExpensiveObject:
    def __init__(self, n: int) -> None:
        self.n = n
        self._computed = 0

    @LazyProperty
    def computed(self) -> int:
        """Expensive computation."""
        self._computed += 1
        return sum(range(self.n))


if __name__ == "__main__":
    p = Person("Alice", 30)
    print(p)
    try:
        p.age = "thirty"  # type: ignore[assignment]
    except TypeError as e:
        print(e)

    c = Clipped(150.0, 2.0)
    print(c.value, c.volume)   # 100.0, 1.0

    obj = ExpensiveObject(100)
    print(obj.computed)        # computed once
    print(obj.computed)        # from instance cache
    print(obj._computed)       # 1 — computed only once
