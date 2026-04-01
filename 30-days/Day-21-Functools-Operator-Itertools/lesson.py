"""
Day 21 — functools, operator & itertools
==========================================
Topics:
  - functools: reduce, partial, lru_cache, cache, cached_property,
               total_ordering, singledispatch
  - operator: attrgetter, itemgetter, methodcaller
  - itertools: chain, islice, count, cycle, groupby, product,
               combinations, accumulate, takewhile, dropwhile
  - Functional pipeline with reduce + operator
"""
from __future__ import annotations

import functools
import itertools
import operator
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from typing import Any, TypeVar

T = TypeVar("T")

# ===========================================================================
# 1. functools
# ===========================================================================

# --- reduce ---
from functools import reduce

def demo_reduce() -> None:
    """reduce(f, iterable) applies f cumulatively."""
    total = reduce(operator.add, [1, 2, 3, 4, 5])       # 15
    product = reduce(operator.mul, [1, 2, 3, 4, 5], 1)  # 120
    print(f"Sum via reduce:     {total}")
    print(f"Product via reduce: {product}")


# --- partial ---
from functools import partial

def power(base: float, exponent: float) -> float:
    """Return base raised to exponent."""
    return base ** exponent

square = partial(power, exponent=2)
cube   = partial(power, exponent=3)

def demo_partial() -> None:
    print(f"square(5) = {square(5)}")  # 25
    print(f"cube(3)   = {cube(3)}")    # 27


# --- lru_cache & cache ---
from functools import lru_cache, cache

@lru_cache(maxsize=128)
def fibonacci_lru(n: int) -> int:
    """Classic fibonacci with LRU cache (Python 3.8+)."""
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

@cache   # unbounded cache — Python 3.9+
def fibonacci_cache(n: int) -> int:
    """Fibonacci with unbounded cache."""
    if n < 2:
        return n
    return fibonacci_cache(n - 1) + fibonacci_cache(n - 2)

def demo_lru_cache() -> None:
    print(f"fib(30) = {fibonacci_lru(30)}")
    print(f"cache info: {fibonacci_lru.cache_info()}")


# --- cached_property ---
from functools import cached_property

class Circle:
    """Circle whose area is computed once and then cached."""

    def __init__(self, radius: float) -> None:
        self.radius = radius

    @cached_property
    def area(self) -> float:
        """Computed only on first access."""
        import math
        print(f"  computing area for radius={self.radius}")
        return math.pi * self.radius ** 2


# --- total_ordering ---
from functools import total_ordering

@total_ordering
@dataclass
class Version:
    """
    Semantic version — only __eq__ and __lt__ needed; total_ordering
    fills in >, >=, <=.
    """
    major: int
    minor: int
    patch: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

    def __hash__(self) -> int:
        return hash((self.major, self.minor, self.patch))


# --- singledispatch ---
from functools import singledispatch

@singledispatch
def process(value: Any) -> str:
    """Default handler for unregistered types."""
    return f"Unknown type: {type(value).__name__}"

@process.register(int)
def _(value: int) -> str:
    return f"Integer: {value * 2}"

@process.register(str)
def _(value: str) -> str:
    return f"String: {value.upper()}"

@process.register(list)
def _(value: list[Any]) -> str:
    return f"List of {len(value)} items"


# ===========================================================================
# 2. operator module
# ===========================================================================

@dataclass
class Employee:
    name: str
    department: str
    salary: float

    def greet(self) -> str:
        return f"Hi, I'm {self.name}"


def demo_operator() -> None:
    employees = [
        Employee("Alice", "Engineering", 95_000),
        Employee("Bob",   "Marketing",   72_000),
        Employee("Carol", "Engineering", 105_000),
        Employee("Dave",  "Marketing",   68_000),
    ]

    # attrgetter — like a lambda but faster and more readable
    by_salary = sorted(employees, key=operator.attrgetter("salary"))
    print("By salary:", [e.name for e in by_salary])

    # itemgetter — for tuples/dicts
    records = [("Alice", 95), ("Bob", 72), ("Carol", 105)]
    by_score = sorted(records, key=operator.itemgetter(1), reverse=True)
    print("By score:", by_score)

    # methodcaller
    greet_all = list(map(operator.methodcaller("greet"), employees[:2]))
    print("Greetings:", greet_all)


