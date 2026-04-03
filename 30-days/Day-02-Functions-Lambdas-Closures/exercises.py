"""
Day 02 — Exercises: Functions, Lambdas, and Closures
"""
from __future__ import annotations

from typing import Callable


# ---------------------------------------------------------------------------
# Exercise 1: Variadic Logger
# ---------------------------------------------------------------------------
# Write `log(*messages, level="INFO", sep=" ")` that:
#   - Accepts any number of message arguments
#   - Joins them with `sep`
#   - Prefixes with [LEVEL]
#   - Returns the formatted string (don't print, return)
#
# Examples:
#   log("started", "server")         → "[INFO] started server"
#   log("error", "not found", level="ERROR", sep=" | ")
#                                    → "[ERROR] error | not found"

def log(*messages: str, level: str = "INFO", sep: str = " ") -> str:
    """Return a formatted log line."""
    joined = sep.join(messages)
    return f"[{level}] {joined}"


# ---------------------------------------------------------------------------
# Exercise 2: Closure Counter with Reset
# ---------------------------------------------------------------------------
# Write `make_counter(start=0, step=1)` that returns a counter object
# as a dict of callables:
#   {"increment": fn, "decrement": fn, "reset": fn, "value": fn}
#
# - increment() adds step to the count
# - decrement() subtracts step
# - reset() sets count back to start
# - value() returns the current count

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


# ---------------------------------------------------------------------------
# Exercise 3: Function Composition
# ---------------------------------------------------------------------------
# Write `compose(*funcs)` that returns a function applying each func
# in right-to-left order (mathematical composition):
#   compose(f, g, h)(x) == f(g(h(x)))
#
# Write `pipe(*funcs)` for left-to-right:
#   pipe(f, g, h)(x) == h(g(f(x)))

def compose(*funcs: Callable[[int], int]) -> Callable[[int], int]:
    """Return right-to-left composition of funcs."""
    def composed(x: int) -> int:
        for f in reversed(funcs):
            x = f(x)
        return x
    return composed


def pipe(*funcs: Callable[[int], int]) -> Callable[[int], int]:
    """Return left-to-right pipeline of funcs."""
    def piped(x: int) -> int:
        for f in funcs:
            x = f(x)
        return x
    return piped


# ---------------------------------------------------------------------------
# Exercise 4: Memoise with Closure
# ---------------------------------------------------------------------------
# Write `memoize(func)` — a higher-order function that caches results.
# (We'll revisit this on Day 13 as a decorator.)
#
# memoize(fib)(n) should compute Fibonacci but cache results.

def memoize(func: Callable[..., int]) -> Callable[..., int]:
    """Return a memoized version of func using a closure cache."""
    cache: dict[tuple[object, ...], int] = {}

    def wrapper(*args: object) -> int:
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper


def slow_fib(n: int) -> int:
    """Recursive Fibonacci — exponential without memoisation."""
    if n <= 1:
        return n
    return slow_fib(n - 1) + slow_fib(n - 2)


# ---------------------------------------------------------------------------
# Exercise 5: Partial Application
# ---------------------------------------------------------------------------
# Without using functools.partial, write your own `partial(func, *bound_args, **bound_kwargs)`
# that returns a function with those arguments pre-filled.
#
# Then use it to create:
#   - multiply_by_3: multiply(x, 3) with 3 pre-filled
#   - greet_formally: greet(title="Dr.", greeting="Good day")

def my_partial(
    func: Callable[..., int], *bound_args: object, **bound_kwargs: object
) -> Callable[..., int]:
    """Return func with some args pre-filled (closure-based partial)."""
    def wrapper(*args: object, **kwargs: object) -> int:
        return func(*bound_args, *args, **bound_kwargs, **kwargs)
    return wrapper


def multiply(x: int, y: int) -> int:
    """Return x * y."""
    return x * y


if __name__ == "__main__":
    print(log("started", "server"))
    print(log("error", "not found", level="ERROR", sep=" | "))

    c = make_counter()
    c["increment"]()
    c["increment"]()
    print(c["value"]())   # 2
    c["reset"]()
    print(c["value"]())   # 0

    add1 = lambda x: x + 1
    times2 = lambda x: x * 2
    sq = lambda x: x ** 2
    f = compose(add1, times2, sq)   # add1(times2(sq(3))) = add1(times2(9)) = add1(18) = 19
    print(f(3))   # 19

    g = pipe(sq, times2, add1)       # add1(times2(sq(3))) = same = 19
    print(g(3))   # 19

    memo_fib = memoize(slow_fib)
    print(memo_fib(10))   # 55

    mul3 = my_partial(multiply, 3)
    print(mul3(7))   # 21
