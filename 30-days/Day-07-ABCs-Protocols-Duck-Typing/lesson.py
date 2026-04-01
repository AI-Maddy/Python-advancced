"""
Day 07 — ABCs, Protocols, and Duck Typing
==========================================

Topics:
  - Duck typing: "If it walks like a duck..."
  - abc.ABC + @abstractmethod for nominal subtyping
  - typing.Protocol for structural subtyping (PEP 544)
  - runtime_checkable + isinstance
  - collections.abc: Sequence, Mapping, Iterable, Iterator, Callable
  - __subclasshook__ for virtual subclasses
  - ABCs vs Protocols: when to use each
"""
from __future__ import annotations

import abc
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from typing import Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# 1. Duck Typing — Python's Default
# ---------------------------------------------------------------------------
# "If it walks like a duck and quacks like a duck, it's a duck."
# Python checks interface at call time, not declaration time.
# C++ requires explicit type declarations; Python requires no upfront contract.

def make_sound(animal: object) -> str:
    """Works on ANYTHING with a speak() method — no inheritance required."""
    # This would require virtual dispatch in C++ (or templates).
    # In Python, any object with .speak() works here.
    return animal.speak()  # type: ignore[union-attr]


class Dog:
    def speak(self) -> str:
        return "Woof!"


class Robot:
    """Not an Animal, but has speak() — duck typing accepts it."""
    def speak(self) -> str:
        return "Beep boop!"


def demo_duck_typing() -> None:
    for obj in [Dog(), Robot(), "not a speaker"]:
        try:
            print(make_sound(obj))
        except AttributeError as e:
            print(f"AttributeError: {e}")


# ---------------------------------------------------------------------------
# 2. ABC — Abstract Base Classes (Nominal Subtyping)
# ---------------------------------------------------------------------------
# Use ABC when you want to:
#   - Enforce that subclasses implement specific methods
#   - Create a formal is-a relationship
#   - Share implementation across subclasses

class Drawable(ABC):
    """ABC: anything that can be drawn."""

    @abstractmethod
    def draw(self) -> str:
        """Subclasses MUST implement this."""
        ...

    @abstractmethod
    def bounding_box(self) -> tuple[float, float, float, float]:
        """Return (x, y, width, height)."""
        ...

    def render_info(self) -> str:
        """Concrete method using abstract methods (NVI-like)."""
        bb = self.bounding_box()
        return f"{type(self).__name__}: drawn={self.draw()}, bb={bb}"


class CircleShape(Drawable):
    def __init__(self, cx: float, cy: float, r: float) -> None:
        self.cx = cx
        self.cy = cy
        self.r = r

    def draw(self) -> str:
        return f"Circle at ({self.cx},{self.cy}) r={self.r}"

    def bounding_box(self) -> tuple[float, float, float, float]:
        return (self.cx - self.r, self.cy - self.r, 2*self.r, 2*self.r)


class TextShape(Drawable):
    def __init__(self, text: str, x: float, y: float) -> None:
        self.text = text
        self.x = x
        self.y = y

    def draw(self) -> str:
        return f"Text '{self.text}' at ({self.x},{self.y})"

    def bounding_box(self) -> tuple[float, float, float, float]:
        return (self.x, self.y, len(self.text) * 8.0, 16.0)  # rough estimate


def demo_abc() -> None:
    shapes: list[Drawable] = [
        CircleShape(0, 0, 5),
        TextShape("Hello", 10, 20),
    ]
    for s in shapes:
        print(s.render_info())

    # Cannot instantiate ABC directly
    try:
        d = Drawable()  # type: ignore[abstract]
    except TypeError as e:
        print(f"TypeError: {e}")


# ---------------------------------------------------------------------------
# 3. Protocol — Structural Subtyping (PEP 544)
# ---------------------------------------------------------------------------
# Protocol: "if it has these methods, it satisfies the interface"
# No inheritance required.
# C++ equivalent: Concepts (C++20) — check structural requirements at compile time.
# Python Protocol: checked by mypy/pyright statically; optionally at runtime.

@runtime_checkable
class Speakable(Protocol):
    """Protocol: any class with a speak() method satisfies this."""
    def speak(self) -> str:
        ...


@runtime_checkable
class Drawable2D(Protocol):
    """Protocol: anything with draw() and bounding_box() qualifies."""
    def draw(self) -> str:
        ...

    def bounding_box(self) -> tuple[float, float, float, float]:
        ...


