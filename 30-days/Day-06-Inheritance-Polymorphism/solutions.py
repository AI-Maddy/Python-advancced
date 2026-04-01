"""
Day 06 — Solutions
"""
from __future__ import annotations

import math


# ---------------------------------------------------------------------------
# Exercise 1: Shape hierarchy
# ---------------------------------------------------------------------------

class Shape:
    def area(self) -> float:
        raise NotImplementedError

    def perimeter(self) -> float:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius

    def __repr__(self) -> str:
        return f"Circle(radius={self.radius})"


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

    def __repr__(self) -> str:
        return f"Rectangle({self.width}, {self.height})"


class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float) -> None:
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Invalid triangle sides")
        self.a = a
        self.b = b
        self.c = c

    def area(self) -> float:
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self) -> float:
        return self.a + self.b + self.c


# ---------------------------------------------------------------------------
# Exercise 2: Animal sounds with polymorphism
# ---------------------------------------------------------------------------

class Animal:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name!r})"


class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"


class Bird(Animal):
    def speak(self) -> str:
        return "Tweet!"


def make_noise(animals: list[Animal]) -> list[str]:
    return [f"{a.name}: {a.speak()}" for a in animals]


# ---------------------------------------------------------------------------
# Exercise 3: Mixin combination
# ---------------------------------------------------------------------------

class SerializableMixin:
    """Adds to_dict() and from_dict() capabilities."""

    def to_dict(self) -> dict[str, object]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}


class ComparableMixin:
    """Adds __lt__, __le__, etc. based on a _compare_key property."""

    def _compare_key(self) -> object:
        raise NotImplementedError

    def __lt__(self, other: "ComparableMixin") -> bool:
        return self._compare_key() < other._compare_key()  # type: ignore[operator]

    def __le__(self, other: "ComparableMixin") -> bool:
        return self._compare_key() <= other._compare_key()  # type: ignore[operator]

    def __gt__(self, other: "ComparableMixin") -> bool:
        return self._compare_key() > other._compare_key()  # type: ignore[operator]


class Product(SerializableMixin, ComparableMixin):
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def _compare_key(self) -> float:
        return self.price

    def __repr__(self) -> str:
        return f"Product({self.name!r}, {self.price})"


if __name__ == "__main__":
    shapes: list[Shape] = [Circle(3.0), Rectangle(2.0, 5.0), Triangle(3.0, 4.0, 5.0)]
    for s in shapes:
        print(f"{s}: area={s.area():.3f}, perimeter={s.perimeter():.3f}")

    animals: list[Animal] = [Dog("Rex"), Cat("Whiskers"), Bird("Tweety")]
    for line in make_noise(animals):
        print(line)

    products = [Product("Apple", 1.2), Product("Banana", 0.5), Product("Cherry", 2.0)]
    print(sorted(products))
    print(products[0].to_dict())
