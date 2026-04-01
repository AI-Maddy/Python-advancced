"""
Day 08 — Exercises: Advanced OOP Patterns
"""
from __future__ import annotations
from typing import Any, Iterator


# Exercise 1: Vector2D with full operator support
class Vector2D:
    __slots__ = ("x", "y")
    def __init__(self, x: float, y: float) -> None: self.x = x; self.y = y
    # TODO: __repr__, __eq__, __hash__, __add__, __sub__, __mul__, __rmul__,
    #       __neg__, __abs__, __lt__, __len__, __getitem__, __iter__,
    #       __contains__, __matmul__, normalize()


# Exercise 2: CallableRegistry (__call__, __contains__, __len__, register decorator)
class CallableRegistry:
    def __init__(self) -> None: self._registry: dict[str, Any] = {}
    def register(self, name: str) -> Any: pass  # TODO: decorator
    def __call__(self, name: str, *args: Any, **kwargs: Any) -> Any: pass  # TODO
    def __contains__(self, name: str) -> bool: pass  # TODO
    def __len__(self) -> int: pass  # TODO


# Exercise 3: PluginBase with __init_subclass__
class PluginBase:
    _registry: dict[str, type] = {}
    def __init_subclass__(cls, plugin_name: str | None = None, **kwargs: Any) -> None:
        pass  # TODO: register cls in _registry

    @classmethod
    def get_plugin(cls, name: str) -> type | None: return cls._registry.get(name)

    @classmethod
    def registry(cls) -> dict[str, type]: return dict(cls._registry)


class JsonPlugin(PluginBase, plugin_name="json"):
    def process(self, data: str) -> str: return f"json:{data}"


if __name__ == "__main__":
    v = Vector2D(3.0, 4.0)
    print(abs(v))  # 5.0
