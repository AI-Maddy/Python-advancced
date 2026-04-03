"""
Day 05 — Exercises: Context Managers and RAII
"""
from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Generator


# Exercise 1: DatabaseTransaction — commit/rollback on exception
class DatabaseTransaction:
    """Context manager that commits on success and rolls back on exception."""

    def __init__(self, name: str = "db") -> None:
        self.name = name
        self.committed = False
        self.rolled_back = False
        self._ops: list[str] = []

    def execute(self, sql: str) -> None:
        self._ops.append(sql)

    def __enter__(self) -> "DatabaseTransaction":
        return self

    def __exit__(
        self,
        exc_type: type | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> bool | None:
        if exc_type is None:
            self.committed = True
        else:
            self.rolled_back = True
            self._ops.clear()
        return None   # do not suppress exceptions


# Exercise 2: Timer — record elapsed time
class Timer:
    """Records elapsed time of a with block."""

    def __init__(self) -> None:
        self.elapsed: float = 0.0
        self._start: float = 0.0

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self

    def __exit__(
        self,
        exc_type: type | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        self.elapsed = time.perf_counter() - self._start


# Exercise 3: suppress_errors — generator-based, collects caught exceptions
@contextmanager
def suppress_errors(*exc_types: type[BaseException]) -> Generator[list[BaseException], None, None]:
    """Suppress specified exception types and collect them."""
    caught: list[BaseException] = []
    try:
        yield caught
    except exc_types as e:
        caught.append(e)


# Exercise 4: temp_environ — temporarily set env vars, restore on exit
@contextmanager
def temp_environ(**env_vars: str) -> Generator[None, None, None]:
    """Temporarily set environment variables, restore on exit."""
    import os
    original = {k: os.environ.get(k) for k in env_vars}
    try:
        os.environ.update(env_vars)
        yield
    finally:
        for k, v in original.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


if __name__ == "__main__":
    with DatabaseTransaction("db") as tx:
        pass
