"""Day 13 — Exercises: Decorators"""
from __future__ import annotations
import functools, time
from typing import Callable, TypeVar, ParamSpec
P = ParamSpec("P"); T = TypeVar("T")

# Ex 1: @retry(max_attempts, delay, exceptions)
def retry(max_attempts: int=3, delay: float=0.0,
          exceptions: tuple[type[Exception],...] = (Exception,)) -> Callable[[Callable[P,T]], Callable[P,T]]:
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            last_exc: Exception = RuntimeError("no attempts made")
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if attempt < max_attempts and delay > 0:
                        time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator

# Ex 2: @timer — print elapsed time
def timer(func: Callable[P, T]) -> Callable[P, T]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[Timer] {func.__name__}: {elapsed*1000:.2f}ms")
        return result
    return wrapper

# Ex 3: @memoize — cache results
def memoize(func: Callable[P, T]) -> Callable[P, T]:
    cache: dict[tuple[object, ...], T] = {}

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        key = args + tuple(sorted(kwargs.items()))  # type: ignore[operator]
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    wrapper.cache = cache  # type: ignore[attr-defined]
    return wrapper

# Ex 4: @validate_args(**validators) — validate kwargs
def validate_args(**validators: Callable[[object], bool]) -> Callable[[Callable[P,T]], Callable[P,T]]:
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            for param_name, validator in validators.items():
                if param_name in kwargs:  # type: ignore[operator]
                    if not validator(kwargs[param_name]):  # type: ignore[index]
                        raise ValueError(
                            f"Validation failed for parameter {param_name!r}"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator

if __name__ == "__main__":
    @memoize
    def fib(n: int) -> int:
        if n <= 1: return n
        return fib(n-1) + fib(n-2)
    print(fib(20))
