"""
Day 08 — Exercises: Advanced OOP Patterns
"""
from __future__ import annotations

import math
from typing import Any, Iterator


# Exercise 1: Vector2D with full operator support
class Vector2D:
    __slots__ = ("x", "y")
    def __init__(self, x: float, y: float) -> None: self.x = x; self.y = y

    def __repr__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __add__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector2D":
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector2D":
        return self.__mul__(scalar)

    def __neg__(self) -> "Vector2D":
        return Vector2D(-self.x, -self.y)

    def __abs__(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def __lt__(self, other: "Vector2D") -> bool:
        return abs(self) < abs(other)

    def __len__(self) -> int:
        return 2

    def __getitem__(self, idx: int) -> float:
        if idx == 0: return self.x
        if idx == 1: return self.y
        raise IndexError(f"index {idx} out of range")

    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y

    def __contains__(self, value: float) -> bool:
        return value == self.x or value == self.y

    def __matmul__(self, other: "Vector2D") -> float:
        return self.x * other.x + self.y * other.y

    def normalize(self) -> "Vector2D":
        mag = abs(self)
        if mag == 0:
            raise ValueError("Cannot normalize zero vector")
        return Vector2D(self.x / mag, self.y / mag)


# Exercise 2: CallableRegistry (__call__, __contains__, __len__, register decorator)
class CallableRegistry:
    def __init__(self) -> None: self._registry: dict[str, Any] = {}

    def register(self, name: str) -> Any:
        def decorator(func: Any) -> Any:
            self._registry[name] = func
            return func
        return decorator

    def __call__(self, name: str, *args: Any, **kwargs: Any) -> Any:
        if name not in self._registry:
            raise KeyError(f"No callable registered as {name!r}")
        return self._registry[name](*args, **kwargs)

    def __contains__(self, name: str) -> bool:
        return name in self._registry

    def __len__(self) -> int:
        return len(self._registry)


# Exercise 3: PluginBase with __init_subclass__
class PluginBase:
    _registry: dict[str, type] = {}
    def __init_subclass__(cls, plugin_name: str | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__.lower()
        PluginBase._registry[name] = cls

    @classmethod
    def get_plugin(cls, name: str) -> type | None: return cls._registry.get(name)

    @classmethod
    def registry(cls) -> dict[str, type]: return dict(cls._registry)


class JsonPlugin(PluginBase, plugin_name="json"):
    def process(self, data: str) -> str: return f"json:{data}"


if __name__ == "__main__":
    v = Vector2D(3.0, 4.0)
    print(abs(v))  # 5.0
