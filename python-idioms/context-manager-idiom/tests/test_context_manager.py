"""pytest tests for context manager idiom."""
from __future__ import annotations

import sys
import tempfile
import os
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from context_manager import (
    DatabaseConnection,
    FakeLegacyResource,
    Timer,
    managed_connection,
    temporary_attribute,
)
import contextlib


class TestDatabaseConnection:
    def test_commits_on_success(self) -> None:
        db = DatabaseConnection("test://db")
        with db:
            db.execute("INSERT 1")
        assert db.committed
        assert not db.rolled_back

    def test_rolls_back_on_exception(self) -> None:
        db = DatabaseConnection("test://db")
        with pytest.raises(ValueError):
            with db:
                raise ValueError("boom")
        assert db.rolled_back
        assert not db.committed

    def test_closed_after_block(self) -> None:
        db = DatabaseConnection("test://db")
        with db:
            pass
        assert not db.connected

    def test_resource_released_on_exception(self) -> None:
        db = DatabaseConnection("test://db")
        try:
            with db:
                raise RuntimeError("fail")
        except RuntimeError:
            pass
        assert not db.connected


class TestTimer:
    def test_elapsed_is_non_negative(self) -> None:
        with Timer() as t:
            pass
        assert t.elapsed >= 0.0

    def test_elapsed_populated_after_block(self) -> None:
        t = Timer()
        assert t.elapsed == 0.0
        with t:
            pass
        assert t.elapsed > 0.0


class TestManagedConnection:
    def test_commits_on_success(self) -> None:
        with managed_connection("test://db") as conn:
            conn.execute("SELECT 1")
        assert conn.committed

    def test_rolls_back_on_exception(self) -> None:
        conn_ref: list[DatabaseConnection] = []
        with pytest.raises(ValueError):
            with managed_connection("test://db") as conn:
                conn_ref.append(conn)
                raise ValueError("boom")
        assert conn_ref[0].rolled_back


class TestNestedContextManagers:
    def test_nested_managers_both_exit(self) -> None:
        db1 = DatabaseConnection("db1")
        db2 = DatabaseConnection("db2")
        with db1:
            with db2:
                db2.execute("q")
        assert not db1.connected
        assert not db2.connected


class TestTemporaryAttribute:
    def test_attribute_restored(self) -> None:
        class Obj:
            x = 1

        obj = Obj()
        with temporary_attribute(obj, "x", 42):
            assert obj.x == 42
        assert obj.x == 1

    def test_attribute_restored_on_exception(self) -> None:
        class Obj:
            x = 1

        obj = Obj()
        with pytest.raises(RuntimeError):
            with temporary_attribute(obj, "x", 99):
                raise RuntimeError()
        assert obj.x == 1


class TestSuppress:
    def test_suppress_silences_file_not_found(self) -> None:
        with contextlib.suppress(FileNotFoundError):
            open("/no/such/path/file.txt")  # noqa: WPS515

    def test_suppress_does_not_silence_other_errors(self) -> None:
        with pytest.raises(ValueError):
            with contextlib.suppress(FileNotFoundError):
                raise ValueError("not suppressed")
