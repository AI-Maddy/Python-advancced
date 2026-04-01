"""
Day 02 — Solutions
"""
from __future__ import annotations

import functools
from typing import Callable


def log(*messages: str, level: str = "INFO", sep: str = " ") -> str:
    """Return a formatted log line."""
    joined = sep.join(messages)
    return f"[{level}] {joined}"


def make_counter(
    start: int = 0, step: int = 1
) -> dict[str, Callable[[], int]]:
    """Return a dict of counter operations using closures."""
    count = start

    def increment() -> int:
        nonlocal count
        count += step
        return count

    def decrement() -> int:
        nonlocal count
        count -= step
        return count

    def reset() -> int:
        nonlocal count
        count = start
        return count

    def value() -> int:
        return count

    return {
        "increment": increment,
        "decrement": decrement,
        "reset": reset,
        "value": value,
    }


def compose(*funcs: Callable[[int], int]) -> Callable[[int], int]:
    """Right-to-left composition: compose(f,g,h)(x) == f(g(h(x)))."""
    def composed(x: int) -> int:
        for f in reversed(funcs):
            x = f(x)
        return x
    return composed


def pipe(*funcs: Callable[[int], int]) -> Callable[[int], int]:
    """Left-to-right pipeline: pipe(f,g,h)(x) == h(g(f(x)))."""
    def piped(x: int) -> int:
        for f in funcs:
            x = f(x)
        return x
    return piped


def memoize(func: Callable[..., int]) -> Callable[..., int]:
    """Return a memoized version of func."""
    cache: dict[tuple[object, ...], int] = {}

    def wrapper(*args: object) -> int:
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper


def slow_fib(n: int) -> int:
    """Recursive Fibonacci."""
    if n <= 1:
        return n
    return slow_fib(n - 1) + slow_fib(n - 2)


def my_partial(
    func: Callable[..., int], *bound_args: object, **bound_kwargs: object
) -> Callable[..., int]:
    """Return func with some args pre-filled."""
    def wrapper(*args: object, **kwargs: object) -> int:
        return func(*bound_args, *args, **bound_kwargs, **kwargs)
    return wrapper


def multiply(x: int, y: int) -> int:
    """Return x * y."""
    return x * y


if __name__ == "__main__":
    print(log("started", "server"))              # [INFO] started server
    print(log("a", "b", level="ERROR", sep="|")) # [ERROR] a|b

    c = make_counter()
    c["increment"]()
    c["increment"]()
    print(c["value"]())   # 2
    c["reset"]()
    print(c["value"]())   # 0

    add1 = lambda x: x + 1
    times2 = lambda x: x * 2
    sq = lambda x: x ** 2
    f = compose(add1, times2, sq)
    print(f(3))   # 19

    g = pipe(sq, times2, add1)
    print(g(3))   # 19

    memo_fib = memoize(slow_fib)
    print(memo_fib(10))   # 55

    mul3 = my_partial(multiply, 3)
    print(mul3(7))   # 21
