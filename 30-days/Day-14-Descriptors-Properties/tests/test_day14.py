"""Tests for Day 14 — Descriptors"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)
import pytest
from solutions import TypedAttribute, Clamped, LazyProperty, Person, Clipped, ExpensiveObject


class TestTypedAttribute:
    def test_correct_type(self) -> None:
        p = Person("Alice", 30)
        assert p.name == "Alice"
        assert p.age == 30

    def test_wrong_type_raises(self) -> None:
        p = Person("Alice", 30)
        with pytest.raises(TypeError):
            p.age = "thirty"  # type: ignore[assignment]

    def test_wrong_type_str(self) -> None:
        p = Person("Alice", 30)
        with pytest.raises(TypeError):
            p.name = 42  # type: ignore[assignment]

    def test_descriptor_name(self) -> None:
        # Descriptor should know its attribute name
        assert Person.name._name == "name"
        assert Person.age._name == "age"


class TestClamped:
    def test_value_within_range(self) -> None:
        c = Clipped(50.0, 0.5)
        assert c.value == 50.0
        assert c.volume == 0.5

    def test_clamp_above_max(self) -> None:
        c = Clipped(200.0, 2.0)
        assert c.value == 100.0
        assert c.volume == 1.0

    def test_clamp_below_min(self) -> None:
        c = Clipped(-50.0, -1.0)
        assert c.value == 0.0
        assert c.volume == 0.0


class TestLazyProperty:
    def test_computed_once(self) -> None:
        obj = ExpensiveObject(10)
        _ = obj.computed
        _ = obj.computed
        assert obj._computed == 1  # only computed once

    def test_correct_value(self) -> None:
        obj = ExpensiveObject(5)
        assert obj.computed == sum(range(5))  # 0+1+2+3+4=10

    def test_cached_in_instance_dict(self) -> None:
        obj = ExpensiveObject(5)
        _ = obj.computed
        assert "computed" in obj.__dict__