# ===========================================================================
# 3. itertools
# ===========================================================================

def demo_itertools() -> None:
    # chain — flatten nested iterables
    flat = list(itertools.chain([1, 2], [3, 4], [5]))
    print("chain:", flat)

    # islice — lazy slicing
    first5 = list(itertools.islice(itertools.count(10), 5))  # [10,11,12,13,14]
    print("islice(count(10), 5):", first5)

    # cycle — repeat sequence forever
    colours = list(itertools.islice(itertools.cycle(["R", "G", "B"]), 7))
    print("cycle:", colours)

    # groupby — group consecutive items (data must be sorted by key first!)
    data = sorted([
        {"dept": "Eng", "name": "Alice"},
        {"dept": "Eng", "name": "Carol"},
        {"dept": "Mkt", "name": "Bob"},
    ], key=operator.itemgetter("dept"))
    groups = {k: [e["name"] for e in g]
              for k, g in itertools.groupby(data, key=operator.itemgetter("dept"))}
    print("groupby:", groups)

    # product — cartesian product
    suits = ["♠", "♥"]
    ranks = ["A", "K"]
    cards = list(itertools.product(ranks, suits))
    print("product:", cards)

    # combinations
    combos = list(itertools.combinations("ABCD", 2))
    print(f"combinations(ABCD, 2): {len(combos)} combos")

    # accumulate — running totals
    sales = [100, 200, 150, 300]
    running = list(itertools.accumulate(sales))
    print("accumulate:", running)

    # takewhile / dropwhile
    nums = [1, 3, 5, 2, 7, 9]
    taken   = list(itertools.takewhile(lambda x: x % 2 != 0, nums))
    dropped = list(itertools.dropwhile(lambda x: x % 2 != 0, nums))
    print("takewhile odd:", taken)
    print("dropwhile odd:", dropped)


# ===========================================================================
# 4. Functional pipeline with reduce + operator
# ===========================================================================

def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    Return a function that applies funcs right-to-left (mathematical composition).
    compose(f, g)(x) == f(g(x))
    """
    return reduce(lambda f, g: lambda x: f(g(x)), funcs)


def demo_pipeline() -> None:
    """Build a functional pipeline."""
    pipeline = compose(
        lambda s: s.strip(),
        lambda s: s.replace(",", ""),
        str.lower,
    )
    result = pipeline("  Hello, World  ")
    print(f"Pipeline result: {result!r}")

    # Operator-based pipeline on numbers
    double_then_add10 = compose(
        partial(operator.add, 10),
        partial(operator.mul, 2),
    )
    print(f"double_then_add10(5) = {double_then_add10(5)}")


# ===========================================================================
# Main demo
# ===========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 21 — functools, operator & itertools")
    print("=" * 60)

    print("\n--- reduce ---")
    demo_reduce()

    print("\n--- partial ---")
    demo_partial()

    print("\n--- lru_cache ---")
    demo_lru_cache()

    print("\n--- cached_property ---")
    c = Circle(5)
    print(f"area (first): {c.area:.4f}")
    print(f"area (cached): {c.area:.4f}")

    print("\n--- total_ordering ---")
    v1 = Version(1, 2, 0)
    v2 = Version(1, 3, 0)
    print(f"v1 < v2: {v1 < v2}")
    print(f"v2 > v1: {v2 > v1}")
    print(f"v1 <= v2: {v1 <= v2}")

    print("\n--- singledispatch ---")
    for val in (42, "hello", [1, 2, 3], 3.14):
        print(f"  process({val!r}) → {process(val)}")

    print("\n--- operator ---")
    demo_operator()

    print("\n--- itertools ---")
    demo_itertools()

    print("\n--- Functional pipeline ---")
    demo_pipeline()
