"""
Day 08 — Advanced OOP Patterns
================================

Topics:
  - Composition over inheritance
  - __slots__ for memory
  - __getattr__ / __getattribute__ / __setattr__
  - __init_subclass__ for subclass hooks
  - __class_getitem__ for generic syntax
  - Operator overloading: __add__, __mul__, __lt__, __len__, __contains__
  - __call__ — callable objects
"""
from __future__ import annotations

from typing import Any, Iterator


# ---------------------------------------------------------------------------
# 1. Composition over Inheritance
# ---------------------------------------------------------------------------

class Logger:
    """Reusable logger component."""
    def log(self, msg: str) -> None:
        print(f"[LOG] {msg}")


class Validator:
    """Reusable validator component."""
    def validate(self, value: object) -> bool:
        return value is not None


class UserService:
    """Uses composition — HAS-A logger and validator, not IS-A."""

    def __init__(self) -> None:
        self._logger = Logger()
        self._validator = Validator()

    def create_user(self, name: str) -> dict[str, str]:
        if not self._validator.validate(name):
            raise ValueError("name required")
        self._logger.log(f"Creating user: {name}")
        return {"name": name, "id": "123"}


# ---------------------------------------------------------------------------
# 2. __slots__ for Memory Optimization
# ---------------------------------------------------------------------------

class WithDict:
    """Regular class — has __dict__, ~200 bytes overhead per instance."""
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class WithSlots:
    """Slots class — no __dict__, ~70 bytes per instance."""
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


def demo_slots() -> None:
    import sys
    a = WithDict(1.0, 2.0)
    b = WithSlots(1.0, 2.0)
    print(f"WithDict size: {sys.getsizeof(a)}")
    print(f"WithSlots size: {sys.getsizeof(b)}")
    print(f"WithDict has __dict__: {hasattr(a, '__dict__')}")
    print(f"WithSlots has __dict__: {hasattr(b, '__dict__')}")

    # Slots prevent adding new attributes
    a.z = 3.0   # works — __dict__ allows it
    try:
        b.z = 3.0   # AttributeError — no __dict__
    except AttributeError as e:
        print(f"Slots prevent: {e}")


# ---------------------------------------------------------------------------
# 3. __getattr__, __getattribute__, __setattr__
# ---------------------------------------------------------------------------

class ProxyObject:
    """Proxy that intercepts attribute access."""

    def __init__(self, wrapped: object) -> None:
        # Use object.__setattr__ to avoid recursion!
        object.__setattr__(self, "_wrapped", wrapped)
        object.__setattr__(self, "_access_count", 0)

    def __getattr__(self, name: str) -> Any:
        """Called only when normal attribute lookup fails.
        This is the SAFE hook — won't cause recursion.
        """
        object.__setattr__(self, "_access_count",
                           object.__getattribute__(self, "_access_count") + 1)
        return getattr(object.__getattribute__(self, "_wrapped"), name)

    def __setattr__(self, name: str, value: Any) -> None:
        """Called for ALL attribute assignments — careful about recursion!"""
        if name.startswith("_"):
            object.__setattr__(self, name, value)  # set on proxy itself
        else:
            setattr(object.__getattribute__(self, "_wrapped"), name, value)

    @property
    def access_count(self) -> int:
        return object.__getattribute__(self, "_access_count")


# ---------------------------------------------------------------------------
# 4. __init_subclass__ — Subclass Registration Hook
# ---------------------------------------------------------------------------

