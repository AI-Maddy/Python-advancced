"""pytest tests for abstract base class idiom."""
from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from abstract_base_class import (
    Circle,
    Dog,
    Drawable,
    ExternalShape,
    FrozenList,
    RangeIterator,
    Rectangle,
    Shape,
)


class TestAbstractShape:
    def test_instantiation_blocked(self) -> None:
        with pytest.raises(TypeError):
            Shape()  # type: ignore[abstract]

    def test_circle_is_shape(self) -> None:
        c = Circle(5.0)
        assert isinstance(c, Shape)

    def test_rectangle_is_shape(self) -> None:
        r = Rectangle(4.0, 3.0)
        assert isinstance(r, Shape)

    def test_circle_area(self) -> None:
        import math
        c = Circle(1.0)
        assert c.area() == pytest.approx(math.pi)

    def test_rectangle_area(self) -> None:
        r = Rectangle(4.0, 5.0)
        assert r.area() == pytest.approx(20.0)

    def test_rectangle_perimeter(self) -> None:
        r = Rectangle(3.0, 4.0)
        assert r.perimeter() == pytest.approx(14.0)

    def test_from_string_circle(self) -> None:
        c = Circle.from_string("r=3.0")
        assert isinstance(c, Circle)

    def test_name_property(self) -> None:
        assert Circle(1).name == "Circle"
        assert Rectangle(1, 1).name == "Rectangle"

    def test_missing_abstract_raises(self) -> None:
        with pytest.raises(TypeError):
            class BadShape(Shape):  # type: ignore[abstract]
                pass
            BadShape()


class TestABCMeta:
    def test_dog_speaks(self) -> None:
        d = Dog()
        assert d.speak() == "Woof!"


class TestSubclassHook:
    def test_external_shape_is_virtual_subclass(self) -> None:
        ext = ExternalShape()
        assert isinstance(ext, Drawable)

    def test_object_without_draw_is_not_drawable(self) -> None:
        class NoDraw:
            pass
        assert not isinstance(NoDraw(), Drawable)


class TestFrozenList:
    def test_is_sequence(self) -> None:
        fl = FrozenList([1, 2, 3])
        assert isinstance(fl, Sequence)

    def test_len(self) -> None:
        fl = FrozenList([1, 2, 3])
        assert len(fl) == 3

    def test_getitem(self) -> None:
        fl = FrozenList([10, 20, 30])
        assert fl[1] == 20

    def test_contains(self) -> None:
        fl = FrozenList([1, 2, 3])
        assert 2 in fl

    def test_count(self) -> None:
        fl = FrozenList([1, 2, 2, 3])
        assert fl.count(2) == 2

    def test_index(self) -> None:
        fl = FrozenList([10, 20, 30])
        assert fl.index(20) == 1


class TestRangeIterator:
    def test_yields_correct_values(self) -> None:
        assert list(RangeIterator(0, 5)) == [0, 1, 2, 3, 4]

    def test_empty_range(self) -> None:
        assert list(RangeIterator(5, 5)) == []

    def test_stop_iteration(self) -> None:
        it = RangeIterator(0, 2)
        next(it)
        next(it)
        with pytest.raises(StopIteration):
            next(it)

    def test_is_iterable(self) -> None:
        from collections.abc import Iterable
        it = RangeIterator(0, 3)
        assert isinstance(it, Iterable)
