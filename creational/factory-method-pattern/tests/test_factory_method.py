"""pytest tests for factory method pattern."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from factory_method import (
    Car,
    CarFactory,
    Motorcycle,
    MotorcycleFactory,
    Truck,
    TruckFactory,
    VehicleFactory,
    get_factory,
)


class TestVehicleFactory:
    def test_car_factory_creates_car(self) -> None:
        factory = CarFactory()
        vehicle = factory.factory_method()
        assert isinstance(vehicle, Car)

    def test_truck_factory_creates_truck(self) -> None:
        factory = TruckFactory()
        vehicle = factory.factory_method()
        assert isinstance(vehicle, Truck)

    def test_motorcycle_factory_creates_motorcycle(self) -> None:
        factory = MotorcycleFactory()
        vehicle = factory.factory_method()
        assert isinstance(vehicle, Motorcycle)

    def test_deliver_returns_string(self) -> None:
        for factory_cls in (CarFactory, TruckFactory, MotorcycleFactory):
            result = factory_cls().deliver()
            assert isinstance(result, str)
            assert "km/h" in result

    def test_polymorphic_usage(self) -> None:
        factories: list[VehicleFactory] = [
            CarFactory(), TruckFactory(), MotorcycleFactory()
        ]
        descriptions = [f.deliver() for f in factories]
        assert len(set(descriptions)) == 3  # all different

    def test_vehicle_speeds_are_positive(self) -> None:
        for factory_cls in (CarFactory, TruckFactory, MotorcycleFactory):
            vehicle = factory_cls().factory_method()
            assert vehicle.max_speed_kmh() > 0


class TestGetFactory:
    def test_lookup_car(self) -> None:
        assert isinstance(get_factory("car").factory_method(), Car)

    def test_lookup_truck(self) -> None:
        assert isinstance(get_factory("truck").factory_method(), Truck)

    def test_lookup_motorcycle(self) -> None:
        assert isinstance(get_factory("motorcycle").factory_method(), Motorcycle)

    def test_case_insensitive(self) -> None:
        assert isinstance(get_factory("CAR").factory_method(), Car)

    def test_unknown_raises_key_error(self) -> None:
        with pytest.raises(KeyError):
            get_factory("spaceship")