class PluginBase:
    """Base class that auto-registers subclasses."""
    _registry: dict[str, type] = {}

    def __init_subclass__(cls, plugin_name: str | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__.lower()
        PluginBase._registry[name] = cls
        print(f"[Registry] Registered plugin: {name!r} -> {cls.__name__}")

    @classmethod
    def get_plugin(cls, name: str) -> type | None:
        return cls._registry.get(name)


class JsonPlugin(PluginBase, plugin_name="json"):
    def process(self, data: str) -> str:
        return f"json:{data}"


class XmlPlugin(PluginBase, plugin_name="xml"):
    def process(self, data: str) -> str:
        return f"xml:{data}"


# ---------------------------------------------------------------------------
# 5. Operator Overloading — Vector2D
# ---------------------------------------------------------------------------

class Vector2D:
    """2D vector with full operator support."""

    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    # Arithmetic operators
    def __add__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector2D":
        """Scalar multiplication: v * 2."""
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector2D":
        """Reverse scalar multiplication: 2 * v."""
        return self.__mul__(scalar)

    def __neg__(self) -> "Vector2D":
        return Vector2D(-self.x, -self.y)

    def __abs__(self) -> float:
        """Magnitude: abs(v)."""
        import math
        return math.sqrt(self.x**2 + self.y**2)

    # Comparison
    def __lt__(self, other: "Vector2D") -> bool:
        """Compare by magnitude."""
        return abs(self) < abs(other)

    # Container-like
    def __len__(self) -> int:
        return 2

    def __getitem__(self, idx: int) -> float:
        if idx == 0: return self.x
        if idx == 1: return self.y
        raise IndexError(f"Vector2D index out of range: {idx}")

    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y

    def __contains__(self, value: float) -> bool:
        return value == self.x or value == self.y

    # Dot product as @
    def __matmul__(self, other: "Vector2D") -> float:
        return self.x * other.x + self.y * other.y


# ---------------------------------------------------------------------------
# 6. __call__ — Callable Objects
# ---------------------------------------------------------------------------

class RateLimiter:
    """Callable object — acts like a function with state."""

    def __init__(self, max_calls: int) -> None:
        self._max = max_calls
        self._count = 0

    def __call__(self, func_name: str) -> bool:
        """Return True if call is allowed, False if rate limited."""
        self._count += 1
        if self._count > self._max:
            print(f"[RateLimit] {func_name} blocked (count={self._count})")
            return False
        return True

    def reset(self) -> None:
        self._count = 0


class Memoizer:
    """Callable decorator object with cache."""

    def __init__(self, func: Any) -> None:
        self._func = func
        self._cache: dict[tuple[Any, ...], Any] = {}
        self.__doc__ = func.__doc__
        self.__name__ = func.__name__

    def __call__(self, *args: Any) -> Any:
        if args not in self._cache:
            self._cache[args] = self._func(*args)
        return self._cache[args]

    def cache_info(self) -> dict[str, int]:
        return {"size": len(self._cache)}


if __name__ == "__main__":
    print("=== Composition ===")
    svc = UserService()
    user = svc.create_user("Alice")
    print(user)

    print("\n=== __slots__ ===")
    demo_slots()

    print("\n=== Proxy ===")
    lst = [1, 2, 3]
    proxy = ProxyObject(lst)
    proxy.append(4)
    print(proxy.access_count)  # 1

    print("\n=== __init_subclass__ ===")
    p = PluginBase.get_plugin("json")
    if p:
        print(p().process("data"))

    print("\n=== Vector2D ===")
    v1 = Vector2D(1.0, 2.0)
    v2 = Vector2D(3.0, 4.0)
    print(v1 + v2)       # Vector2D(4.0, 6.0)
    print(v2 - v1)       # Vector2D(2.0, 2.0)
    print(v1 * 3)        # Vector2D(3.0, 6.0)
    print(2 * v1)        # Vector2D(2.0, 4.0)
    print(abs(v1))       # 2.236...
    print(v1 @ v2)       # dot product: 11.0
    print(list(v1))      # [1.0, 2.0]
    print(1.0 in v1)     # True

    print("\n=== Callable Objects ===")
    limiter = RateLimiter(3)
    for i in range(5):
        allowed = limiter("api_call")
        print(f"Call {i+1}: {'ok' if allowed else 'blocked'}")
