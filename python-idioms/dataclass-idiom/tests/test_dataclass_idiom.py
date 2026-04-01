"""pytest tests for dataclass idiom."""
from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from dataclass_idiom import Coordinate, Point, RGB, Team, Vector3


class TestPoint:
    def test_equality(self) -> None:
        assert Point(1.0, 2.0) == Point(1.0, 2.0)

    def test_not_equal(self) -> None:
        assert Point(1.0, 2.0) != Point(1.0, 3.0)

    def test_distance(self) -> None:
        assert Point(0.0, 0.0).distance_to(Point(3.0, 4.0)) == pytest.approx(5.0)

    def test_mutable(self) -> None:
        p = Point(1.0, 2.0)
        p.x = 99.0
        assert p.x == 99.0


class TestRGB:
    def test_valid_creation(self) -> None:
        c = RGB(255, 128, 0)
        assert c.r == 255

    def test_to_hex(self) -> None:
        assert RGB(255, 0, 0).to_hex() == "#ff0000"
        assert RGB(0, 255, 0).to_hex() == "#00ff00"

    def test_invalid_channel_raises(self) -> None:
        with pytest.raises(ValueError):
            RGB(256, 0, 0)

    def test_negative_channel_raises(self) -> None:
        with pytest.raises(ValueError):
            RGB(-1, 0, 0)

    def test_frozen_mutation_raises(self) -> None:
        c = RGB(100, 100, 100)
        with pytest.raises(dataclasses.FrozenInstanceError):
            c.r = 0  # type: ignore[misc]

    def test_hashable(self) -> None:
        s: set[RGB] = {RGB(255, 0, 0), RGB(255, 0, 0), RGB(0, 0, 255)}
        assert len(s) == 2

    def test_asdict(self) -> None:
        d = dataclasses.asdict(RGB(10, 20, 30))
        assert d == {"r": 10, "g": 20, "b": 30}

    def test_replace(self) -> None:
        red = RGB(255, 0, 0)
        pink = dataclasses.replace(red, b=128)
        assert pink.b == 128
        assert red.b == 0   # original unaffected


class TestVector3:
    def test_magnitude(self) -> None:
        import math
        v = Vector3(1.0, 0.0, 0.0)
        assert v.magnitude() == pytest.approx(1.0)

    def test_no_dict_with_slots(self) -> None:
        v = Vector3(1.0, 2.0, 3.0)
        assert not hasattr(v, "__dict__")


class TestTeam:
    def test_basic_creation(self) -> None:
        t = Team("Alpha", ["Alice"])
        assert t.name == "Alpha"
        assert "Alice" in t.members

    def test_default_empty_members(self) -> None:
        t = Team("Beta")
        assert t.members == []

    def test_add_member(self) -> None:
        t = Team("Gamma")
        t.add_member("Dave")
        assert "Dave" in t.members

    def test_max_size_exceeded_raises(self) -> None:
        with pytest.raises(ValueError):
            Team("Small", ["a", "b", "c"], max_size=2)

    def test_team_full_raises(self) -> None:
        t = Team("Tiny", max_size=1)
        t.add_member("Alice")
        with pytest.raises(ValueError):
            t.add_member("Bob")

    def test_default_factory_independent(self) -> None:
        t1 = Team("T1")
        t2 = Team("T2")
        t1.members.append("x")
        assert t2.members == []


class TestCoordinate:
    def test_is_namedtuple(self) -> None:
        c = Coordinate(0.0, 0.0)
        assert isinstance(c, tuple)

    def test_indexing(self) -> None:
        c = Coordinate(10.0, 20.0)
        assert c[0] == 10.0
        assert c[1] == 20.0

    def test_label(self) -> None:
        c = Coordinate(51.5074, -0.1278)
        label = c.label()
        assert "N" in label
        assert "W" in label
