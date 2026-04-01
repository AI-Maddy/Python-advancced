"""
Decorator-Function Idiom.

Demonstrates:
* @functools.wraps preserving metadata
* Parameterised decorators (decorator factories)
* Class-based decorators
* Stacking decorators (order matters)
* @functools.lru_cache, @functools.cache, @functools.cached_property
"""
from __future__ import annotations

import functools
import time
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


# ---------------------------------------------------------------------------
# 1. @functools.wraps preserving __name__, __doc__, __wrapped__
# ---------------------------------------------------------------------------
def log_calls(func: F) -> F:
    """Decorator that logs each call to the wrapped function.

    Uses @functools.wraps to preserve the original function's metadata.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"[LOG] Calling {func.__name__}{args}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} returned {result!r}")
        return result

    return wrapper  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# 2. Parameterised decorator (decorator factory)
# ---------------------------------------------------------------------------
def retry(times: int = 3, exceptions: tuple[type[BaseException], ...] = (Exception,)) -> Callable[[F], F]:
    """Decorator factory: retry ``func`` up to ``times`` times on failure.

    Args:
        times: Maximum number of attempts.
        exceptions: Exception types to catch and retry.
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exc: BaseException | None = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    print(f"  [retry] attempt {attempt}/{times} failed: {exc}")
            raise last_exc  # type: ignore[misc]

        return wrapper  # type: ignore[return-value]

    return decorator


def validate_types(**types: type) -> Callable[[F], F]:
    """Decorator factory: validate argument types at runtime.

    Example::

        @validate_types(x=int, y=float)
        def add(x, y): ...
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            sig = func.__code__.co_varnames
            for name, expected in types.items():
                idx = list(sig).index(name)
                if idx < len(args) and not isinstance(args[idx], expected):
                    raise TypeError(
                        f"Argument {name!r} must be {expected.__name__}, "
                        f"got {type(args[idx]).__name__}"
                    )
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


# ---------------------------------------------------------------------------
# 3. Class-based decorator
# ---------------------------------------------------------------------------
class CallCounter:
    """Class-based decorator that counts invocations.

    Preserves the original function's metadata via functools.update_wrapper.
    """

    def __init__(self, func: Callable[..., Any]) -> None:
        functools.update_wrapper(self, func)
        self._func = func
        self.call_count = 0

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.call_count += 1
        return self._func(*args, **kwargs)

    def reset(self) -> None:
        self.call_count = 0


# ---------------------------------------------------------------------------
# 4. Stacking decorators — order matters (outermost applied last)
# ---------------------------------------------------------------------------
def uppercase_result(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs).upper()

    return wrapper  # type: ignore[return-value]


def add_exclamation(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs) + "!"

    return wrapper  # type: ignore[return-value]


@add_exclamation
@uppercase_result
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"hello {name}"


# ---------------------------------------------------------------------------
# 5. functools.lru_cache, cache, cached_property
# ---------------------------------------------------------------------------
@functools.lru_cache(maxsize=128)
def expensive_fib(n: int) -> int:
    """Fibonacci with LRU memoisation."""
    if n < 2:
        return n
    return expensive_fib(n - 1) + expensive_fib(n - 2)


@functools.cache  # unbounded cache (Python 3.9+)
def factorial(n: int) -> int:
    """Factorial with unbounded cache."""
    return 1 if n <= 1 else n * factorial(n - 1)


class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius

    @functools.cached_property
    def area(self) -> float:
        """Computed once and cached on the instance."""
        import math
        return math.pi * self.radius ** 2


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    @log_calls
    def add(x: int, y: int) -> int:
        """Add two numbers."""
        return x + y

    print(f"__name__: {add.__name__}")  # 'add'
    print(f"__doc__: {add.__doc__}")
    result = add(3, 4)

    # Retry
    _attempt = 0

    @retry(times=3, exceptions=(ValueError,))
    def flaky() -> str:
        global _attempt
        _attempt += 1
        if _attempt < 3:
            raise ValueError(f"attempt {_attempt}")
        return "success"

    print(flaky())

    # Stacking
    print(greet("world"))  # "HELLO WORLD!"

    # CallCounter
    @CallCounter
    def square(n: int) -> int:
        return n * n

    square(3)
    square(4)
    print(f"square called {square.call_count} times")

    # LRU cache
    expensive_fib(30)
    print(f"fib(30)={expensive_fib(30)}, info={expensive_fib.cache_info()}")

    # cached_property
    c = Circle(5)
    print(f"area: {c.area:.4f}")
    print(f"cached: {c.area:.4f}")
    print(f"'area' in __dict__: {'area' in c.__dict__}")
