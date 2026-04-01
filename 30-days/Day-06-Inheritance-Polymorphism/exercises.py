"""
Day 06 — Exercises: Inheritance and Polymorphism
"""
from __future__ import annotations


# Exercise 1: Shape hierarchy with Triangle
class Shape:
    def area(self) -> float: raise NotImplementedError
    def perimeter(self) -> float: raise NotImplementedError

class Circle(Shape):
    def __init__(self, radius: float) -> None: self.radius = radius
    # TODO: area, perimeter

class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width; self.height = height
    # TODO: area, perimeter

class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float) -> None:
        self.a = a; self.b = b; self.c = c
    # TODO: area (Heron's formula), perimeter, validation


# Exercise 2: Animal sounds
class Animal:
    def __init__(self, name: str) -> None: self.name = name
    def speak(self) -> str: raise NotImplementedError

class Dog(Animal):
    def speak(self) -> str: pass  # TODO: "Woof!"

class Cat(Animal):
    def speak(self) -> str: pass  # TODO: "Meow!"

class Bird(Animal):
    def speak(self) -> str: pass  # TODO: "Tweet!"

def make_noise(animals: list[Animal]) -> list[str]:
    # TODO: return ["name: sound", ...]
    pass


# Exercise 3: Mixin combination
class SerializableMixin:
    def to_dict(self) -> dict[str, object]:
        # TODO: return public __dict__ items
        pass

class ComparableMixin:
    def _compare_key(self) -> object: raise NotImplementedError
    def __lt__(self, other: "ComparableMixin") -> bool: pass  # TODO
    def __le__(self, other: "ComparableMixin") -> bool: pass  # TODO
    def __gt__(self, other: "ComparableMixin") -> bool: pass  # TODO

class Product(SerializableMixin, ComparableMixin):
    def __init__(self, name: str, price: float) -> None:
        self.name = name; self.price = price
    def _compare_key(self) -> float: return self.price


if __name__ == "__main__":
    print(Circle(5.0).area())
