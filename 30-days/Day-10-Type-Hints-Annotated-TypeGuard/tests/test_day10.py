"""Tests for Day 10"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)
import pytest
from solutions import (
    is_str_list, is_positive_int, parse_status,
    format_percentage, narrow_and_process, MAX_RETRIES, DEFAULT_HOST,
)


class TestTypeGuards:
    def test_is_str_list_true(self) -> None:
        assert is_str_list(["a", "b", "c"]) is True

    def test_is_str_list_false(self) -> None:
        assert is_str_list([1, 2, 3]) is False

    def test_is_str_list_mixed(self) -> None:
        assert is_str_list(["a", 1]) is False

    def test_is_str_list_empty(self) -> None:
        assert is_str_list([]) is True

    def test_is_positive_int_true(self) -> None:
        assert is_positive_int(5) is True
        assert is_positive_int(1) is True

    def test_is_positive_int_zero(self) -> None:
        assert is_positive_int(0) is False

    def test_is_positive_int_negative(self) -> None:
        assert is_positive_int(-1) is False

    def test_is_positive_int_bool_excluded(self) -> None:
        # True == 1 but we exclude bools
        assert is_positive_int(True) is False

    def test_is_positive_int_str(self) -> None:
        assert is_positive_int("5") is False


class TestLiteralTypes:
    def test_parse_active(self) -> None:
        assert "active" in parse_status("active")

    def test_parse_inactive(self) -> None:
        assert "inactive" in parse_status("inactive")


class TestAnnotated:
    def test_format_percentage(self) -> None:
        assert format_percentage(0.5) == "50.0%"
        assert format_percentage(1.0) == "100.0%"
        assert format_percentage(0.0) == "0.0%"
        assert format_percentage(0.333) == "33.3%"


class TestFinalConstants:
    def test_max_retries_value(self) -> None:
        assert MAX_RETRIES == 3

    def test_default_host_value(self) -> None:
        assert DEFAULT_HOST == "localhost"


class TestNarrowAndProcess:
    def test_str_list_uppercased(self) -> None:
        result = narrow_and_process(["hello", "world"])
        assert result == ["HELLO", "WORLD"]

    def test_mixed_list_stringified(self) -> None:
        result = narrow_and_process([1, 2, 3])
        assert result == ["1", "2", "3"]
