"""Chain of Responsibility Pattern — passes requests along a handler chain.

Each handler in the chain either handles the request or forwards it to the
next handler.  The sender is decoupled from the receiver — it doesn't know
which handler will process the request.

Python-specific notes:
- ABC + @abstractmethod enforces the ``handle(request)`` interface.
- ``set_next`` returns ``self`` so handlers can be chained fluently:
  ``low.set_next(medium).set_next(high)``
- Returning ``None`` when no handler processes the request is Pythonic and
  avoids exceptions for the "unhandled" case.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


# ---------------------------------------------------------------------------
# Abstract handler
# ---------------------------------------------------------------------------

class Handler(ABC):
    """Abstract base for all handlers in the chain.

    Attributes:
        _next: The next handler in the chain, or ``None`` if this is the last.
    """

    def __init__(self) -> None:
        self._next: Handler | None = None

    def set_next(self, handler: Handler) -> Handler:
        """Attach *handler* as the next link in the chain and return it.

        This allows fluent chaining::

            low.set_next(medium).set_next(high)

        Args:
            handler: The next handler.

        Returns:
            The *handler* argument (for fluent chaining).
        """
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, request: Any) -> Any | None:
        """Process *request* or forward it to the next handler.

        Args:
            request: The incoming request.

        Returns:
            The result of handling *request*, or ``None`` if unhandled.
        """

    def _forward(self, request: Any) -> Any | None:
        """Forward *request* to the next handler, or return ``None``."""
        if self._next:
            return self._next.handle(request)
        return None


# ---------------------------------------------------------------------------
# Priority-based concrete handlers
# ---------------------------------------------------------------------------

@dataclass
class Request:
    """A work item with a priority level and a description.

    Attributes:
        priority: Numeric priority (1 = low, 2 = medium, 3 = high).
        description: Human-readable description of the request.
    """
    priority: int
    description: str


class LowPriorityHandler(Handler):
    """Handles requests with priority <= 1."""

    def handle(self, request: Any) -> Any | None:
        if isinstance(request, Request) and request.priority <= 1:
            result = f"[Low] Handled: {request.description}"
            print(result)
            return result
        return self._forward(request)


class MediumPriorityHandler(Handler):
    """Handles requests with priority <= 2."""

    def handle(self, request: Any) -> Any | None:
        if isinstance(request, Request) and request.priority <= 2:
            result = f"[Medium] Handled: {request.description}"
            print(result)
            return result
        return self._forward(request)


class HighPriorityHandler(Handler):
    """Handles requests with priority <= 3 (catches everything it can)."""

    def handle(self, request: Any) -> Any | None:
        if isinstance(request, Request) and request.priority <= 3:
            result = f"[High] Handled: {request.description}"
            print(result)
            return result
        return self._forward(request)


# ---------------------------------------------------------------------------
# Client demonstration
# ---------------------------------------------------------------------------

def main() -> None:
    """Build a priority chain and route requests through it."""
    low = LowPriorityHandler()
    medium = MediumPriorityHandler()
    high = HighPriorityHandler()

    # Build chain: low → medium → high
    low.set_next(medium).set_next(high)

    requests = [
        Request(1, "Fix typo in docs"),
        Request(2, "Refactor module"),
        Request(3, "Production outage"),
        Request(4, "Unknown priority — unhandled"),
    ]

    for req in requests:
        result = low.handle(req)
        if result is None:
            print(f"[Chain] No handler for priority={req.priority}")


if __name__ == "__main__":
    main()
