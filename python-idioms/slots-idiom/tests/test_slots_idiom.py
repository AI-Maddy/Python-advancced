"""pytest tests for slots idiom."""
from __future__ import annotations

import sys
import weakref
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from slots_idiom import (
    ColoredPoint,
    ColoredPointBad,
    PointWithDict,
    PointWithSlots,
    WeakRefPoint,
)


class TestPointWithDict:
    def test_has_dict(self) -> None:
        p = PointWithDict(1.0, 2.0)
        assert hasattr(p, "__dict__")

    def test_dynamic_attribute_allowed(self) -> None:
        p = PointWithDict(1.0, 2.0)
        p.z = 3.0  # type: ignore[attr-defined]
        assert p.z == 3.0  # type: ignore[attr-defined]

    def test_attribute_access(self) -> None:
        p = PointWithDict(3.0, 4.0)
        assert p.x == 3.0
        assert p.y == 4.0


class TestPointWithSlots:
    def test_no_dict(self) -> None:
        p = PointWithSlots(1.0, 2.0)
        assert not hasattr(p, "__dict__")

    def test_attribute_access(self) -> None:
        p = PointWithSlots(3.0, 4.0)
        assert p.x == 3.0
        assert p.y == 4.0

    def test_dynamic_attribute_blocked(self) -> None:
        p = PointWithSlots(1.0, 2.0)
        with pytest.raises(AttributeError):
            p.z = 3.0  # type: ignore[attr-defined]

    def test_slots_smaller_than_dict(self) -> None:
        """Slots instance should be smaller or equal in getsizeof."""
        pd = PointWithDict(1.0, 2.0)
        ps = PointWithSlots(1.0, 2.0)
        # getsizeof of slots instance is typically smaller
        assert sys.getsizeof(ps) <= sys.getsizeof(pd)

    def test_has_slots_attribute(self) -> None:
        assert hasattr(PointWithSlots, "__slots__")
        assert "x" in PointWithSlots.__slots__
        assert "y" in PointWithSlots.__slots__


class TestWeakRefPoint:
    def test_weakref_works(self) -> None:
        p = WeakRefPoint(1.0, 2.0)
        ref = weakref.ref(p)
        assert ref() is p

    def test_weakref_clears_on_del(self) -> None:
        p = WeakRefPoint(1.0, 2.0)
        ref = weakref.ref(p)
        del p
        assert ref() is None


class TestColoredPoint:
    def test_no_dict(self) -> None:
        cp = ColoredPoint(1.0, 2.0, "red")
        assert not hasattr(cp, "__dict__")

    def test_all_attributes_accessible(self) -> None:
        cp = ColoredPoint(5.0, 6.0, "blue")
        assert cp.x == 5.0
        assert cp.y == 6.0
        assert cp.color == "blue"

    def test_inherits_parent_slots(self) -> None:
        cp = ColoredPoint(1.0, 2.0, "green")
        assert hasattr(cp, "x")
        assert hasattr(cp, "y")


class TestColoredPointBad:
    def test_has_dict_due_to_missing_slots(self) -> None:
        cpb = ColoredPointBad(1.0, 2.0, "red")
        # Subclass without __slots__ gets __dict__ back
        assert hasattr(cpb, "__dict__")

    def test_dynamic_attribute_allowed(self) -> None:
        cpb = ColoredPointBad(1.0, 2.0, "red")
        cpb.extra = "dynamic"  # type: ignore[attr-defined]
        assert cpb.extra == "dynamic"  # type: ignore[attr-defined]
