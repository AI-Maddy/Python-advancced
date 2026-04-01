"""
Tests for Day 05 — Context Managers and RAII
"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)

import os
import time

import pytest

from solutions import DatabaseTransaction, Timer, suppress_errors, temp_environ


class TestDatabaseTransaction:
    def test_commit_on_success(self) -> None:
        with DatabaseTransaction("test") as tx:
            tx.execute("INSERT INTO t VALUES (1)")
        assert tx.committed is True
        assert tx.rolled_back is False

    def test_rollback_on_exception(self) -> None:
        try:
            with DatabaseTransaction("test") as tx:
                tx.execute("INSERT INTO t VALUES (1)")
                raise ValueError("oops")
        except ValueError:
            pass
        assert tx.rolled_back is True
        assert tx.committed is False

    def test_exception_propagates(self) -> None:
        """Exceptions should NOT be suppressed by default."""
        with pytest.raises(RuntimeError):
            with DatabaseTransaction("test"):
                raise RuntimeError("not suppressed")

    def test_execute_stores_ops(self) -> None:
        with DatabaseTransaction("test") as tx:
            tx.execute("op1")
            tx.execute("op2")
        # After commit, ops might be kept or cleared — just check no error


class TestTimer:
    def test_elapsed_recorded(self) -> None:
        with Timer() as t:
            time.sleep(0.05)
        assert t.elapsed >= 0.04  # at least 40ms

    def test_elapsed_on_exception(self) -> None:
        """Timer should still record elapsed even if exception occurs."""
        try:
            with Timer() as t:
                time.sleep(0.02)
                raise ValueError("test")
        except ValueError:
            pass
        assert t.elapsed >= 0.01

    def test_returns_self(self) -> None:
        t = Timer()
        with t as result:
            pass
        assert result is t


class TestSuppressErrors:
    def test_suppresses_specified_exception(self) -> None:
        with suppress_errors(ValueError) as caught:
            int("bad")
        assert len(caught) == 1
        assert isinstance(caught[0], ValueError)

    def test_does_not_suppress_other_exceptions(self) -> None:
        with pytest.raises(RuntimeError):
            with suppress_errors(ValueError):
                raise RuntimeError("not suppressed")

    def test_no_exception_empty_list(self) -> None:
        with suppress_errors(ValueError) as caught:
            pass
        assert caught == []

    def test_multiple_exception_types(self) -> None:
        with suppress_errors(ValueError, TypeError) as caught:
            raise TypeError("type error")
        assert len(caught) == 1


class TestTempEnviron:
    def test_sets_variable(self) -> None:
        with temp_environ(TEST_VAR="hello"):
            assert os.environ["TEST_VAR"] == "hello"

    def test_restores_after_exit(self) -> None:
        original = os.environ.get("TEST_VAR_UNIQUE_XYZ")
        with temp_environ(TEST_VAR_UNIQUE_XYZ="temporary"):
            assert os.environ["TEST_VAR_UNIQUE_XYZ"] == "temporary"
        assert os.environ.get("TEST_VAR_UNIQUE_XYZ") == original

    def test_restores_on_exception(self) -> None:
        try:
            with temp_environ(TEST_X="123"):
                raise RuntimeError("oops")
        except RuntimeError:
            pass
        assert os.environ.get("TEST_X") is None
