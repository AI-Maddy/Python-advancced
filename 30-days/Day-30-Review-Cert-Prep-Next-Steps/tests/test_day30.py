"""
Tests for Day 30 — Review: Key OOP Concepts
Run with: pytest tests/test_day30.py -v

These tests serve as a final review — each test checks one fundamental OOP
concept from the 30-day course.
"""
from __future__ import annotations

import asyncio
import copy
import functools
import itertools
import math
import operator
import pickle
import sys
import weakref
from abc import ABC, abstractmethod
from collections import Counter, deque
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, auto
from pathlib import Path
from typing import Any, ClassVar, Protocol

import pytest


# ---------------------------------------------------------------------------
# Day 16: import / __all__
# ---------------------------------------------------------------------------

def test_importlib_can_load_json() -> None:
    import importlib
    json = importlib.import_module("json")
    assert json.dumps({"key": 1}) == '{"key": 1}'


# ---------------------------------------------------------------------------
# Day 17: Strategy, Observer, Registry
# ---------------------------------------------------------------------------

def test_strategy_callable() -> None:
    sorter = lambda data, key=sorted: key(data)
    assert sorter([3, 1, 2]) == [1, 2, 3]
    assert sorter([3, 1, 2], key=lambda d: sorted(d, reverse=True)) == [3, 2, 1]


def test_observer_list_of_callables() -> None:
    log: list[int] = []
    listeners = [lambda x: log.append(x), lambda x: log.append(x * 2)]
    for fn in listeners:
        fn(5)
    assert log == [5, 10]


# ---------------------------------------------------------------------------
# Day 18: SOLID
# ---------------------------------------------------------------------------

class Saver(Protocol):
    def save(self, data: str) -> None: ...


class FileSaver:
    def save(self, data: str) -> None:
        pass   # no I/O in test


class Service:
    def __init__(self, saver: Saver) -> None:
        self._saver = saver

    def run(self, payload: str) -> None:
        self._saver.save(payload)


def test_dependency_inversion() -> None:
    svc = Service(FileSaver())
    svc.run("data")   # no assertion needed; just verifying no TypeError


# ---------------------------------------------------------------------------
# Day 19: pytest fixtures, parametrize, raises
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("a,b,expected", [(1, 2, 3), (0, 0, 0), (-1, 1, 0)])
def test_add_parametrize(a: int, b: int, expected: int) -> None:
    assert a + b == expected


def test_raises_key_error() -> None:
    with pytest.raises(KeyError):
        {}["missing"]


def test_approx_float() -> None:
    assert 0.1 + 0.2 == pytest.approx(0.3)


# ---------------------------------------------------------------------------
# Day 20: Metaclasses
# ---------------------------------------------------------------------------

class SingletonMeta(type):
    _instances: ClassVar[dict[type, Any]] = {}
    def __call__(cls, *a: Any, **kw: Any) -> Any:
        if cls not in SingletonMeta._instances:
            SingletonMeta._instances[cls] = super().__call__(*a, **kw)
        return SingletonMeta._instances[cls]


class MySingleton(metaclass=SingletonMeta):
    pass


def test_singleton_same_instance() -> None:
    SingletonMeta._instances.clear()
    a = MySingleton()
    b = MySingleton()
    assert a is b


# ---------------------------------------------------------------------------
# Day 21: functools, itertools
# ---------------------------------------------------------------------------

def test_lru_cache() -> None:
    @functools.lru_cache(maxsize=4)
    def fib(n: int) -> int:
        return n if n < 2 else fib(n-1) + fib(n-2)
    assert fib(10) == 55


def test_accumulate() -> None:
    result = list(itertools.accumulate([1, 2, 3, 4]))
    assert result == [1, 3, 6, 10]


def test_compose() -> None:
    compose = lambda *fns: functools.reduce(lambda f, g: lambda x: f(g(x)), fns)
    pipeline = compose(str.upper, str.strip)
    assert pipeline("  hello  ") == "HELLO"


# ---------------------------------------------------------------------------
# Day 22: __slots__, timeit
# ---------------------------------------------------------------------------

class Slotted:
    __slots__ = ("x", "y")
    def __init__(self, x: int, y: int) -> None:
        self.x = x; self.y = y


class Regular:
    def __init__(self, x: int, y: int) -> None:
        self.x = x; self.y = y


def test_slots_no_dict() -> None:
    assert not hasattr(Slotted(1, 2), "__dict__")
    assert hasattr(Regular(1, 2), "__dict__")


