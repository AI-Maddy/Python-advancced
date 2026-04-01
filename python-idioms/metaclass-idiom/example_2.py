"""
Example 2 — __init_subclass__ for handler registration.
"""
from __future__ import annotations

from typing import ClassVar


class EventHandler:
    """Base class; subclasses register themselves for named events."""

    _registry: ClassVar[dict[str, type[EventHandler]]] = {}
    event_name: ClassVar[str] = ""

    def __init_subclass__(cls, event: str = "", **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if event:
            cls.event_name = event
            EventHandler._registry[event] = cls

    def handle(self, payload: dict) -> str:
        return f"{type(self).__name__} handled {payload}"


class UserCreatedHandler(EventHandler, event="user.created"):
    def handle(self, payload: dict) -> str:
        return f"New user: {payload.get('name')}"


class OrderPlacedHandler(EventHandler, event="order.placed"):
    def handle(self, payload: dict) -> str:
        return f"Order #{payload.get('id')} placed"


def dispatch(event: str, payload: dict) -> str:
    handler_cls = EventHandler._registry.get(event)
    if handler_cls is None:
        return f"No handler for {event!r}"
    return handler_cls().handle(payload)


def main() -> None:
    print("Registered events:", list(EventHandler._registry.keys()))
    print(dispatch("user.created", {"name": "Alice"}))
    print(dispatch("order.placed", {"id": 42}))
    print(dispatch("unknown.event", {}))


if __name__ == "__main__":
    main()
