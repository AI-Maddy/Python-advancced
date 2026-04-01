"""Day 11 — Exercises: Generic OOP Design"""
from __future__ import annotations
from typing import Generic, TypeVar
T = TypeVar("T")
ID = TypeVar("ID")

# Ex 1: Generic Repository[T, ID] with save, find_by_id, find_all, delete, count
class Repository(Generic[T, ID]):
    pass  # TODO

# Ex 2: Ok[T] and Err[E] Result types with is_ok, is_err, unwrap, map
class Ok(Generic[T]):
    pass  # TODO

class Err(Generic[T]):
    pass  # TODO

# Ex 3: safe_divide and safe_parse_int returning Ok/Err
def safe_divide(a: float, b: float) -> "Ok[float] | Err[Exception]":
    pass  # TODO

def safe_parse_int(s: str) -> "Ok[int] | Err[Exception]":
    pass  # TODO

if __name__ == "__main__":
    repo: Repository[str, int] = Repository()  # type: ignore
