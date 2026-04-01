"""
Descriptor Idiom.

Data descriptors implement __get__ + __set__ (and optionally __delete__)
for validated, typed, or clamped attribute access.

Non-data descriptors (only __get__) enable lazy/cached properties.
"""
from __future__ import annotations

from typing import Any, TypeVar, overload

T = TypeVar("T")


# ---------------------------------------------------------------------------
# 1. Validated — ensures a predicate holds
# ---------------------------------------------------------------------------
class Validated:
    """Data descriptor that validates values through a user-supplied predicate.

    Args:
        predicate: Callable[value] → bool.  Raises ValueError on failure.
        error_msg: Message included in the ValueError.

    Example::

        class Person:
            age = Validated(lambda v: isinstance(v, int) and v >= 0,
                            "age must be a non-negative int")
    """

    def __init__(
        self,
        predicate: Any,
        error_msg: str = "Validation failed",
    ) -> None:
        self._predicate = predicate
        self._error_msg = error_msg
        self._name: str = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        if obj is None:
            return self
        return obj.__dict__.get(self._name)

    def __set__(self, obj: Any, value: Any) -> None:
        if not self._predicate(value):
            raise ValueError(f"{self._name!r}: {self._error_msg} (got {value!r})")
        obj.__dict__[self._name] = value

    def __delete__(self, obj: Any) -> None:
        obj.__dict__.pop(self._name, None)


# ---------------------------------------------------------------------------
# 2. TypeChecked — ensures type matches
# ---------------------------------------------------------------------------
class TypeChecked:
    """Data descriptor that enforces a specific type.

    Args:
        expected_type: The required type (or tuple of types).

    Example::

        class Config:
            host = TypeChecked(str)
            port = TypeChecked(int)
    """

    def __init__(self, expected_type: type | tuple[type, ...]) -> None:
        self._type = expected_type
        self._name: str = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        if obj is None:
            return self
        return obj.__dict__.get(self._name)

    def __set__(self, obj: Any, value: Any) -> None:
        if not isinstance(value, self._type):
            raise TypeError(
                f"{self._name!r} must be {self._type!r}, got {type(value).__name__!r}"
            )
        obj.__dict__[self._name] = value

    def __delete__(self, obj: Any) -> None:
        obj.__dict__.pop(self._name, None)


# ---------------------------------------------------------------------------
# 3. Clamped — clamps numeric value to [min_val, max_val]
# ---------------------------------------------------------------------------
class Clamped:
    """Data descriptor that clamps a numeric value to [min_val, max_val].

    Args:
        min_val: Minimum allowed value.
        max_val: Maximum allowed value.
    """

    def __init__(self, min_val: float, max_val: float) -> None:
        self._min = min_val
        self._max = max_val
        self._name: str = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        if obj is None:
            return self
        return obj.__dict__.get(self._name, self._min)

    def __set__(self, obj: Any, value: float) -> None:
        obj.__dict__[self._name] = max(self._min, min(self._max, value))

    def __delete__(self, obj: Any) -> None:
        obj.__dict__.pop(self._name, None)


# ---------------------------------------------------------------------------
# 4. Non-data descriptor: CachedProperty
# ---------------------------------------------------------------------------
class CachedProperty:
    """Non-data descriptor that computes a property once and caches it.

    Equivalent to functools.cached_property but written from scratch.

    Example::

        class Circle:
            def __init__(self, r): self.r = r
            area = CachedProperty(lambda self: 3.14159 * self.r ** 2)
    """

    def __init__(self, func: Any) -> None:
        self._func = func
        self._name: str = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        if obj is None:
            return self
        if self._name not in obj.__dict__:
            obj.__dict__[self._name] = self._func(obj)
        return obj.__dict__[self._name]


# ---------------------------------------------------------------------------
# Usage examples
# ---------------------------------------------------------------------------
class Person:
    """Demonstrates Validated and TypeChecked descriptors."""

    name: str = TypeChecked(str)  # type: ignore[assignment]
    age: int = Validated(  # type: ignore[assignment]
        lambda v: isinstance(v, int) and v >= 0,
        "age must be a non-negative integer",
    )

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age


class Sensor:
    """Demonstrates Clamped descriptor."""

    temperature: float = Clamped(-40.0, 125.0)  # type: ignore[assignment]
    humidity: float = Clamped(0.0, 100.0)  # type: ignore[assignment]

    def __init__(self, temperature: float, humidity: float) -> None:
        self.temperature = temperature
        self.humidity = humidity


class Circle:
    """Demonstrates non-data CachedProperty."""

    def __init__(self, radius: float) -> None:
        self.radius = radius
        self._compute_count = 0

    def _calc_area(self) -> float:
        self._compute_count += 1
        import math
        return math.pi * self.radius ** 2

    area = CachedProperty(_calc_area)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    p = Person("Alice", 30)
    print(f"Person: {p.name}, age={p.age}")

    try:
        p.age = -5
    except ValueError as e:
        print(f"Validation error: {e}")

    try:
        p.name = 42  # type: ignore[assignment]
    except TypeError as e:
        print(f"Type error: {e}")

    s = Sensor(200.0, 150.0)   # clamped to max
    print(f"Sensor temp={s.temperature}, humidity={s.humidity}")  # 125, 100

    c = Circle(5.0)
    print(f"Area: {c.area:.4f}")
    print(f"Area again: {c.area:.4f}")
    print(f"Computed {c._compute_count} time(s)")  # 1
