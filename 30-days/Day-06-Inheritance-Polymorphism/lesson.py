"""
Day 06 — Inheritance and Polymorphism
=======================================

Topics:
  - Single inheritance: class Child(Parent):
  - super() and MRO (C3 linearization)
  - Method overriding
  - isinstance(), issubclass()
  - Multiple inheritance: diamond problem solved by MRO
  - Mixin pattern
  - Python vs C++ virtual dispatch (everything is virtual in Python)
"""
from __future__ import annotations

import math


# ---------------------------------------------------------------------------
# 1. Basic Inheritance
# ---------------------------------------------------------------------------
# C++ virtual dispatch: opt-in with 'virtual' keyword.
# Python: ALL method calls use dynamic dispatch by default.
# There is no non-virtual method in Python (unlike C++).

class Shape:
    """Abstract base — all shapes have area and perimeter."""

    def area(self) -> float:
        """Return area. Subclasses should override."""
        raise NotImplementedError(f"{type(self).__name__} must implement area()")

    def perimeter(self) -> float:
        """Return perimeter. Subclasses should override."""
        raise NotImplementedError(f"{type(self).__name__} must implement perimeter()")

    def describe(self) -> str:
        """Template method using polymorphism."""
        return (
            f"{type(self).__name__}: area={self.area():.4f}, "
            f"perimeter={self.perimeter():.4f}"
        )

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"


class Circle(Shape):
    """Circle — inherits from Shape."""

    def __init__(self, radius: float) -> None:
        if radius < 0:
            raise ValueError(f"radius must be non-negative, got {radius}")
        self._radius = radius

    def area(self) -> float:
        return math.pi * self._radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self._radius

    def __repr__(self) -> str:
        return f"Circle(radius={self._radius!r})"


class Rectangle(Shape):
    """Rectangle — inherits from Shape."""

    def __init__(self, width: float, height: float) -> None:
        self._width = width
        self._height = height

    def area(self) -> float:
        return self._width * self._height

    def perimeter(self) -> float:
        return 2 * (self._width + self._height)

    def __repr__(self) -> str:
        return f"Rectangle({self._width!r}, {self._height!r})"


class Square(Rectangle):
    """Square — inherits from Rectangle.

    Note: In C++, Square(Rectangle) violates LSP (Liskov Substitution Principle)
    if you allow setting width and height independently. Here we model it correctly:
    Square only accepts one dimension, ensuring the invariant.
    """

    def __init__(self, side: float) -> None:
        super().__init__(side, side)   # delegate to Rectangle.__init__

    def __repr__(self) -> str:
        return f"Square(side={self._width!r})"


# ---------------------------------------------------------------------------
# 2. super() and Method Resolution Order (MRO)
# ---------------------------------------------------------------------------
# super() calls the NEXT method in the MRO chain, not necessarily the direct parent.
# Python uses C3 linearisation to resolve the MRO.

def demo_mro() -> None:
    """Show MRO for various class hierarchies."""
    print("Circle MRO:", [c.__name__ for c in Circle.__mro__])
    # ['Circle', 'Shape', 'object']

    print("Square MRO:", [c.__name__ for c in Square.__mro__])
    # ['Square', 'Rectangle', 'Shape', 'object']


# ---------------------------------------------------------------------------
# 3. Polymorphism in Action
# ---------------------------------------------------------------------------

def total_area(shapes: list[Shape]) -> float:
    """Sum areas of any list of shapes — polymorphic dispatch."""
    return sum(s.area() for s in shapes)


def demo_polymorphism() -> None:
    shapes: list[Shape] = [
        Circle(5.0),
        Rectangle(4.0, 6.0),
        Square(3.0),
        Circle(1.0),
    ]

    for shape in shapes:
        print(shape.describe())    # dispatches to correct subclass

    print(f"\nTotal area: {total_area(shapes):.4f}")

    # isinstance() — preferred for polymorphic type checks
    for s in shapes:
        print(f"{s!r} is Shape? {isinstance(s, Shape)}")
        print(f"{s!r} is Rectangle? {isinstance(s, Rectangle)}")


# ---------------------------------------------------------------------------
# 4. Multiple Inheritance and the Diamond Problem
# ---------------------------------------------------------------------------
# C++ has the diamond problem with shared base class state.
# Python's C3 MRO solves it by ensuring each class in the hierarchy
# appears exactly once in the linearisation.

