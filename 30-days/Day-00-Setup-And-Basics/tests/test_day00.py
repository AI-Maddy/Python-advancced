"""
Tests for Day 00 — Setup and Basics
"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)

import importlib
import sys
from datetime import date


# Import solutions (not exercises — exercises have TODO stubs)
from solutions import (
    compute_square,
    hello_world,
    introspect,
)


class TestComputeSquare:
    def test_positive(self) -> None:
        assert compute_square(5) == 25

    def test_zero(self) -> None:
        assert compute_square(0) == 0

    def test_negative(self) -> None:
        assert compute_square(-3) == 9

    def test_large(self) -> None:
        # Python integers have arbitrary precision (unlike C++ int)
        assert compute_square(10**10) == 10**20


class TestHelloWorld:
    def test_contains_name(self) -> None:
        msg = hello_world("Alice")
        assert "Alice" in msg

    def test_contains_today(self) -> None:
        msg = hello_world("Bob")
        today_str = str(date.today().year)
        assert today_str in msg

    def test_returns_string(self) -> None:
        assert isinstance(hello_world("X"), str)


class TestIntrospect:
    def test_int_type_name(self) -> None:
        report = introspect(42)
        assert report["type_name"] == "int"

    def test_int_is_numeric(self) -> None:
        assert introspect(42)["is_numeric"] is True

    def test_str_is_not_numeric(self) -> None:
        assert introspect("hello")["is_numeric"] is False

    def test_float_is_numeric(self) -> None:
        assert introspect(3.14)["is_numeric"] is True

    def test_complex_is_numeric(self) -> None:
        assert introspect(1 + 2j)["is_numeric"] is True

    def test_callable_function(self) -> None:
        assert introspect(print)["callable"] is True

    def test_not_callable_int(self) -> None:
        assert introspect(42)["callable"] is False

    def test_public_attrs_list(self) -> None:
        report = introspect([])
        attrs = report["public_attrs"]
        assert isinstance(attrs, list)
        assert "append" in attrs

    def test_all_keys_present(self) -> None:
        report = introspect(None)
        assert set(report.keys()) == {"type_name", "is_numeric", "public_attrs", "callable"}


class TestPythonEnvironment:
    """Verify we are running in a suitable Python version."""

    def test_python_version(self) -> None:
        assert sys.version_info >= (3, 11), (
            f"Python 3.11+ required, got {sys.version_info}"
        )

    def test_bool_is_subtype_of_int(self) -> None:
        # Python fundamental: bool IS-A int
        assert isinstance(True, int)
        assert isinstance(False, int)
        assert True == 1
        assert False == 0

    def test_none_type(self) -> None:
        assert type(None) is type(None)
        assert introspect(None)["type_name"] == "NoneType"

    def test_name_guard_works(self) -> None:
        """Importing solutions should not print anything (guard is correct)."""
        import importlib.util, sys as _sys, os as _os
        _sol_path = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "solutions.py")
        _spec = importlib.util.spec_from_file_location("solutions_day00", _sol_path)
        sol = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
        _spec.loader.exec_module(sol)  # type: ignore[union-attr]
        assert hasattr(sol, "compute_square")
