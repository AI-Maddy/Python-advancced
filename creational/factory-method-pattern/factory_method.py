"""
Factory Method Pattern.

Defines a ``Creator`` ABC with a ``factory_method()`` that subclasses
override to produce different ``Product`` objects.  The creator's
business logic works through the Product interface.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Product hierarchy
# ---------------------------------------------------------------------------
class Vehicle(ABC):
    """Abstract product interface."""

    @abstractmethod
    def describe(self) -> str:
        """Return a human-readable description of this vehicle."""

    @abstractmethod
    def max_speed_kmh(self) -> int:
        """Return the maximum speed in km/h."""


class Car(Vehicle):
    """Concrete product: passenger car."""

    def describe(self) -> str:
        return "Car: 4-door sedan, comfortable for city driving."

    def max_speed_kmh(self) -> int:
        return 200


class Truck(Vehicle):
    """Concrete product: heavy goods truck."""

    def describe(self) -> str:
        return "Truck: heavy-duty, ideal for long-haul freight."

    def max_speed_kmh(self) -> int:
        return 120


class Motorcycle(Vehicle):
    """Concrete product: two-wheeled motorcycle."""

    def describe(self) -> str:
        return "Motorcycle: nimble, great for urban commuting."

    def max_speed_kmh(self) -> int:
        return 220


# ---------------------------------------------------------------------------
# Creator hierarchy
# ---------------------------------------------------------------------------
class VehicleFactory(ABC):
    """Abstract creator.  Subclasses override ``factory_method``."""

    @abstractmethod
    def factory_method(self) -> Vehicle:
        """Create and return a Vehicle product."""

    def deliver(self) -> str:
        """Template-method: uses factory_method internally."""
        vehicle = self.factory_method()
        return (
            f"Delivering [{vehicle.describe()}] "
            f"(max {vehicle.max_speed_kmh()} km/h)"
        )


class CarFactory(VehicleFactory):
    """Concrete creator for Cars."""

    def factory_method(self) -> Vehicle:
        return Car()


class TruckFactory(VehicleFactory):
    """Concrete creator for Trucks."""

    def factory_method(self) -> Vehicle:
        return Truck()


class MotorcycleFactory(VehicleFactory):
    """Concrete creator for Motorcycles."""

    def factory_method(self) -> Vehicle:
        return Motorcycle()


# ---------------------------------------------------------------------------
# Convenience registry (optional — not part of pattern core)
# ---------------------------------------------------------------------------
_REGISTRY: dict[str, type[VehicleFactory]] = {
    "car": CarFactory,
    "truck": TruckFactory,
    "motorcycle": MotorcycleFactory,
}


def get_factory(vehicle_type: str) -> VehicleFactory:
    """Look up and instantiate a factory by vehicle type string.

    Args:
        vehicle_type: One of ``'car'``, ``'truck'``, ``'motorcycle'``.

    Returns:
        A concrete VehicleFactory instance.

    Raises:
        KeyError: If vehicle_type is not registered.
    """
    cls = _REGISTRY[vehicle_type.lower()]
    return cls()


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    for vtype in ("car", "truck", "motorcycle"):
        factory = get_factory(vtype)
        print(factory.deliver())
