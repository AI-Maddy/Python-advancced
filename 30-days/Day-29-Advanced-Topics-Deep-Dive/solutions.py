"""
Day 29 — Solutions: Advanced Topics Deep Dive
===============================================
"""
from __future__ import annotations

import copy
import gc
import pickle
import threading
import weakref
from collections import ChainMap
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Solution 1 — WeakCache
# ---------------------------------------------------------------------------

class WeakCache:
    def __init__(self) -> None:
        self._store: weakref.WeakValueDictionary[str, Any] = weakref.WeakValueDictionary()

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value

    def get(self, key: str) -> Any | None:
        return self._store.get(key)


def exercise1_weak_cache() -> tuple[bool, bool]:
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
# Solution 2 — Planet Enum
# ---------------------------------------------------------------------------

G = 6.674e-11


class Planet(Enum):
    MERCURY = (3.303e+23, 2.4397e6)
    VENUS   = (4.869e+24, 6.0518e6)
    EARTH   = (5.976e+24, 6.37814e6)
    MARS    = (6.421e+23, 3.3972e6)

    def __init__(self, mass: float, radius: float) -> None:
        self.mass = mass
        self.radius = radius

    def surface_gravity(self) -> float:
        return G * self.mass / self.radius ** 2

    def weight_on(self, body_weight_n: float) -> float:
        earth_g = Planet.EARTH.surface_gravity()
        return body_weight_n * (self.surface_gravity() / earth_g)


def exercise2_planet_enum() -> tuple[float, float]:
    earth_g = Planet.EARTH.surface_gravity()
    weight_on_mars = Planet.MARS.weight_on(75 * 9.8)   # 75 kg on Earth
    return (earth_g, weight_on_mars)


# ---------------------------------------------------------------------------
# Solution 3 — ChainMap config
# ---------------------------------------------------------------------------

def exercise3_chainmap_config() -> dict[str, str]:
    defaults = {"debug": "false", "host": "localhost", "port": "8080"}
    env_vars = {"port": "9090", "host": "staging.example.com"}
    cli_args = {"debug": "true"}
    config = ChainMap(cli_args, env_vars, defaults)
    return dict(config)


# ---------------------------------------------------------------------------
# Solution 4 — Pickle-safe class
# ---------------------------------------------------------------------------

class Config:
    def __init__(self, name: str, value: str) -> None:
        self.name = name
        self.value = value
        self._connection = threading.Lock()

    def __getstate__(self) -> dict[str, Any]:
        state = self.__dict__.copy()
        del state["_connection"]
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__dict__.update(state)
        self._connection = threading.Lock()


def exercise4_pickle_safe() -> tuple[str, str, bool]:
    cfg = Config("test", "42")
    data = pickle.dumps(cfg)
    loaded = pickle.loads(data)
    return (loaded.name, loaded.value, hasattr(loaded, "_connection"))


# ---------------------------------------------------------------------------
# Solution 5 — __deepcopy__ with cycle prevention
# ---------------------------------------------------------------------------

class GraphNode:
    def __init__(self, value: int) -> None:
        self.value = value
        self.neighbors: list[GraphNode] = []

    def __deepcopy__(self, memo: dict[int, Any]) -> GraphNode:
        if id(self) in memo:
            return memo[id(self)]  # type: ignore[return-value]
        new_node = GraphNode(self.value)
        memo[id(self)] = new_node
        for neighbor in self.neighbors:
            new_node.neighbors.append(copy.deepcopy(neighbor, memo))
        return new_node


def exercise5_deepcopy_graph() -> tuple[bool, bool]:
    n1 = GraphNode(1)
    n2 = GraphNode(2)
    n1.neighbors.append(n2)
    n2.neighbors.append(n1)   # cycle

    n1_copy = copy.deepcopy(n1)
    is_different = n1_copy is not n1
    values_ok = n1_copy.value == 1 and n1_copy.neighbors[0].value == 2
    return (is_different, values_ok)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Solution 1:", exercise1_weak_cache())
    print("Solution 2:", exercise2_planet_enum())
    print("Solution 3:", exercise3_chainmap_config())
    print("Solution 4:", exercise4_pickle_safe())
    print("Solution 5:", exercise5_deepcopy_graph())
