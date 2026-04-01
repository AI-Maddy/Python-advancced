"""pytest tests for protocol idiom."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from protocol_idiom import (
    Circle,
    Comparable,
    Drawable,
    Serializable,
    Square,
    Temperature,
    find_min,
    render_all,
    save_all,
)


class TestDrawableProtocol:
    def test_circle_is_drawable(self) -> None:
        assert isinstance(Circle(5), Drawable)

    def test_square_is_drawable(self) -> None:
        assert isinstance(Square(3), Drawable)

    def test_int_is_not_drawable(self) -> None:
        assert not isinstance(42, Drawable)

    def test_protocol_without_inheritance(self) -> None:
        class Triangle:
            def draw(self) -> str:
                return "△"

        t = Triangle()
        assert isinstance(t, Drawable)

    def test_render_all(self) -> None:
        shapes: list[Drawable] = [Circle(1), Square(2)]
        results = render_all(shapes)
        assert len(results) == 2
        assert all(isinstance(r, str) for r in results)


class TestSerializableProtocol:
    def test_temperature_is_serializable(self) -> None:
        assert isinstance(Temperature(25.0), Serializable)

    def test_to_dict(self) -> None:
        d = Temperature(100.0).to_dict()
        assert d == {"celsius": 100.0}

    def test_from_dict_round_trip(self) -> None:
        t = Temperature(37.5)
        restored = Temperature.from_dict(t.to_dict())
        assert restored.celsius == 37.5

    def test_save_all(self) -> None:
        items: list[Serializable] = [Temperature(0), Temperature(100)]
        dicts = save_all(items)
        assert dicts == [{"celsius": 0}, {"celsius": 100}]


class TestComparableProtocol:
    def test_temperature_is_comparable(self) -> None:
        assert isinstance(Temperature(0), Comparable)

    def test_find_min(self) -> None:
        temps: list[Comparable] = [  # type: ignore[list-item]
            Temperature(50), Temperature(-10), Temperature(100)
        ]
        result = find_min(temps)
        assert isinstance(result, Temperature)
        assert result.celsius == -10  # type: ignore[attr-defined]

    def test_equality(self) -> None:
        assert Temperature(25) == Temperature(25)
        assert Temperature(25) != Temperature(30)

    def test_less_than(self) -> None:
        assert Temperature(10) < Temperature(20)


class TestConformingWithoutInheritance:
    def test_class_satisfies_protocol_without_explicit_inheritance(self) -> None:
        class MyShape:
            def draw(self) -> str:
                return "my shape"

        # No inheritance from Drawable at all
        shape = MyShape()
        assert isinstance(shape, Drawable)
        assert shape.draw() == "my shape"
