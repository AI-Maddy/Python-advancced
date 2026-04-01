"""
Abstract Base Class Idiom.

Demonstrates:
* abc.ABC, @abstractmethod, @classmethod + @abstractmethod, @property + @abstractmethod
* abc.ABCMeta directly
* __subclasshook__ for virtual subclasses
* collections.abc — Sequence, Mapping, Iterable, Iterator
"""
from __future__ import annotations

import abc
from abc import ABC, ABCMeta, abstractmethod
from collections.abc import Iterable, Iterator, Mapping, MutableSequence, Sequence
from typing import Any


# ---------------------------------------------------------------------------
# 1. abc.ABC with @abstractmethod
# ---------------------------------------------------------------------------
class Shape(ABC):
    """Abstract shape — subclasses must implement area() and perimeter()."""

    @abstractmethod
    def area(self) -> float:
        """Return the area of the shape."""

    @abstractmethod
    def perimeter(self) -> float:
        """Return the perimeter of the shape."""

    @classmethod
    @abstractmethod
    def from_string(cls, s: str) -> Shape:
        """Parse a shape from a string representation."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of this shape type."""

    def describe(self) -> str:
        return f"{self.name}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self._radius = radius

    def area(self) -> float:
        import math
        return math.pi * self._radius ** 2

    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self._radius

    @classmethod
    def from_string(cls, s: str) -> Circle:
        return cls(float(s.split("=")[1]))

    @property
    def name(self) -> str:
        return "Circle"


class Rectangle(Shape):
    def __init__(self, w: float, h: float) -> None:
        self._w = w
        self._h = h

    def area(self) -> float:
        return self._w * self._h

    def perimeter(self) -> float:
        return 2 * (self._w + self._h)

    @classmethod
    def from_string(cls, s: str) -> Rectangle:
        parts = s.split(",")
        return cls(float(parts[0]), float(parts[1]))

    @property
    def name(self) -> str:
        return "Rectangle"


# ---------------------------------------------------------------------------
# 2. ABCMeta directly (equivalent to abc.ABC)
# ---------------------------------------------------------------------------
class Animal(metaclass=ABCMeta):
    """Abstract animal using ABCMeta directly."""

    @abstractmethod
    def speak(self) -> str: ...


class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"


# ---------------------------------------------------------------------------
# 3. __subclasshook__ — virtual subclasses
# ---------------------------------------------------------------------------
class Drawable(ABC):
    """ABC that accepts any class with a .draw() method as a virtual subclass."""

    @abstractmethod
    def draw(self) -> str: ...

    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        if cls is Drawable:
            return callable(getattr(subclass, "draw", None))
        return NotImplemented


class ExternalShape:
    """Third-party class — no explicit inheritance from Drawable."""

    def draw(self) -> str:
        return "ExternalShape drawn"


# ---------------------------------------------------------------------------
# 4. collections.abc: Sequence, Mapping, Iterable, Iterator
# ---------------------------------------------------------------------------
class FrozenList(Sequence):
    """Immutable sequence backed by a tuple — implements Sequence ABC."""

    def __init__(self, items: Iterable) -> None:
        self._data = tuple(items)

    def __getitem__(self, index: int) -> Any:
        return self._data[index]

    def __len__(self) -> int:
        return len(self._data)


class RangeIterator:
    """Custom iterator implementing the Iterator ABC."""

    def __init__(self, start: int, stop: int) -> None:
        self._current = start
        self._stop = stop

    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> int:
        if self._current >= self._stop:
            raise StopIteration
        value = self._current
        self._current += 1
        return value


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    shapes: list[Shape] = [Circle(5.0), Rectangle(4.0, 3.0)]
    for s in shapes:
        print(s.describe())

    # Cannot instantiate abstract class
    try:
        Shape()  # type: ignore[abstract]
    except TypeError as e:
        print(f"\nInstantiation blocked: {e}")

    # from_string
    c = Circle.from_string("r=7.0")
    print(f"from_string: {c.describe()}")

    # Virtual subclass via __subclasshook__
    ext = ExternalShape()
    print(f"\nExternalShape isinstance(Drawable): {isinstance(ext, Drawable)}")  # True

    # FrozenList (Sequence ABC)
    fl = FrozenList([3, 1, 4, 1, 5])
    print(f"\nFrozenList: {list(fl)}, len={len(fl)}")
    print(f"fl[2] = {fl[2]}")
    # Sequence ABC provides __contains__, __reversed__, index, count for free
    print(f"4 in fl: {4 in fl}")
    print(f"count(1): {fl.count(1)}")

    # Iterator
    it = RangeIterator(0, 5)
    print(f"\nRangeIterator: {list(it)}")
    print(f"isinstance(Iterable): {isinstance(it, Iterable)}")
    print(f"isinstance(Iterator): {isinstance(it, Iterator)}")
