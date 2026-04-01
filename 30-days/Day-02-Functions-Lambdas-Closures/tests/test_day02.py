"""
Tests for Day 02 — Functions, Lambdas, and Closures
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
    compose,
    log,
    make_counter,
    memoize,
    multiply,
    my_partial,
    pipe,
    slow_fib,
)


class TestLog:
    def test_single_message(self) -> None:
        assert log("hello") == "[INFO] hello"

    def test_multiple_messages_default_sep(self) -> None:
        assert log("a", "b", "c") == "[INFO] a b c"

    def test_custom_level(self) -> None:
        assert log("boom", level="ERROR") == "[ERROR] boom"

    def test_custom_sep(self) -> None:
        assert log("x", "y", sep="|") == "[INFO] x|y"

    def test_level_and_sep(self) -> None:
        assert log("a", "b", level="WARN", sep=",") == "[WARN] a,b"


class TestMakeCounter:
    def test_starts_at_zero(self) -> None:
        c = make_counter()
        assert c["value"]() == 0

    def test_increment(self) -> None:
        c = make_counter()
        c["increment"]()
        assert c["value"]() == 1
        c["increment"]()
        assert c["value"]() == 2

    def test_decrement(self) -> None:
        c = make_counter(start=5)
        c["decrement"]()
        assert c["value"]() == 4

    def test_reset(self) -> None:
        c = make_counter(start=10)
        c["increment"]()
        c["increment"]()
        c["reset"]()
        assert c["value"]() == 10

    def test_custom_step(self) -> None:
        c = make_counter(step=5)
        c["increment"]()
        assert c["value"]() == 5
        c["increment"]()
        assert c["value"]() == 10

    def test_independent_counters(self) -> None:
        c1 = make_counter()
        c2 = make_counter(start=100)
        c1["increment"]()
        assert c1["value"]() == 1
        assert c2["value"]() == 100  # unaffected


class TestCompose:
    def test_single_function(self) -> None:
        f = compose(lambda x: x + 1)
        assert f(5) == 6

    def test_two_functions_right_to_left(self) -> None:
        # compose(f, g)(x) == f(g(x))
        f = compose(lambda x: x + 1, lambda x: x * 2)
        assert f(3) == 7   # 3*2=6, 6+1=7

    def test_three_functions(self) -> None:
        sq = lambda x: x ** 2
        times2 = lambda x: x * 2
        add1 = lambda x: x + 1
        f = compose(add1, times2, sq)   # add1(times2(sq(3)))
        assert f(3) == 19   # sq(3)=9, *2=18, +1=19


class TestPipe:
    def test_single_function(self) -> None:
        f = pipe(lambda x: x + 1)
        assert f(5) == 6

    def test_two_functions_left_to_right(self) -> None:
        # pipe(f, g)(x) == g(f(x))
        f = pipe(lambda x: x * 2, lambda x: x + 1)
        assert f(3) == 7   # 3*2=6, 6+1=7

    def test_compose_and_pipe_same_result(self) -> None:
        """compose(f,g,h) and pipe(h,g,f) should give same result."""
        sq = lambda x: x ** 2
        times2 = lambda x: x * 2
        add1 = lambda x: x + 1
        assert compose(add1, times2, sq)(4) == pipe(sq, times2, add1)(4)


class TestMemoize:
    def test_correct_result(self) -> None:
        memo_fib = memoize(slow_fib)
        assert memo_fib(10) == 55

    def test_caches_results(self) -> None:
        call_count = 0

        def counting_func(n: int) -> int:
            nonlocal call_count
            call_count += 1
            return n * 2

        memo = memoize(counting_func)
        memo(5)
        memo(5)
        memo(5)
        assert call_count == 1  # only called once

    def test_different_args_not_cached(self) -> None:
        memo = memoize(lambda x: x * 3)
        assert memo(3) == 9
        assert memo(4) == 12


class TestMyPartial:
    def test_positional_pre_fill(self) -> None:
        mul3 = my_partial(multiply, 3)
        assert mul3(7) == 21

    def test_remaining_args(self) -> None:
        mul3 = my_partial(multiply, 3)
        assert mul3(0) == 0
        assert mul3(-1) == -3

    def test_composability(self) -> None:
        add = lambda a, b: a + b
        add10 = my_partial(add, 10)
        assert add10(5) == 15
