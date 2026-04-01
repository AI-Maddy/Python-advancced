"""Day 13 — Exercises: Decorators"""
from __future__ import annotations
import functools, time
from typing import Callable, TypeVar, ParamSpec
P = ParamSpec("P"); T = TypeVar("T")

# Ex 1: @retry(max_attempts, delay, exceptions)
def retry(max_attempts: int=3, delay: float=0.0,
          exceptions: tuple[type[Exception],...] = (Exception,)) -> Callable[[Callable[P,T]], Callable[P,T]]:
    pass  # TODO

# Ex 2: @timer — print elapsed time
def timer(func: Callable[P, T]) -> Callable[P, T]:
    pass  # TODO

# Ex 3: @memoize — cache results
def memoize(func: Callable[P, T]) -> Callable[P, T]:
    pass  # TODO

# Ex 4: @validate_args(**validators) — validate kwargs
def validate_args(**validators: Callable[[object], bool]) -> Callable[[Callable[P,T]], Callable[P,T]]:
    pass  # TODO

if __name__ == "__main__":
    @memoize
    def fib(n: int) -> int:
        if n <= 1: return n
        return fib(n-1) + fib(n-2)
    print(fib(20))
