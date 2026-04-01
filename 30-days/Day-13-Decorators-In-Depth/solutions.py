"""Day 13 — Solutions: Decorators In Depth"""
from __future__ import annotations

import functools
import time
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
T = TypeVar("T")


def retry(max_attempts: int = 3, delay: float = 0.0,
          exceptions: tuple[type[Exception], ...] = (Exception,)) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Parameterised decorator: retry on failure."""
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


def timer(func: Callable[P, T]) -> Callable[P, T]:
    """Decorator: prints elapsed time."""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[Timer] {func.__name__}: {elapsed*1000:.2f}ms")
        return result
    return wrapper


def memoize(func: Callable[P, T]) -> Callable[P, T]:
    """Decorator: cache results."""
    cache: dict[tuple[object, ...], T] = {}

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        key = args + tuple(sorted(kwargs.items()))  # type: ignore[operator]
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    wrapper.cache = cache  # type: ignore[attr-defined]
    return wrapper


def validate_args(**validators: Callable[[object], bool]) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Parameterised decorator: validate keyword arguments."""
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


def singleton(cls: type) -> type:
    """Class decorator: ensure only one instance exists."""
    instances: dict[type, object] = {}

    @functools.wraps(cls, updated=[])
    class Wrapper:
        def __new__(cls_inner: type) -> object:  # type: ignore[misc]
            if cls not in instances:
                instances[cls] = object.__new__(cls)
            return instances[cls]

    # Better: use a wrapper function
    _instance: list[object] = []

    def get_instance(*args: object, **kwargs: object) -> object:
        if not _instance:
            _instance.append(cls(*args, **kwargs))
        return _instance[0]

    get_instance._instance = _instance  # type: ignore[attr-defined]
    return get_instance  # type: ignore[return-value]


if __name__ == "__main__":
    # retry
    call_count = [0]

    @retry(max_attempts=3, exceptions=(ValueError,))
    def flaky() -> str:
        call_count[0] += 1
        if call_count[0] < 3:
            raise ValueError("not yet")
        return "ok"

    print(flaky())     # ok
    print(call_count)  # 3

    # memoize
    @memoize
    def fib(n: int) -> int:
        if n <= 1: return n
        return fib(n-1) + fib(n-2)

    print(fib(30))   # 832040

    # timer
    @timer
    def slow(n: int) -> int:
        return sum(range(n))

    print(slow(100000))

    # validate_args
    @validate_args(age=lambda x: isinstance(x, int) and x >= 0)
    def create_user(name: str, age: int) -> dict[str, object]:
        return {"name": name, "age": age}

    print(create_user(name="Alice", age=30))
    try:
        create_user(name="Bob", age=-1)
    except ValueError as e:
        print(e)
