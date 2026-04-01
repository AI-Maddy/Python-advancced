"""pytest tests for descriptor idiom."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from descriptor import CachedProperty, Clamped, Circle, Person, Sensor, TypeChecked, Validated


class TestValidated:
    def test_valid_value_accepted(self) -> None:
        p = Person("Alice", 25)
        assert p.age == 25

    def test_invalid_value_raises_value_error(self) -> None:
        p = Person("Alice", 25)
        with pytest.raises(ValueError, match="age"):
            p.age = -1

    def test_valid_zero_age(self) -> None:
        p = Person("Baby", 0)
        assert p.age == 0

    def test_class_access_returns_descriptor(self) -> None:
        desc = Person.__dict__["age"]
        assert isinstance(desc, Validated)


class TestTypeChecked:
    def test_correct_type_accepted(self) -> None:
        p = Person("Alice", 30)
        p.name = "Bob"
        assert p.name == "Bob"

    def test_wrong_type_raises_type_error(self) -> None:
        p = Person("Alice", 30)
        with pytest.raises(TypeError, match="name"):
            p.name = 123  # type: ignore[assignment]

    def test_subclass_accepted(self) -> None:
        """Subclasses of str should still pass isinstance check."""
        class MyStr(str):
            pass
        p = Person("Alice", 30)
        p.name = MyStr("Carol")

    def test_class_access_returns_descriptor(self) -> None:
        desc = Person.__dict__["name"]
        assert isinstance(desc, TypeChecked)


class TestClamped:
    def test_value_within_range_unchanged(self) -> None:
        s = Sensor(25.0, 50.0)
        assert s.temperature == 25.0

    def test_value_above_max_clamped(self) -> None:
        s = Sensor(200.0, 50.0)
        assert s.temperature == 125.0

    def test_value_below_min_clamped(self) -> None:
        s = Sensor(-100.0, 50.0)
        assert s.temperature == -40.0

    def test_humidity_clamped_to_zero(self) -> None:
        s = Sensor(20.0, -10.0)
        assert s.humidity == 0.0

    def test_delete_resets_to_min(self) -> None:
        s = Sensor(20.0, 50.0)
        del s.temperature
        assert s.temperature == -40.0  # default returns min


class TestCachedProperty:
    def test_computed_once(self) -> None:
        c = Circle(5.0)
        _ = c.area
        _ = c.area
        assert c._compute_count == 1

    def test_correct_value(self) -> None:
        import math
        c = Circle(3.0)
        assert c.area == pytest.approx(math.pi * 9)

    def test_cache_stored_in_instance_dict(self) -> None:
        c = Circle(4.0)
        _ = c.area
        assert "area" in c.__dict__

    def test_different_instances_independent(self) -> None:
        c1 = Circle(1.0)
        c2 = Circle(2.0)
        assert c1.area != c2.area
