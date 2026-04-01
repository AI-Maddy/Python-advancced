"""Tests for Day 15 — Error Handling"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)
import pytest
from solutions import (
    AppError, ValidationError, NotFoundError, DatabaseError,
    ConnectionError, safe_divide, validate_form,
)


class TestExceptionHierarchy:
    def test_validation_is_app_error(self) -> None:
        with pytest.raises(AppError):
            raise ValidationError("field", "bad")

    def test_not_found_is_app_error(self) -> None:
        with pytest.raises(AppError):
            raise NotFoundError("User", 1)

    def test_connection_is_database_error(self) -> None:
        with pytest.raises(DatabaseError):
            raise ConnectionError("localhost", 5432)

    def test_connection_is_app_error(self) -> None:
        with pytest.raises(AppError):
            raise ConnectionError("localhost", 5432)


class TestValidationError:
    def test_has_field(self) -> None:
        e = ValidationError("email", "invalid")
        assert e.field == "email"

    def test_has_value(self) -> None:
        e = ValidationError("age", "must be positive", value=-1)
        assert e.value == -1

    def test_has_code(self) -> None:
        e = ValidationError("x", "bad")
        assert e.code > 0

    def test_str_contains_field(self) -> None:
        e = ValidationError("email", "invalid format")
        assert "email" in str(e)


class TestNotFoundError:
    def test_has_resource(self) -> None:
        e = NotFoundError("User", 42)
        assert e.resource == "User"

    def test_has_id(self) -> None:
        e = NotFoundError("User", 42)
        assert e.resource_id == 42

    def test_str_contains_info(self) -> None:
        e = NotFoundError("Product", "p-001")
        s = str(e)
        assert "Product" in s
        assert "p-001" in s


class TestSafeDivide:
    def test_normal(self) -> None:
        assert safe_divide(10.0, 2.0) == pytest.approx(5.0)

    def test_zero_raises_validation_error(self) -> None:
        with pytest.raises(ValidationError):
            safe_divide(1.0, 0.0)


class TestValidateForm:
    def test_valid_form_passes(self) -> None:
        validate_form({"name": "Alice", "age": 25, "email": "a@b.com"})  # no exception

    def test_invalid_form_raises_group(self) -> None:
        with pytest.raises(ExceptionGroup):
            validate_form({"name": "", "age": -1, "email": "bad"})

    def test_multiple_errors_collected(self) -> None:
        try:
            validate_form({"name": "", "age": -1, "email": "bad"})
        except ExceptionGroup as eg:
            assert len(eg.exceptions) >= 2

    def test_single_error(self) -> None:
        try:
            validate_form({"name": "", "age": 25, "email": "a@b.com"})
        except ExceptionGroup as eg:
            assert len(eg.exceptions) == 1
