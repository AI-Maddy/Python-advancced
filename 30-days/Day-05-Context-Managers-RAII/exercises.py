"""
Day 05 — Exercises: Context Managers and RAII
"""
from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Generator


# Exercise 1: DatabaseTransaction — commit/rollback on exception
class DatabaseTransaction:
    # TODO
    pass


# Exercise 2: Timer — record elapsed time
class Timer:
    # TODO
    pass


# Exercise 3: suppress_errors — generator-based, collects caught exceptions
@contextmanager
def suppress_errors(*exc_types: type[BaseException]) -> Generator[list[BaseException], None, None]:
    # TODO
    yield []


# Exercise 4: temp_environ — temporarily set env vars, restore on exit
@contextmanager
def temp_environ(**env_vars: str) -> Generator[None, None, None]:
    # TODO
    yield


if __name__ == "__main__":
    with DatabaseTransaction("db") as tx:
        pass
