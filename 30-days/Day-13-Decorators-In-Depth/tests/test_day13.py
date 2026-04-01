"""Tests for Day 13 — Decorators"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)
import pytest
import time
from solutions import retry, timer, memoize, validate_args


class TestRetry:
    def test_succeeds_immediately(self) -> None:
        @retry(max_attempts=3)
        def always_ok() -> str:
            return "ok"
        assert always_ok() == "ok"

    def test_retries_on_failure(self) -> None:
        call_count = 0

        @retry(max_attempts=3, exceptions=(ValueError,))
        def eventually_ok() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("not yet")
            return "ok"

        assert eventually_ok() == "ok"
        assert call_count == 3

    def test_raises_after_max(self) -> None:
        @retry(max_attempts=2, exceptions=(ValueError,))
        def always_fails() -> str:
            raise ValueError("always")

        with pytest.raises(ValueError):
            always_fails()

    def test_preserves_name(self) -> None:
        @retry()
        def my_func() -> None: pass
        assert my_func.__name__ == "my_func"


class TestMemoize:
    def test_correct_result(self) -> None:
        @memoize
        def double(n: int) -> int:
            return n * 2
        assert double(5) == 10

    def test_caches_result(self) -> None:
        calls = 0

        @memoize
        def counted(n: int) -> int:
            nonlocal calls
            calls += 1
            return n * 2

        counted(5)
        counted(5)
        counted(5)
        assert calls == 1

    def test_different_args_not_cached(self) -> None:
        calls = 0

        @memoize
        def f(n: int) -> int:
            nonlocal calls
            calls += 1
            return n

        f(1)
        f(2)
        assert calls == 2

    def test_preserves_name(self) -> None:
        @memoize
        def named_fn() -> None: pass
        assert named_fn.__name__ == "named_fn"


class TestValidateArgs:
    def test_valid_passes(self) -> None:
        @validate_args(age=lambda x: isinstance(x, int) and x >= 0)
        def create(name: str, age: int) -> dict[str, object]:
            return {"name": name, "age": age}

        result = create(name="Alice", age=30)
        assert result == {"name": "Alice", "age": 30}

    def test_invalid_raises(self) -> None:
        @validate_args(age=lambda x: isinstance(x, int) and x >= 0)
        def create(name: str, age: int) -> dict[str, object]:
            return {}

        with pytest.raises(ValueError):
            create(name="Bob", age=-1)

    def test_preserves_name(self) -> None:
        @validate_args()
        def my_func() -> None: pass
        assert my_func.__name__ == "my_func"
