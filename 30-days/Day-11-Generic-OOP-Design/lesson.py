"""Day 11 — Generic OOP Design

Topics: Generic Repository, Result type, Generic Event System, Protocol with generics
"""
from __future__ import annotations
from typing import Generic, TypeVar, Protocol, Callable
T = TypeVar("T")
ID = TypeVar("ID")

# See solutions.py for full implementations — this file shows the patterns.

from solutions import Repository, Ok, Err, safe_divide, safe_parse_int, EventBus

if __name__ == "__main__":
    from dataclasses import dataclass

    @dataclass
    class Product:
        name: str
        price: float

    repo: Repository[Product, str] = Repository()  # type: ignore[type-arg]
    repo.save("p1", Product("Widget", 9.99))
    repo.save("p2", Product("Gadget", 19.99))
    print(repo.find_all())
    print(repo.count())

    # Result monad
    for s in ["42", "bad", "100"]:
        result = safe_parse_int(s)
        if result.is_ok():
            print(f"Parsed: {result.unwrap()}")
        else:
            print(f"Error: {result.error}")  # type: ignore[union-attr]

    # Event bus
    bus: EventBus[int] = EventBus()
    received: list[int] = []
    bus.subscribe(received.append)
    bus.publish(1)
    bus.publish(2)
    print(f"Received events: {received}")
