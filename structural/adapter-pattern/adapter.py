"""
Adapter Pattern.

Two flavours:
* Object adapter  — wraps the adaptee via composition.
* Class adapter   — inherits from both Target and Adaptee.

Target interface: ``request() -> str``
Adaptee (legacy): ``specific_request() -> str``
"""
from __future__ import annotations

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Target interface (what the client expects)
# ---------------------------------------------------------------------------
class Target(ABC):
    """New interface that all modern code expects."""

    @abstractmethod
    def request(self) -> str:
        """Execute a request using the modern interface."""


# ---------------------------------------------------------------------------
# Adaptee — legacy class with incompatible interface
# ---------------------------------------------------------------------------
class Adaptee:
    """Legacy component with a different interface.

    Clients cannot call this directly because the interface is wrong.
    """

    def specific_request(self) -> str:
        """The legacy operation (reversed for illustration)."""
        return "!eetpadA eht fo esnopser eht si sihT"

    def legacy_compute(self, x: int, y: int) -> int:
        """Another legacy operation."""
        return x * y + 42


# ---------------------------------------------------------------------------
# Object Adapter (composition)
# ---------------------------------------------------------------------------
class ObjectAdapter(Target):
    """Adapts Adaptee to the Target interface via composition.

    Args:
        adaptee: The legacy object to wrap.
    """

    def __init__(self, adaptee: Adaptee) -> None:
        self._adaptee = adaptee

    def request(self) -> str:
        result = self._adaptee.specific_request()
        return result[::-1]  # reverse the reversed string

    def compute(self, x: int, y: int) -> int:
        """Delegate to the legacy compute, exposing it through a cleaner API."""
        return self._adaptee.legacy_compute(x, y)


# ---------------------------------------------------------------------------
# Class Adapter (multiple inheritance)
# ---------------------------------------------------------------------------
class ClassAdapter(Target, Adaptee):
    """Adapts by inheriting both Target and Adaptee.

    Note: Multiple inheritance class adapters are less common in Python
    but valid.  Prefer object adapters when composition is possible.
    """

    def request(self) -> str:
        result = self.specific_request()
        return result[::-1]


# ---------------------------------------------------------------------------
# Client code — only knows about Target
# ---------------------------------------------------------------------------
def client_code(target: Target) -> str:
    """Works with any object that satisfies the Target interface."""
    return target.request()


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    adaptee = Adaptee()
    print(f"Adaptee raw output: {adaptee.specific_request()!r}")

    obj_adapter = ObjectAdapter(adaptee)
    print(f"Object adapter:     {client_code(obj_adapter)!r}")

    cls_adapter = ClassAdapter()
    print(f"Class adapter:      {client_code(cls_adapter)!r}")

    print(f"Compute via adapter: {obj_adapter.compute(3, 4)}")
