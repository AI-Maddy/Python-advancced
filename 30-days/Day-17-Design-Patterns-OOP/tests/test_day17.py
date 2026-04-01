"""
Tests for Day 17 — Design Patterns (OOP)
Run with: pytest tests/test_day17.py -v
"""
from __future__ import annotations
import sys as _sys
import os as _os
_day_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _day_dir)
for _m in ['solutions', 'exercises', 'lesson']:
    _sys.modules.pop(_m, None)

from collections.abc import Callable
from typing import Any, ClassVar

import pytest


# ---------------------------------------------------------------------------
# Strategy tests
# ---------------------------------------------------------------------------

class TextProcessor:
    def __init__(self, strategies: list[Callable[[str], str]]) -> None:
        self._strategies = strategies

    def process(self, text: str) -> str:
        result = text
        for s in self._strategies:
            result = s(result)
        return result


def test_strategy_single() -> None:
    proc = TextProcessor([str.upper])
    assert proc.process("hello") == "HELLO"


def test_strategy_pipeline() -> None:
    proc = TextProcessor([str.strip, str.upper, lambda s: s.replace(" ", "_")])
    assert proc.process("  hello world  ") == "HELLO_WORLD"


def test_strategy_swap() -> None:
    """Strategy can be replaced at runtime."""
    results: list[str] = []

    class Sorter:
        def __init__(self, strategy: Callable[[list[int]], list[int]]) -> None:
            self.strategy = strategy

        def sort(self, data: list[int]) -> list[int]:
            return self.strategy(data)

    s = Sorter(sorted)
    assert s.sort([3, 1, 2]) == [1, 2, 3]
    s.strategy = lambda d: sorted(d, reverse=True)
    assert s.sort([3, 1, 2]) == [3, 2, 1]


# ---------------------------------------------------------------------------
# Observer tests
# ---------------------------------------------------------------------------

class EventEmitter:
    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable]] = {}

    def on(self, event: str, fn: Callable) -> None:
        self._listeners.setdefault(event, []).append(fn)

    def off(self, event: str, fn: Callable) -> None:
        self._listeners.get(event, []).remove(fn)

    def emit(self, event: str, payload: Any = None) -> None:
        for fn in self._listeners.get(event, []):
            fn(event, payload)


def test_observer_fires() -> None:
    bus = EventEmitter()
    log: list[Any] = []
    bus.on("click", lambda e, p: log.append(p))
    bus.emit("click", 42)
    assert log == [42]


def test_observer_multiple_listeners() -> None:
    bus = EventEmitter()
    log: list[str] = []
    bus.on("msg", lambda e, p: log.append(f"A:{p}"))
    bus.on("msg", lambda e, p: log.append(f"B:{p}"))
    bus.emit("msg", "hi")
    assert log == ["A:hi", "B:hi"]


def test_observer_unregister() -> None:
    bus = EventEmitter()
    log: list[str] = []

    def handler(e: str, p: Any) -> None:
        log.append(p)

    bus.on("ev", handler)
    bus.emit("ev", "first")
    bus.off("ev", handler)
    bus.emit("ev", "second")
    assert log == ["first"]  # second not recorded


def test_observer_no_listeners_no_error() -> None:
    bus = EventEmitter()
    bus.emit("nonexistent", "payload")  # should not raise


# ---------------------------------------------------------------------------
# Null Object tests
# ---------------------------------------------------------------------------

class NullLogger:
    def log(self, msg: str) -> None:
        pass


class Logger:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def log(self, msg: str) -> None:
        self.messages.append(msg)


def test_null_logger_no_output(capsys: pytest.CaptureFixture[str]) -> None:
    nl = NullLogger()
    nl.log("should not appear")
    captured = capsys.readouterr()
    assert captured.out == ""


def test_null_logger_same_interface() -> None:
    real = Logger()
    null = NullLogger()
    for logger in (real, null):
        logger.log("test")  # both have .log() — duck typing satisfied
    assert real.messages == ["test"]


# ---------------------------------------------------------------------------
# Borg tests
# ---------------------------------------------------------------------------

class Borg:
    _shared: ClassVar[dict[str, Any]] = {}

    def __init__(self) -> None:
        self.__dict__ = self.__class__._shared


def test_borg_shared_state() -> None:
    Borg._shared.clear()  # reset for test isolation
    b1 = Borg()
    b2 = Borg()
    b1.value = 99
    assert b2.value == 99


def test_borg_different_instances() -> None:
    Borg._shared.clear()
    b1 = Borg()
    b2 = Borg()
    assert b1 is not b2
    assert b1.__dict__ is b2.__dict__


# ---------------------------------------------------------------------------
# Registry tests
# ---------------------------------------------------------------------------

class Handler:
    _registry: ClassVar[dict[str, type[Handler]]] = {}

    def __init_subclass__(cls, name: str = "", **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if name:
            Handler._registry[name] = cls

    @classmethod
    def get(cls, name: str) -> type[Handler]:
        return cls._registry[name]

    def handle(self, data: Any) -> str:
        raise NotImplementedError


class UpperHandler(Handler, name="upper"):
    def handle(self, data: Any) -> str:
        return str(data).upper()


class LowerHandler(Handler, name="lower"):
    def handle(self, data: Any) -> str:
        return str(data).lower()


def test_registry_registered() -> None:
    assert "upper" in Handler._registry
    assert "lower" in Handler._registry


def test_registry_get_and_use() -> None:
    h = Handler.get("upper")()
    assert h.handle("hello") == "HELLO"


def test_registry_missing_key() -> None:
    with pytest.raises(KeyError):
        Handler.get("nonexistent")
