"""pytest tests for classmethod factory idiom."""
from __future__ import annotations

import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from classmethod_factory import (
    Connection,
    Date,
    HandlerA,
    HandlerB,
    Registry,
    TypedList,
)


class TestDate:
    def test_from_string(self) -> None:
        d = Date.from_string("2024-03-15")
        assert d.year == 2024
        assert d.month == 3
        assert d.day == 15

    def test_from_timestamp(self) -> None:
        ts = time.mktime((2024, 6, 1, 0, 0, 0, 0, 0, 0))
        d = Date.from_timestamp(ts)
        assert d.year == 2024
        assert d.month == 6
        assert d.day == 1

    def test_today_returns_today(self) -> None:
        import datetime
        today = datetime.date.today()
        d = Date.today()
        assert d.year == today.year
        assert d.month == today.month
        assert d.day == today.day

    def test_equality(self) -> None:
        d1 = Date.from_string("2024-01-01")
        d2 = Date(2024, 1, 1)
        assert d1 == d2

    def test_to_string(self) -> None:
        d = Date(2024, 3, 5)
        assert d.to_string() == "2024-03-05"

    def test_invalid_month_raises(self) -> None:
        with pytest.raises(ValueError):
            Date(2024, 13, 1)

    def test_invalid_day_raises(self) -> None:
        with pytest.raises(ValueError):
            Date(2024, 1, 0)

    def test_each_factory_produces_date(self) -> None:
        for d in (Date.from_string("2024-05-01"), Date.today(), Date.from_timestamp(0)):
            assert isinstance(d, Date)


class TestConnection:
    def test_from_dsn(self) -> None:
        conn = Connection.from_dsn("postgresql://db.example.com:5432/myapp")
        assert conn.host == "db.example.com"
        assert conn.port == 5432
        assert conn.database == "myapp"

    def test_local(self) -> None:
        conn = Connection.local("testdb")
        assert conn.host == "127.0.0.1"
        assert conn.port == 5432
        assert conn.database == "testdb"

    def test_readonly(self) -> None:
        conn = Connection.readonly("replica.example.com", "analytics")
        assert conn.port == 5433
        assert conn.database == "analytics"

    def test_each_factory_produces_connection(self) -> None:
        conns = [
            Connection.from_dsn("postgresql://h:5432/d"),
            Connection.local("d"),
            Connection.readonly("h", "d"),
        ]
        for c in conns:
            assert isinstance(c, Connection)


class TestInitSubclass:
    def test_handler_a_registered(self) -> None:
        assert "handler_a" in Registry._registry

    def test_handler_b_registered(self) -> None:
        assert "handler_b" in Registry._registry

    def test_get_returns_correct_class(self) -> None:
        assert Registry.get("handler_a") is HandlerA
        assert Registry.get("handler_b") is HandlerB


class TestTypedList:
    def test_int_list_valid(self) -> None:
        IntList = TypedList[int]
        il = IntList([1, 2, 3])
        assert il._items == [1, 2, 3]

    def test_int_list_rejects_string(self) -> None:
        IntList = TypedList[int]
        with pytest.raises(TypeError):
            IntList([1, "two"])

    def test_str_list_valid(self) -> None:
        StrList = TypedList[str]
        sl = StrList(["a", "b"])
        assert sl._items == ["a", "b"]

    def test_different_specialisations_are_different_types(self) -> None:
        IntList = TypedList[int]
        StrList = TypedList[str]
        assert IntList is not StrList

    def test_class_getitem_returns_type(self) -> None:
        IntList = TypedList[int]
        assert issubclass(IntList, TypedList)