class Flyable:
    """Mixin: provides flying behaviour."""

    def fly(self) -> str:
        return f"{type(self).__name__} is flying"

    def describe_movement(self) -> str:
        return f"moves by flying"


class Swimmable:
    """Mixin: provides swimming behaviour."""

    def swim(self) -> str:
        return f"{type(self).__name__} is swimming"

    def describe_movement(self) -> str:
        return f"moves by swimming"


class Animal:
    """Base class for animals."""

    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        return "..."

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name!r})"


class Duck(Animal, Flyable, Swimmable):
    """Duck can fly AND swim — multiple inheritance."""

    def __init__(self, name: str) -> None:
        super().__init__(name)   # calls Animal.__init__ via MRO

    def speak(self) -> str:
        return "Quack!"

    def describe_movement(self) -> str:
        # super() calls the next in MRO — Flyable.describe_movement
        base = super().describe_movement()
        return f"moves by flying and swimming (from {base})"


def demo_multiple_inheritance() -> None:
    duck = Duck("Donald")
    print(duck.speak())
    print(duck.fly())
    print(duck.swim())
    print(duck.describe_movement())

    # MRO shows resolution order
    print("Duck MRO:", [c.__name__ for c in Duck.__mro__])
    # ['Duck', 'Animal', 'Flyable', 'Swimmable', 'object']

    # Diamond: both Flyable and Swimmable define describe_movement
    # MRO ensures Flyable's version is called (first in MRO after Duck)


# ---------------------------------------------------------------------------
# 5. Mixin Pattern — Composition via Inheritance
# ---------------------------------------------------------------------------
# Mixins add behaviour without IS-A relationship.
# Use when you want to share code but not model a true hierarchy.

class JsonMixin:
    """Mixin: adds JSON serialisation to any class."""

    def to_json(self) -> str:
        import json
        # Serialize public attributes
        data = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return json.dumps(data, default=str)


class LogMixin:
    """Mixin: adds logging capability to any class."""

    def log(self, message: str, level: str = "INFO") -> None:
        print(f"[{level}] {type(self).__name__}: {message}")


class Product(JsonMixin, LogMixin):
    """Product with JSON and logging mixins."""

    def __init__(self, name: str, price: float, sku: str) -> None:
        self.name = name
        self.price = price
        self.sku = sku

    def apply_discount(self, percent: float) -> None:
        self.log(f"Applying {percent}% discount")
        self.price *= (1 - percent / 100)


def demo_mixins() -> None:
    p = Product("Widget", 29.99, "WGT-001")
    print(p.to_json())
    p.apply_discount(10.0)
    p.log(f"Price after discount: {p.price:.2f}")


# ---------------------------------------------------------------------------
# 6. super() in Multiple Inheritance — Cooperative Multiple Inheritance
# ---------------------------------------------------------------------------

class Logger:
    """Cooperative mixin: uses super() to pass along the chain."""

    def process(self, data: str) -> str:
        print(f"[Logger] processing: {data}")
        return super().process(data)  # type: ignore[return-value]


class Validator:
    """Cooperative mixin: validates before processing."""

    def process(self, data: str) -> str:
        if not data:
            raise ValueError("data cannot be empty")
        print(f"[Validator] validated: {data!r}")
        return super().process(data)  # type: ignore[return-value]


class Processor:
    """Base processor."""

    def process(self, data: str) -> str:
        return data.upper()


class Pipeline(Logger, Validator, Processor):
    """Combines Logger, Validator, and Processor via cooperative MI."""
    pass
    # MRO: Pipeline → Logger → Validator → Processor → object
    # calling pipeline.process("hello") chains:
    #   Logger.process → Validator.process → Processor.process


if __name__ == "__main__":
    print("=== Shape Hierarchy ===")
    c = Circle(5.0)
    r = Rectangle(4.0, 6.0)
    s = Square(3.0)
    print(c.describe())
    print(r.describe())
    print(s.describe())

    print("\n=== MRO ===")
    demo_mro()

    print("\n=== Polymorphism ===")
    demo_polymorphism()

    print("\n=== Multiple Inheritance ===")
    demo_multiple_inheritance()

    print("\n=== Mixins ===")
    demo_mixins()

    print("\n=== Cooperative super() ===")
    pipeline = Pipeline()
    result = pipeline.process("hello world")
    print(f"result: {result}")
