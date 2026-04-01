"""
Tests for Day 01 — Variables, Types, and Literals
"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)

import pytest

from solutions import (
    classify,
    describe_result,
    factorial,
    find_first,
    format_table,
    safe_divide,
)


class TestSafeDivide:
    def test_integer_division_returns_float(self) -> None:
        assert safe_divide(10, 4) == 2.5
        assert isinstance(safe_divide(10, 4), float)

    def test_division_by_zero_returns_none(self) -> None:
        assert safe_divide(7, 0) is None

    def test_negative_divisor(self) -> None:
        assert safe_divide(10, -2) == -5.0

    def test_float_inputs(self) -> None:
        result = safe_divide(1.5, 0.5)
        assert result == pytest.approx(3.0)

    def test_zero_numerator(self) -> None:
        assert safe_divide(0, 5) == 0.0


class TestFormatTable:
    def test_header_present(self) -> None:
        result = format_table([("Alice", 95)])
        assert "Name" in result
        assert "Score" in result

    def test_data_rows(self) -> None:
        result = format_table([("Alice", 95), ("Bob", 87)])
        assert "Alice" in result
        assert "95" in result
        assert "Bob" in result
        assert "87" in result

    def test_separator_line(self) -> None:
        result = format_table([("X", 1)])
        assert "---" in result

    def test_empty_table(self) -> None:
        result = format_table([])
        assert "Name" in result  # header still present


class TestClassify:
    def test_none(self) -> None:
        assert classify(None) == "none"

    def test_bool_before_int(self) -> None:
        # Critical: bool must be classified as "boolean", not "integer"
        assert classify(True) == "boolean"
        assert classify(False) == "boolean"

    def test_int(self) -> None:
        assert classify(42) == "integer"
        assert classify(0) == "integer"
        assert classify(-100) == "integer"

    def test_float(self) -> None:
        assert classify(3.14) == "float"
        assert classify(0.0) == "float"

    def test_complex(self) -> None:
        assert classify(1 + 2j) == "complex"

    def test_str(self) -> None:
        assert classify("hello") == "text"
        assert classify("") == "text"

    def test_bytes(self) -> None:
        assert classify(b"hello") == "bytes"

    def test_other(self) -> None:
        assert classify([1, 2]) == "other"
        assert classify({"a": 1}) == "other"


class TestFindFirst:
    def test_finds_first_match(self) -> None:
        result = find_first([1, 5, 3, 8, 2], lambda x: x > 4)
        assert result == 5  # first element > 4 is 5

    def test_returns_none_when_not_found(self) -> None:
        result = find_first([1, 2, 3], lambda x: x > 100)
        assert result is None

    def test_empty_list(self) -> None:
        assert find_first([], lambda x: True) is None

    def test_first_element_matches(self) -> None:
        assert find_first([10, 20, 30], lambda x: x > 5) == 10


class TestDescribeResult:
    def test_none_says_not_found(self) -> None:
        assert describe_result(None) == "not found"

    def test_value_says_found(self) -> None:
        assert describe_result(5) == "found: 5"

    def test_zero_is_not_none(self) -> None:
        # Common bug: 'if not result' would misidentify 0 as not found
        assert describe_result(0) == "found: 0"

    def test_empty_string_is_not_none(self) -> None:
        assert describe_result("") == "found: "


class TestFactorial:
    def test_zero(self) -> None:
        assert factorial(0) == 1

    def test_one(self) -> None:
        assert factorial(1) == 1

    def test_small(self) -> None:
        assert factorial(5) == 120
        assert factorial(10) == 3628800

    def test_large_arbitrary_precision(self) -> None:
        # Python int has arbitrary precision — no overflow
        f100 = factorial(100)
        assert len(str(f100)) == 158  # 158 digits

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError):
            factorial(-1)


class TestPythonTypeFundamentals:
    """Tests that verify Python type system behaviour."""

    def test_bool_is_subtype_of_int(self) -> None:
        assert isinstance(True, int)
        assert isinstance(False, int)

    def test_none_is_singleton(self) -> None:
        x = None
        y = None
        assert x is y  # same object

    def test_arbitrary_precision(self) -> None:
        # Python int never overflows
        huge = 2 ** 1000
        assert huge > 0
        assert isinstance(huge, int)

    def test_float_ieee754_quirk(self) -> None:
        # Same in Python and C++
        assert 0.1 + 0.2 != 0.3

    def test_is_vs_equality(self) -> None:
        a = [1, 2, 3]
        b = [1, 2, 3]
        assert a == b    # same value
        assert a is not b  # different objects
