"""pytest tests for generator idiom."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from generator_idiom import (
    accumulator,
    chain,
    countdown,
    fibonacci,
    filter_gen,
    flatten,
    integers_from,
    map_gen,
    resilient_generator,
    running_average,
    take,
    take_gen,
)


class TestFibonacci:
    def test_first_ten(self) -> None:
        fib = fibonacci()
        assert take(10, fib) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_is_lazy(self) -> None:
        fib = fibonacci()
        # Should not hang — only materialises what we ask for
        first = next(fib)
        assert first == 0


class TestCountdown:
    def test_yields_correct_sequence(self) -> None:
        assert list(countdown(5)) == [5, 4, 3, 2, 1]

    def test_return_value(self) -> None:
        gen = countdown(3)
        values = []
        try:
            while True:
                values.append(next(gen))
        except StopIteration as e:
            assert e.value == "done"
        assert values == [3, 2, 1]


class TestAccumulator:
    def test_send_accumulates(self) -> None:
        acc = accumulator()
        next(acc)
        assert acc.send(10.0) == 10.0
        assert acc.send(5.0) == 15.0
        assert acc.send(3.0) == 18.0

    def test_initial_total_is_zero(self) -> None:
        acc = accumulator()
        total = next(acc)
        assert total == 0.0


class TestRunningAverage:
    def test_running_average(self) -> None:
        avg = running_average()
        next(avg)
        avg.send(10.0)
        result = avg.send(20.0)
        assert result == pytest.approx(15.0)

    def test_initial_average_is_zero(self) -> None:
        avg = running_average()
        assert next(avg) == 0.0


class TestResilientGenerator:
    def test_throw_resets(self) -> None:
        gen = resilient_generator()
        assert next(gen) == 0
        assert next(gen) == 1
        # throw() is caught internally; generator resets i=0 and yields 0
        thrown_result = gen.throw(ValueError, "test")
        assert thrown_result == 0  # generator resumed with i=0

    def test_close_stops(self) -> None:
        gen = resilient_generator()
        next(gen)
        gen.close()
        with pytest.raises(StopIteration):
            next(gen)


class TestFlatten:
    def test_already_flat(self) -> None:
        assert list(flatten([1, 2, 3])) == [1, 2, 3]

    def test_nested(self) -> None:
        assert list(flatten([1, [2, [3, 4], 5], [6, 7]])) == [1, 2, 3, 4, 5, 6, 7]

    def test_empty(self) -> None:
        assert list(flatten([])) == []


class TestChain:
    def test_chains_iterators(self) -> None:
        result = list(chain(iter([1, 2]), iter([3, 4])))
        assert result == [1, 2, 3, 4]


class TestPipeline:
    def test_take_gen(self) -> None:
        result = list(take_gen(3, integers_from(0)))
        assert result == [0, 1, 2]

    def test_filter_gen(self) -> None:
        result = list(take_gen(5, filter_gen(lambda x: x % 2 == 0, integers_from(0))))
        assert result == [0, 2, 4, 6, 8]

    def test_map_gen(self) -> None:
        result = list(take_gen(4, map_gen(lambda x: x ** 2, integers_from(1))))
        assert result == [1, 4, 9, 16]

    def test_composed_pipeline(self) -> None:
        pipeline = take_gen(
            5,
            map_gen(
                lambda x: x ** 2,
                filter_gen(lambda x: x % 2 == 0, integers_from(0))
            )
        )
        assert list(pipeline) == [0, 4, 16, 36, 64]