def test_slots_smaller() -> None:
    r, s = Regular(1, 2), Slotted(1, 2)
    # __slots__ eliminates __dict__; total memory is smaller
    r_total = sys.getsizeof(r) + sys.getsizeof(r.__dict__)
    s_total = sys.getsizeof(s)
    assert s_total < r_total


# ---------------------------------------------------------------------------
# Day 23: asyncio
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_gather_concurrent() -> None:
    results = await asyncio.gather(
        asyncio.sleep(0, result=1),
        asyncio.sleep(0, result=2),
        asyncio.sleep(0, result=3),
    )
    assert list(results) == [1, 2, 3]


# ---------------------------------------------------------------------------
# Day 24: Decimal for money
# ---------------------------------------------------------------------------

def test_decimal_precision() -> None:
    a = Decimal("0.10")
    b = Decimal("0.20")
    assert a + b == Decimal("0.30")   # no float rounding error


def test_frozen_dataclass_immutable() -> None:
    @dataclass(frozen=True)
    class Money:
        amount: Decimal
        currency: str

    m = Money(Decimal("9.99"), "USD")
    with pytest.raises(Exception):
        m.amount = Decimal("10.00")  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Day 25: Visitor pattern
# ---------------------------------------------------------------------------

class Shape(ABC):
    @abstractmethod
    def accept(self, visitor: Any) -> Any: ...


@dataclass
class Rect(Shape):
    w: float; h: float
    def accept(self, visitor: Any) -> Any:
        return visitor.visit_rect(self)


class AreaVisitor:
    def visit_rect(self, r: Rect) -> float:
        return r.w * r.h


def test_visitor_dispatch() -> None:
    r = Rect(3, 4)
    assert r.accept(AreaVisitor()) == 12.0


# ---------------------------------------------------------------------------
# Day 26: ECS / state machine
# ---------------------------------------------------------------------------

class State(Enum):
    IDLE    = auto()
    RUNNING = auto()
    DEAD    = auto()


TRANSITIONS = {State.IDLE: {State.RUNNING}, State.RUNNING: {State.DEAD}, State.DEAD: set()}


def test_state_machine() -> None:
    state = State.IDLE
    assert State.RUNNING in TRANSITIONS[state]
    state = State.RUNNING
    assert State.DEAD in TRANSITIONS[state]
    state = State.DEAD
    assert len(TRANSITIONS[state]) == 0


# ---------------------------------------------------------------------------
# Day 27: Refactoring
# ---------------------------------------------------------------------------

def test_extract_method_pattern() -> None:
    def compute_subtotal(items: list[dict]) -> float:
        return sum(i["price"] * i["qty"] for i in items)

    items = [{"price": 10.0, "qty": 3}, {"price": 5.0, "qty": 2}]
    assert compute_subtotal(items) == 40.0


# ---------------------------------------------------------------------------
# Day 28: Common pitfalls
# ---------------------------------------------------------------------------

def test_mutable_default_fixed() -> None:
    def fn(lst: list[int] | None = None) -> list[int]:
        if lst is None:
            lst = []
        lst.append(1)
        return lst

    r1 = fn()
    r2 = fn()
    assert r1 is not r2


def test_late_binding_fixed() -> None:
    fns = [lambda i=i: i for i in range(5)]
    assert [f() for f in fns] == [0, 1, 2, 3, 4]


def test_equality_not_identity() -> None:
    s = "hel" + "lo"
    assert s == "hello"


# ---------------------------------------------------------------------------
# Day 29: Advanced topics
# ---------------------------------------------------------------------------

def test_weakref_cleans_up() -> None:
    class Obj: pass
    obj = Obj()
    ref = weakref.ref(obj)
    del obj
    import gc; gc.collect()
    assert ref() is None


def test_pickle_round_trip() -> None:
    data = {"key": [1, 2, 3], "nested": {"a": True}}
    assert pickle.loads(pickle.dumps(data)) == data


def test_deepcopy_independence() -> None:
    lst = [[1, 2], [3, 4]]
    copy_lst = copy.deepcopy(lst)
    copy_lst[0].append(99)
    assert lst[0] == [1, 2]   # original unaffected


def test_pathlib_write_read(tmp_path: Path) -> None:
    f = tmp_path / "test.txt"
    f.write_text("hello")
    assert f.read_text() == "hello"
    assert f.name == "test.txt"
