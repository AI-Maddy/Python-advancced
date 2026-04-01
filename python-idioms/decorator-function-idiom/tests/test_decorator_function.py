"""pytest tests for decorator-function idiom."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from decorator_function import (
    CallCounter,
    Circle,
    add_exclamation,
    expensive_fib,
    factorial,
    greet,
    log_calls,
    retry,
    uppercase_result,
    validate_types,
)


class TestWrapsPreservesMetadata:
    def test_name_preserved(self) -> None:
        @log_calls
        def my_func() -> None:
            """My docstring."""

        assert my_func.__name__ == "my_func"

    def test_doc_preserved(self) -> None:
        @log_calls
        def my_func() -> None:
            """My docstring."""

        assert my_func.__doc__ == "My docstring."

    def test_wrapped_attribute_set(self) -> None:
        @log_calls
        def my_func() -> None:
            pass

        assert hasattr(my_func, "__wrapped__")


class TestRetryDecorator:
    def test_succeeds_on_first_try(self) -> None:
        @retry(times=3)
        def always_ok() -> str:
            return "ok"

        assert always_ok() == "ok"

    def test_retries_on_failure(self) -> None:
        attempts: list[int] = [0]

        @retry(times=3, exceptions=(ValueError,))
        def flaky() -> str:
            attempts[0] += 1
            if attempts[0] < 3:
                raise ValueError("not yet")
            return "done"

        result = flaky()
        assert result == "done"
        assert attempts[0] == 3

    def test_raises_after_all_retries(self) -> None:
        @retry(times=2, exceptions=(ValueError,))
        def always_fails() -> None:
            raise ValueError("always")

        with pytest.raises(ValueError):
            always_fails()


class TestValidateTypes:
    def test_valid_types_pass(self) -> None:
        @validate_types(x=int, y=int)
        def add(x: int, y: int) -> int:
            return x + y

        assert add(1, 2) == 3

    def test_wrong_type_raises_type_error(self) -> None:
        @validate_types(x=int)
        def identity(x: int) -> int:
            return x

        with pytest.raises(TypeError):
            identity("not an int")  # type: ignore[arg-type]


class TestCallCounter:
    def test_increments_on_call(self) -> None:
        @CallCounter
        def func() -> None:
            pass

        assert func.call_count == 0
        func()
        func()
        assert func.call_count == 2

    def test_reset(self) -> None:
        @CallCounter
        def func() -> None:
            pass

        func()
        func.reset()
        assert func.call_count == 0

    def test_wraps_preserved(self) -> None:
        @CallCounter
        def named_func() -> None:
            """Doc."""

        assert named_func.__name__ == "named_func"


class TestStackingDecorators:
    def test_greet_stacks_correctly(self) -> None:
        result = greet("world")
        assert result == "HELLO WORLD!"

    def test_order_matters(self) -> None:
        def say(s: str) -> str:
            return s

        # uppercase then exclamation
        r1 = add_exclamation(uppercase_result(say))("hi")
        # exclamation then uppercase
        r2 = uppercase_result(add_exclamation(say))("hi")
        assert r1 == "HI!"
        assert r2 == "HI!"


class TestLruCache:
    def test_fib_correct(self) -> None:
        expensive_fib.cache_clear()
        assert expensive_fib(10) == 55

    def test_cache_hits(self) -> None:
        expensive_fib.cache_clear()
        for _ in range(5):
            expensive_fib(20)
        info = expensive_fib.cache_info()
        assert info.hits > 0

    def test_factorial_correct(self) -> None:
        factorial.cache_clear()
        assert factorial(5) == 120

    def test_cached_property_computed_once(self) -> None:
        c = Circle(3.0)
        _ = c.area
        _ = c.area
        assert "area" in c.__dict__
