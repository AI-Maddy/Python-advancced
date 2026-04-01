"""Tests for Day 11 — Generic OOP Design"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)
import pytest
from solutions import Repository, Ok, Err, safe_divide, safe_parse_int, EventBus


class TestRepository:
    def test_save_and_find(self) -> None:
        repo: Repository[str, int] = Repository()  # type: ignore
        repo.save(1, "Alice")
        assert repo.find_by_id(1) == "Alice"

    def test_find_missing(self) -> None:
        repo: Repository[str, int] = Repository()  # type: ignore
        assert repo.find_by_id(999) is None

    def test_find_all(self) -> None:
        repo: Repository[str, int] = Repository()  # type: ignore
        repo.save(1, "Alice")
        repo.save(2, "Bob")
        assert set(repo.find_all()) == {"Alice", "Bob"}

    def test_delete(self) -> None:
        repo: Repository[str, int] = Repository()  # type: ignore
        repo.save(1, "Alice")
        assert repo.delete(1) is True
        assert repo.find_by_id(1) is None

    def test_delete_missing(self) -> None:
        repo: Repository[str, int] = Repository()  # type: ignore
        assert repo.delete(999) is False

    def test_count(self) -> None:
        repo: Repository[str, int] = Repository()  # type: ignore
        assert repo.count() == 0
        repo.save(1, "x")
        assert repo.count() == 1


class TestResult:
    def test_ok_is_ok(self) -> None:
        assert Ok(42).is_ok() is True
        assert Ok(42).is_err() is False

    def test_err_is_err(self) -> None:
        assert Err(ValueError("x")).is_err() is True
        assert Err(ValueError("x")).is_ok() is False

    def test_ok_unwrap(self) -> None:
        assert Ok(42).unwrap() == 42

    def test_err_unwrap_raises(self) -> None:
        with pytest.raises(ValueError):
            Err(ValueError("oops")).unwrap()

    def test_safe_divide_ok(self) -> None:
        r = safe_divide(10.0, 2.0)
        assert r.is_ok()
        assert r.unwrap() == pytest.approx(5.0)

    def test_safe_divide_zero(self) -> None:
        r = safe_divide(1.0, 0.0)
        assert r.is_err()

    def test_safe_parse_int_ok(self) -> None:
        r = safe_parse_int("42")
        assert r.is_ok()
        assert r.unwrap() == 42

    def test_safe_parse_int_err(self) -> None:
        r = safe_parse_int("bad")
        assert r.is_err()


class TestEventBus:
    def test_subscribe_and_publish(self) -> None:
        bus: EventBus[int] = EventBus()
        received: list[int] = []
        bus.subscribe(received.append)
        bus.publish(42)
        assert received == [42]

    def test_multiple_handlers(self) -> None:
        bus: EventBus[str] = EventBus()
        a: list[str] = []
        b: list[str] = []
        bus.subscribe(a.append)
        bus.subscribe(b.append)
        bus.publish("event")
        assert a == ["event"]
        assert b == ["event"]

    def test_handler_count(self) -> None:
        bus: EventBus[int] = EventBus()
        bus.subscribe(lambda x: None)
        bus.subscribe(lambda x: None)
        assert bus.handler_count() == 2
