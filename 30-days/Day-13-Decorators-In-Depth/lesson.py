"""
Day 13 — Decorators In Depth
==============================

Topics:
  - Decorator anatomy: @functools.wraps
  - Parameterized decorators (decorator factories)
  - Class-based decorators
  - Stacking multiple decorators
  - @functools.lru_cache, @functools.cache, @functools.cached_property
  - Real examples: @retry, @timer, @validate_args, @singleton
"""
from __future__ import annotations

import functools
import time
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
T = TypeVar("T")


# ---------------------------------------------------------------------------
# 1. Decorator Anatomy
# ---------------------------------------------------------------------------

def simple_decorator(func: Callable[P, T]) -> Callable[P, T]:
    """Basic decorator without functools.wraps — loses metadata."""
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print(f"Before {func.__name__}")
        result = func(*args, **kwargs)
        print(f"After {func.__name__}")
        return result
    return wrapper


def good_decorator(func: Callable[P, T]) -> Callable[P, T]:
    """Decorator WITH functools.wraps — preserves metadata."""
    @functools.wraps(func)    # copies __name__, __doc__, __annotations__, etc.
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print(f"Before {func.__name__}")
        result = func(*args, **kwargs)
        print(f"After {func.__name__}")
        return result
    return wrapper


@good_decorator
def my_function() -> str:
    """My function's docstring."""
    return "hello"


# ---------------------------------------------------------------------------
# 2. Parameterised Decorators (Decorator Factories)
# ---------------------------------------------------------------------------

def repeat(n: int) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator factory: call function n times."""
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            result: T = func(*args, **kwargs)  # type: ignore[assignment]
            for _ in range(n - 1):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@repeat(3)
def say_hi(name: str) -> str:
    print(f"Hi, {name}!")
    return f"Hi, {name}!"


# ---------------------------------------------------------------------------
# 3. functools.lru_cache and cache
# ---------------------------------------------------------------------------

@functools.lru_cache(maxsize=128)
def fib_cached(n: int) -> int:
    """Fibonacci with LRU cache."""
    if n <= 1:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)


@functools.cache  # Python 3.9+, unbounded cache (same as lru_cache(maxsize=None))
def fib_unbounded(n: int) -> int:
    if n <= 1:
        return n
    return fib_unbounded(n - 1) + fib_unbounded(n - 2)


# ---------------------------------------------------------------------------
# 4. cached_property
# ---------------------------------------------------------------------------

class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius

    @functools.cached_property
    def area(self) -> float:
        """Computed once and cached as an instance attribute."""
        import math
        print("[Computing area...]")
        return math.pi * self.radius ** 2


# ---------------------------------------------------------------------------
# 5. Class-based Decorator
# ---------------------------------------------------------------------------

class CallCounter:
    """Class-based decorator that counts calls."""

    def __init__(self, func: Callable[..., T]) -> None:
        functools.update_wrapper(self, func)
        self._func = func
        self.call_count = 0

    def __call__(self, *args: object, **kwargs: object) -> T:
        self.call_count += 1
        return self._func(*args, **kwargs)

    def reset(self) -> None:
        self.call_count = 0


@CallCounter
def process(data: str) -> str:
    return data.upper()


# ---------------------------------------------------------------------------
# 6. Stacking Decorators
# ---------------------------------------------------------------------------
# Decorators apply bottom-up (closest to function applied first)

from solutions import retry, timer, memoize, validate_args


@timer
@memoize
def slow_sqrt(n: int) -> float:
    import math
    time.sleep(0.001)
    return math.sqrt(n)


if __name__ == "__main__":
    print("=== functools.wraps ===")
    print(my_function.__name__)   # my_function (not 'wrapper')
    print(my_function.__doc__)    # My function's docstring.

    print("\n=== repeat(3) ===")
    say_hi("Alice")

    print("\n=== lru_cache ===")
    start = time.perf_counter()
    fib_cached(35)
    elapsed1 = time.perf_counter() - start
    start = time.perf_counter()
    fib_cached(35)
    elapsed2 = time.perf_counter() - start
    print(f"First call: {elapsed1*1000:.2f}ms, Cached: {elapsed2*1000:.2f}ms")
    print(fib_cached.cache_info())

    print("\n=== cached_property ===")
    c = Circle(5.0)
    _ = c.area   # computed
    _ = c.area   # from cache (no print)

    print("\n=== Class-based decorator ===")
    print(process("hello"))
    print(process("world"))
    print(f"Called {process.call_count} times")

    print("\n=== Stacked decorators ===")
    slow_sqrt(16)   # computed + timed
    slow_sqrt(16)   # from memoize cache (no sleep)
