"""
Tests for Day 06 — Inheritance and Polymorphism
"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)

import math
import pytest

from solutions import (
    Animal, Bird, Cat, Circle, Dog, Product,
    Rectangle, SerializableMixin, Shape, Triangle, make_noise,
)


class TestShapeHierarchy:
    def test_circle_area(self) -> None:
        assert Circle(5.0).area() == pytest.approx(math.pi * 25)

    def test_circle_perimeter(self) -> None:
        assert Circle(3.0).perimeter() == pytest.approx(2 * math.pi * 3)

    def test_rectangle_area(self) -> None:
        assert Rectangle(4.0, 6.0).area() == pytest.approx(24.0)

    def test_rectangle_perimeter(self) -> None:
        assert Rectangle(4.0, 6.0).perimeter() == pytest.approx(20.0)

    def test_triangle_area_345(self) -> None:
        # 3-4-5 right triangle: area = 6
        assert Triangle(3.0, 4.0, 5.0).area() == pytest.approx(6.0)

    def test_triangle_perimeter(self) -> None:
        assert Triangle(3.0, 4.0, 5.0).perimeter() == pytest.approx(12.0)

    def test_invalid_triangle(self) -> None:
        with pytest.raises((ValueError, Exception)):
            Triangle(1.0, 1.0, 10.0)   # 1+1 <= 10

    def test_isinstance_hierarchy(self) -> None:
        c = Circle(1.0)
        assert isinstance(c, Circle)
        assert isinstance(c, Shape)

    def test_polymorphic_total(self) -> None:
        shapes: list[Shape] = [Circle(1.0), Rectangle(2.0, 3.0)]
        total = sum(s.area() for s in shapes)
        expected = math.pi + 6.0
        assert total == pytest.approx(expected)


class TestAnimalSounds:
    def test_dog_speaks(self) -> None:
        assert Dog("Rex").speak() == "Woof!"

    def test_cat_speaks(self) -> None:
        assert Cat("Whiskers").speak() == "Meow!"

    def test_bird_speaks(self) -> None:
        assert Bird("Tweety").speak() == "Tweet!"

    def test_make_noise(self) -> None:
        animals: list[Animal] = [Dog("Rex"), Cat("Kitty")]
        result = make_noise(animals)
        assert result == ["Rex: Woof!", "Kitty: Meow!"]

    def test_polymorphic_speak(self) -> None:
        animals: list[Animal] = [Dog("a"), Cat("b"), Bird("c")]
        sounds = [a.speak() for a in animals]
        assert sounds == ["Woof!", "Meow!", "Tweet!"]


class TestMixins:
    def test_serializable(self) -> None:
        p = Product("Widget", 9.99)
        d = p.to_dict()
        assert d["name"] == "Widget"
        assert d["price"] == 9.99

    def test_comparable_lt(self) -> None:
        cheap = Product("A", 5.0)
        expensive = Product("B", 20.0)
        assert cheap < expensive

    def test_comparable_sort(self) -> None:
        products = [
            Product("C", 30.0),
            Product("A", 10.0),
            Product("B", 20.0),
        ]
        sorted_products = sorted(products)
        prices = [p.price for p in sorted_products]
        assert prices == [10.0, 20.0, 30.0]
