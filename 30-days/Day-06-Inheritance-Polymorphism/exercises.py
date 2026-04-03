"""
Day 06 — Exercises: Inheritance and Polymorphism
"""
from __future__ import annotations

import math


# Exercise 1: Shape hierarchy with Triangle
class Shape:
    def area(self) -> float: raise NotImplementedError
    def perimeter(self) -> float: raise NotImplementedError

class Circle(Shape):
    def __init__(self, radius: float) -> None: self.radius = radius
    def area(self) -> float:
        return math.pi * self.radius ** 2
    def perimeter(self) -> float:
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width; self.height = height
    def area(self) -> float:
        return self.width * self.height
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float) -> None:
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Invalid triangle sides")
        self.a = a; self.b = b; self.c = c
    def area(self) -> float:
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
    def perimeter(self) -> float:
        return self.a + self.b + self.c


# Exercise 2: Animal sounds
class Animal:
    def __init__(self, name: str) -> None: self.name = name
    def speak(self) -> str: raise NotImplementedError

class Dog(Animal):
    def speak(self) -> str: return "Woof!"

class Cat(Animal):
    def speak(self) -> str: return "Meow!"

class Bird(Animal):
    def speak(self) -> str: return "Tweet!"

def make_noise(animals: list[Animal]) -> list[str]:
    return [f"{a.name}: {a.speak()}" for a in animals]


# Exercise 3: Mixin combination
class SerializableMixin:
    def to_dict(self) -> dict[str, object]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

class ComparableMixin:
    def _compare_key(self) -> object: raise NotImplementedError
    def __lt__(self, other: "ComparableMixin") -> bool:
        return self._compare_key() < other._compare_key()  # type: ignore[operator]
    def __le__(self, other: "ComparableMixin") -> bool:
        return self._compare_key() <= other._compare_key()  # type: ignore[operator]
    def __gt__(self, other: "ComparableMixin") -> bool:
        return self._compare_key() > other._compare_key()  # type: ignore[operator]

class Product(SerializableMixin, ComparableMixin):
    def __init__(self, name: str, price: float) -> None:
        self.name = name; self.price = price
    def _compare_key(self) -> float: return self.price


if __name__ == "__main__":
    print(Circle(5.0).area())
