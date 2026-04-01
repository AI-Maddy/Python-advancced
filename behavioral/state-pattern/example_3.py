"""State Pattern — Example 3: Order Lifecycle.

An e-commerce order moves through: Pending → Paid → Shipped → Delivered
(or Cancelled from any state before Delivered).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class OrderState(ABC):
    @abstractmethod
    def pay(self, order: Order) -> None: ...
    @abstractmethod
    def ship(self, order: Order) -> None: ...
    @abstractmethod
    def deliver(self, order: Order) -> None: ...
    @abstractmethod
    def cancel(self, order: Order) -> None: ...

    def __repr__(self) -> str:
        return type(self).__name__


class PendingState(OrderState):
    def pay(self, order: Order) -> None:
        print(f"  Order {order.id}: Payment received.")
        order.state = PaidState()

    def ship(self, order: Order) -> None:
        print(f"  Order {order.id}: Must be paid before shipping.")

    def deliver(self, order: Order) -> None:
        print(f"  Order {order.id}: Cannot deliver — not paid or shipped.")

    def cancel(self, order: Order) -> None:
        print(f"  Order {order.id}: Cancelled (was pending).")
        order.state = CancelledState()


class PaidState(OrderState):
    def pay(self, order: Order) -> None:
        print(f"  Order {order.id}: Already paid.")

    def ship(self, order: Order) -> None:
        print(f"  Order {order.id}: Shipped!")
        order.state = ShippedState()

    def deliver(self, order: Order) -> None:
        print(f"  Order {order.id}: Cannot deliver — not shipped yet.")

    def cancel(self, order: Order) -> None:
        print(f"  Order {order.id}: Cancelled (refunding payment).")
        order.state = CancelledState()


class ShippedState(OrderState):
    def pay(self, order: Order) -> None:
        print(f"  Order {order.id}: Already paid.")

    def ship(self, order: Order) -> None:
        print(f"  Order {order.id}: Already shipped.")

    def deliver(self, order: Order) -> None:
        print(f"  Order {order.id}: Delivered!")
        order.state = DeliveredState()

    def cancel(self, order: Order) -> None:
        print(f"  Order {order.id}: Cannot cancel — already shipped.")


class DeliveredState(OrderState):
    def pay(self, order: Order) -> None:
        print(f"  Order {order.id}: Already delivered.")

    def ship(self, order: Order) -> None:
        print(f"  Order {order.id}: Already delivered.")

    def deliver(self, order: Order) -> None:
        print(f"  Order {order.id}: Already delivered.")

    def cancel(self, order: Order) -> None:
        print(f"  Order {order.id}: Cannot cancel — already delivered.")


class CancelledState(OrderState):
    def pay(self, order: Order) -> None:
        print(f"  Order {order.id}: Order is cancelled.")

    def ship(self, order: Order) -> None:
        print(f"  Order {order.id}: Order is cancelled.")

    def deliver(self, order: Order) -> None:
        print(f"  Order {order.id}: Order is cancelled.")

    def cancel(self, order: Order) -> None:
        print(f"  Order {order.id}: Already cancelled.")


@dataclass
class Order:
    id: str
    state: OrderState = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        self.state = PendingState()

    def pay(self) -> None: self.state.pay(self)
    def ship(self) -> None: self.state.ship(self)
    def deliver(self) -> None: self.state.deliver(self)
    def cancel(self) -> None: self.state.cancel(self)

    def status(self) -> str:
        return f"Order {self.id}: {self.state!r}"


def main() -> None:
    print("=== Normal flow ===")
    o1 = Order("ORD-001")
    o1.pay()
    o1.ship()
    o1.deliver()
    o1.cancel()  # too late

    print("\n=== Cancellation after payment ===")
    o2 = Order("ORD-002")
    o2.pay()
    o2.cancel()
    o2.ship()   # blocked

    print("\n=== Skip steps ===")
    o3 = Order("ORD-003")
    o3.ship()   # blocked
    o3.deliver()  # blocked


if __name__ == "__main__":
    main()
