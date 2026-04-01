"""
Example 1 — Timing and rate-limiting decorators.
"""
from __future__ import annotations

import functools
import time
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def timer(func: F) -> F:
    """Measure and print execution time."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIMER] {func.__name__} took {elapsed:.6f}s")
        return result
    return wrapper  # type: ignore[return-value]


def throttle(min_interval: float) -> Callable[[F], F]:
    """Decorator factory: ensure at least min_interval seconds between calls."""
    def decorator(func: F) -> F:
        last_called: list[float] = [0.0]

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            now = time.perf_counter()
            elapsed = now - last_called[0]
            if elapsed < min_interval:
                wait = min_interval - elapsed
                print(f"[THROTTLE] {func.__name__}: waiting {wait:.3f}s")
                time.sleep(wait)
            last_called[0] = time.perf_counter()
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]
    return decorator


@timer
def compute_sum(n: int) -> int:
    return sum(range(n))


def main() -> None:
    result = compute_sum(1_000_000)
    print(f"Sum: {result}")

    # Verify wraps preserved metadata
    print(f"__name__: {compute_sum.__name__}")
    print(f"__wrapped__: {compute_sum.__wrapped__.__name__}")  # type: ignore[attr-defined]


if __name__ == "__main__":
    main()