class Car:
    """Car has speak() but does NOT inherit from Speakable."""
    def speak(self) -> str:
        return "Vroom!"


def demo_protocol() -> None:
    # Car satisfies Speakable structurally — no explicit inheritance
    car = Car()
    print(isinstance(car, Speakable))   # True — runtime_checkable!

    # Protocol isinstance only checks method existence, not signatures
    dog = Dog()
    print(isinstance(dog, Speakable))   # True

    # Works with mypy/pyright:
    # def greet(s: Speakable) -> str:
    #     return s.speak()
    # greet(Car())    # type-checks correctly!

    # CircleShape satisfies Drawable2D because it has draw() and bounding_box()
    c = CircleShape(0, 0, 5)
    print(isinstance(c, Drawable2D))   # True


# ---------------------------------------------------------------------------
# 4. ABC with __subclasshook__ — Virtual Subclasses
# ---------------------------------------------------------------------------
# __subclasshook__ lets you declare "anything with these methods IS-A MyABC"
# without requiring explicit inheritance.

class Closeable(ABC):
    """ABC that recognises any class with a close() method."""

    @abstractmethod
    def close(self) -> None:
        ...

    @classmethod
    def __subclasshook__(cls, C: type) -> bool:
        """Return True if C has a 'close' method — makes it a virtual subclass."""
        if cls is Closeable:
            if any("close" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented  # type: ignore[return-value]


class FileHandle:
    """Has close() but doesn't inherit from Closeable."""
    def close(self) -> None:
        print("File closed")


def demo_subclasshook() -> None:
    fh = FileHandle()
    print(isinstance(fh, Closeable))    # True — virtual subclass via __subclasshook__
    print(issubclass(FileHandle, Closeable))  # True


# ---------------------------------------------------------------------------
# 5. collections.abc — Built-in Abstract Base Classes
# ---------------------------------------------------------------------------

def demo_collections_abc() -> None:
    """Show how to use collections.abc for interface checks."""

    # Sequence: has __getitem__, __len__
    lst = [1, 2, 3]
    s = "hello"
    t = (1, 2, 3)
    print(isinstance(lst, Sequence))    # True
    print(isinstance(s, Sequence))      # True
    print(isinstance(t, Sequence))      # True

    # Mapping: has __getitem__, keys(), items()
    d = {"a": 1}
    print(isinstance(d, Mapping))       # True

    # Iterable: has __iter__
    print(isinstance(lst, Iterable))    # True
    print(isinstance(42, Iterable))     # False

    # Iterator: has __iter__ and __next__
    it = iter([1, 2, 3])
    print(isinstance(it, Iterator))     # True

    # Callable: has __call__
    print(isinstance(print, Callable))  # True
    print(isinstance(42, Callable))     # False

    # Custom Iterable
    class NumberRange:
        def __init__(self, start: int, stop: int) -> None:
            self.start = start
            self.stop = stop

        def __iter__(self) -> Iterator[int]:
            return iter(range(self.start, self.stop))

        def __len__(self) -> int:
            return max(0, self.stop - self.start)

    nr = NumberRange(1, 5)
    print(isinstance(nr, Iterable))     # True
    print(isinstance(nr, Sequence))     # False (no __getitem__)
    print(list(nr))                     # [1, 2, 3, 4]


# ---------------------------------------------------------------------------
# 6. ABCs vs Protocols — When to Use Which
# ---------------------------------------------------------------------------
#
# Use ABC when:
#   - You want to provide default implementations
#   - Subclasses must formally declare 'class Foo(MyABC):'
#   - You're building a framework where the hierarchy matters
#   - isinstance() checks are central to your design
#
# Use Protocol when:
#   - You don't control the classes being checked
#   - You want structural ("duck-type") matching for static analysis
#   - You're checking third-party or built-in types
#   - You want zero overhead (no virtual dispatch, just static checks)
#
# Rule of thumb: Protocols for public API type hints, ABCs for framework
# base classes.

if __name__ == "__main__":
    print("=== Duck Typing ===")
    demo_duck_typing()

    print("\n=== ABC ===")
    demo_abc()

    print("\n=== Protocol ===")
    demo_protocol()

    print("\n=== __subclasshook__ ===")
    demo_subclasshook()

    print("\n=== collections.abc ===")
    demo_collections_abc()
