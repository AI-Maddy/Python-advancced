"""
Tests for Day 04 — Dataclasses, Slots, and Constructors
"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)

import pytest

from solutions import Card, DateRange, ImmutableConfig, Point3D


class TestPoint3D:
    def test_repr(self) -> None:
        p = Point3D(1.0, 2.0, 3.0)
        assert "1.0" in repr(p)

    def test_equality(self) -> None:
        assert Point3D(1.0, 2.0, 3.0) == Point3D(1.0, 2.0, 3.0)
        assert Point3D(1.0, 2.0, 3.0) != Point3D(1.0, 2.0, 4.0)

    def test_distance(self) -> None:
        p1 = Point3D(0.0, 0.0, 0.0)
        p2 = Point3D(1.0, 2.0, 2.0)
        assert p1.distance_to(p2) == pytest.approx(3.0)

    def test_midpoint(self) -> None:
        p1 = Point3D(0.0, 0.0, 0.0)
        p2 = Point3D(2.0, 4.0, 6.0)
        mid = p1.midpoint(p2)
        assert mid == Point3D(1.0, 2.0, 3.0)

    def test_origin(self) -> None:
        o = Point3D.origin()
        assert o == Point3D(0.0, 0.0, 0.0)


class TestImmutableConfig:
    def test_creation(self) -> None:
        c = ImmutableConfig(host="localhost", port=8080)
        assert c.host == "localhost"
        assert c.port == 8080

    def test_frozen(self) -> None:
        c = ImmutableConfig(host="localhost", port=8080)
        with pytest.raises(Exception):  # FrozenInstanceError
            c.host = "other"  # type: ignore[misc]

    def test_hashable(self) -> None:
        c1 = ImmutableConfig("localhost", 8080)
        c2 = ImmutableConfig("localhost", 8080)
        s = {c1, c2}
        assert len(s) == 1  # same value → same hash

    def test_development_factory(self) -> None:
        dev = ImmutableConfig.development()
        assert dev.debug is True
        assert dev.port == 8000

    def test_production_factory(self) -> None:
        prod = ImmutableConfig.production("example.com")
        assert prod.debug is False
        assert prod.host == "example.com"

    def test_invalid_port(self) -> None:
        with pytest.raises(ValueError):
            ImmutableConfig("localhost", 0)
        with pytest.raises(ValueError):
            ImmutableConfig("localhost", 99999)


class TestDateRange:
    def test_basic(self) -> None:
        dr = DateRange("2024-01-01", "2024-12-31")
        assert dr.start == "2024-01-01"

    def test_invalid_range(self) -> None:
        with pytest.raises(ValueError):
            DateRange("2024-06-01", "2024-01-01")

    def test_single_day(self) -> None:
        dr = DateRange.single_day("2024-03-15")
        assert dr.start == dr.end == "2024-03-15"
        assert dr.days == 1

    def test_year(self) -> None:
        yr = DateRange.year(2024)
        assert yr.days == 366  # 2024 is a leap year

    def test_contains(self) -> None:
        dr = DateRange("2024-01-01", "2024-12-31")
        assert dr.contains("2024-06-15")
        assert not dr.contains("2025-01-01")

    def test_overlaps(self) -> None:
        dr1 = DateRange("2024-01-01", "2024-06-30")
        dr2 = DateRange("2024-06-01", "2024-12-31")
        assert dr1.overlaps(dr2)

    def test_no_overlap(self) -> None:
        dr1 = DateRange("2024-01-01", "2024-03-31")
        dr2 = DateRange("2024-07-01", "2024-12-31")
        assert not dr1.overlaps(dr2)


class TestCard:
    def test_creation(self) -> None:
        card = Card("A", "♠")
        assert card.rank == "A"
        assert card.suit == "♠"

    def test_ace_value(self) -> None:
        assert Card("A", "♠").value == 11

    def test_face_card_value(self) -> None:
        assert Card("K", "♥").value == 10
        assert Card("Q", "♦").value == 10
        assert Card("J", "♣").value == 10

    def test_number_card_value(self) -> None:
        assert Card("7", "♠").value == 7
        assert Card("10", "♥").value == 10

    def test_immutable(self) -> None:
        card = Card("A", "♠")
        with pytest.raises(AttributeError):
            card.rank = "K"  # type: ignore[misc]

    def test_tuple_indexing(self) -> None:
        card = Card("A", "♠")
        assert card[0] == "A"
        assert card[1] == "♠"
