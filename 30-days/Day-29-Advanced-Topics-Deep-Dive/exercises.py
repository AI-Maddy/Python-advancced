"""
Day 29 — Exercises: Advanced Topics Deep Dive
===============================================
"""
from __future__ import annotations

import copy
import pickle
import weakref
from collections import ChainMap, Counter
from enum import Enum, Flag, auto
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Exercise 1 — Cache with weak refs
# ---------------------------------------------------------------------------
# TODO: Implement WeakCache that:
#   - Stores objects by key using WeakValueDictionary
#   - get(key) returns the object or None if GC'd
#   - set(key, value) stores the object
#   - Verify that after del + gc.collect(), get() returns None

class WeakCache:
    """TODO: Cache that doesn't prevent garbage collection."""

    def __init__(self) -> None:
        # TODO: use weakref.WeakValueDictionary
        ...

    def set(self, key: str, value: Any) -> None:
        """TODO: store value."""
        ...

    def get(self, key: str) -> Any | None:
        """TODO: retrieve value or None."""
        ...
        return None


def exercise1_weak_cache() -> tuple[bool, bool]:
    """Return (found_before_del, found_after_del). Expected: (True, False)."""
    import gc
    cache = WeakCache()

    class Obj:
        pass

    obj = Obj()
    cache.set("item", obj)
    found_before = cache.get("item") is not None
    del obj
    gc.collect()
    found_after = cache.get("item") is not None
    return (found_before, found_after)


# ---------------------------------------------------------------------------
# Exercise 2 — Custom Enum with methods
# ---------------------------------------------------------------------------
# TODO: Implement Planet(Enum) with:
#   - members: MERCURY, VENUS, EARTH, MARS
#   - Each member has (mass_kg: float, radius_m: float) as value (tuple)
#   - surface_gravity() → GM/r^2 (G = 6.674e-11)
#   - weight_on(body_weight_n: float) → body_weight_n * (gravity / earth_gravity)

class Planet(Enum):
    """TODO: Planet enum with physics methods."""
    MERCURY = (3.303e+23, 2.4397e6)
    VENUS   = (4.869e+24, 6.0518e6)
    EARTH   = (5.976e+24, 6.37814e6)
    MARS    = (6.421e+23, 3.3972e6)

    def __init__(self, mass: float, radius: float) -> None:
        # TODO: store mass and radius
        ...

    def surface_gravity(self) -> float:
        """TODO: return G * mass / radius^2."""
        ...
        return 0.0

    def weight_on(self, body_weight_n: float) -> float:
        """TODO: scale weight by ratio of surface gravities."""
        ...
        return 0.0


def exercise2_planet_enum() -> tuple[float, float]:
    """Return (earth_gravity, weight_75kg_on_mars). Expected: (~9.8, ~28.3)."""
    # TODO
    ...
    return (0.0, 0.0)


# ---------------------------------------------------------------------------
# Exercise 3 — ChainMap config system
# ---------------------------------------------------------------------------
# TODO: Build a 3-layer config system:
#   Layer 1 (highest priority): CLI args
#   Layer 2: Environment variables
#   Layer 3 (lowest): Defaults
# Use ChainMap.  Demonstrate that CLI overrides env, env overrides defaults.

def exercise3_chainmap_config() -> dict[str, str]:
    """
    Return the merged config dict.
    CLI overrides env; env overrides defaults.
    """
    defaults = {"debug": "false", "host": "localhost", "port": "8080"}
    env_vars = {"port": "9090", "host": "staging.example.com"}
    cli_args = {"debug": "true"}

    # TODO: use ChainMap
    ...
    return {}


# ---------------------------------------------------------------------------
# Exercise 4 — Pickle-safe class
# ---------------------------------------------------------------------------
# TODO: Implement Config that:
#   - Has public fields: name, value
#   - Has a non-picklable _connection (a threading.Lock — can't be pickled)
#   - Implements __getstate__/__setstate__ to exclude _connection
#   - After unpickling, _connection is re-created as a new Lock

import threading

class Config:
    """TODO: pickle-safe class with non-picklable field."""

    def __init__(self, name: str, value: str) -> None:
        self.name = name
        self.value = value
        self._connection = threading.Lock()   # non-picklable on some platforms

    def __getstate__(self) -> dict[str, Any]:
        """TODO: exclude _connection."""
        ...
        return {}

    def __setstate__(self, state: dict[str, Any]) -> None:
        """TODO: restore and re-create _connection."""
        ...


def exercise4_pickle_safe() -> tuple[str, str, bool]:
    """
    Return (name_after_pickle, value_after_pickle, has_connection).
    Expected: ('test', '42', True)
    """
    # TODO
    ...
    return ("", "", False)


# ---------------------------------------------------------------------------
# Exercise 5 — __deepcopy__ with cycle prevention
# ---------------------------------------------------------------------------
# TODO: Implement a Graph with Node objects.
#       Node has: value (int), neighbors (list[Node]).
#       Implement __deepcopy__ with memo dict to avoid infinite recursion
#       on circular graphs.

class GraphNode:
    """TODO: graph node with custom deepcopy."""

    def __init__(self, value: int) -> None:
        self.value = value
        self.neighbors: list[GraphNode] = []

    def __deepcopy__(self, memo: dict[int, Any]) -> GraphNode:
        """TODO: deep copy with cycle prevention using memo."""
        ...
        return GraphNode(self.value)   # placeholder


def exercise5_deepcopy_graph() -> tuple[bool, bool]:
    """
    Return (deep_copy_is_different_object, values_preserved).
    Create a cycle: n1 → n2 → n1, deep copy it.
    """
    # TODO
    ...
    return (False, False)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Exercise 1:", exercise1_weak_cache())
    print("Exercise 2:", exercise2_planet_enum())
    print("Exercise 3:", exercise3_chainmap_config())
    print("Exercise 4:", exercise4_pickle_safe())
    print("Exercise 5:", exercise5_deepcopy_graph())
