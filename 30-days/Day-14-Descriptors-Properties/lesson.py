"""
Day 14 — Descriptors and Properties
======================================

Topics:
  - Descriptor protocol: __get__, __set__, __delete__, __set_name__
  - Data descriptor vs non-data descriptor
  - property is a descriptor
  - Validated descriptor for type checking
  - Clamped descriptor for range enforcement
  - classmethod and staticmethod are descriptors
  - Lazy computed attributes
"""
from __future__ import annotations

from typing import Any, TypeVar

T = TypeVar("T")


# ---------------------------------------------------------------------------
# 1. The Descriptor Protocol
# ---------------------------------------------------------------------------
# A descriptor is an object attribute with "binding behaviour" —
# one whose attribute access has been overridden by methods in the
# descriptor protocol: __get__, __set__, __delete__, __set_name__.
#
# Data descriptor:     defines __set__ or __delete__ (takes priority over instance dict)
# Non-data descriptor: only __get__ (instance dict takes priority)
#
# C++ analogy: descriptor ≈ smart member variable with custom get/set logic


class Verbose:
    """Data descriptor: logs all gets and sets."""

    def __set_name__(self, owner: type, name: str) -> None:
        """Called when the descriptor is assigned to a class attribute.
        name is the attribute name in the class body.
        """
        self._name = name
        print(f"[Verbose] Descriptor {name!r} attached to {owner.__name__}")

    def __get__(self, obj: object | None, objtype: type) -> Any:
        if obj is None:
            return self   # accessed on the class
        value = obj.__dict__.get(self._name, "<unset>")
        print(f"[Get] {self._name} = {value!r}")
        return value

    def __set__(self, obj: object, value: Any) -> None:
        print(f"[Set] {self._name} = {value!r}")
        obj.__dict__[self._name] = value

    def __delete__(self, obj: object) -> None:
        print(f"[Del] {self._name}")
        obj.__dict__.pop(self._name, None)


class Demo:
    x = Verbose()
    y = Verbose()


# ---------------------------------------------------------------------------
# 2. property as a descriptor
# ---------------------------------------------------------------------------
# property is a built-in descriptor. These are equivalent:
#
#   @property
#   def radius(self): return self._radius
#
#   radius = property(fget=lambda self: self._radius)

import math

class Circle:
    def __init__(self, radius: float) -> None:
        self._radius = radius

    # property is just syntactic sugar for a descriptor
    radius = property(
        fget=lambda self: self._radius,
        fset=lambda self, v: setattr(self, '_radius', max(0.0, v)),
        doc="Radius (non-negative)"
    )

    @property
    def area(self) -> float:
        return math.pi * self._radius ** 2


# ---------------------------------------------------------------------------
# 3. From solutions.py — real descriptor examples
# ---------------------------------------------------------------------------

from solutions import TypedAttribute, Clamped, LazyProperty


class Config:
    """Uses TypedAttribute descriptor for type safety."""
    host = TypedAttribute(str)
    port = TypedAttribute(int)
    debug = TypedAttribute(bool)

    def __init__(self, host: str, port: int, debug: bool = False) -> None:
        self.host = host
        self.port = port
        self.debug = debug


class AudioPlayer:
    """Uses Clamped descriptor to keep volume in [0.0, 1.0]."""
    volume = Clamped(0.0, 1.0)
    bass = Clamped(-10.0, 10.0)

    def __init__(self) -> None:
        self.volume = 0.5
        self.bass = 0.0


class DataProcessor:
    """Uses LazyProperty for one-time expensive computation."""

    def __init__(self, data: list[int]) -> None:
        self.data = data

    @LazyProperty
    def statistics(self) -> dict[str, float]:
        """Compute statistics once."""
        print("[Computing statistics...]")
        n = len(self.data)
        if n == 0:
            return {}
        mean = sum(self.data) / n
        variance = sum((x - mean) ** 2 for x in self.data) / n
        return {
            "min": float(min(self.data)),
            "max": float(max(self.data)),
            "mean": mean,
            "std": variance ** 0.5,
        }


if __name__ == "__main__":
    print("=== Verbose Descriptor ===")
    d = Demo()
    d.x = 42
    _ = d.x
    del d.x

    print("\n=== property as descriptor ===")
    c = Circle(5.0)
    print(c.radius, c.area)
    c.radius = -3.0     # clamped to 0
    print(c.radius)

    print("\n=== TypedAttribute ===")
    cfg = Config("localhost", 8080)
    print(cfg.host, cfg.port)
    try:
        cfg.port = "eight-thousand"  # type: ignore[assignment]
    except TypeError as e:
        print(f"TypeError: {e}")

    print("\n=== Clamped ===")
    player = AudioPlayer()
    player.volume = 1.5    # clamped to 1.0
    print(f"volume: {player.volume}")

    print("\n=== LazyProperty ===")
    proc = DataProcessor([1, 2, 3, 4, 5, 10, 20])
    print(proc.statistics)   # computed
    print(proc.statistics)   # from cache (no print)
