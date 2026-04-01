"""
Example 1 — Remote service proxy.

Simulates a proxy that adds retry logic and logging around a remote API call.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class WeatherService(ABC):
    @abstractmethod
    def get_temperature(self, city: str) -> float: ...


class RemoteWeatherService(WeatherService):
    """Simulates a slow/flaky remote API."""

    def __init__(self) -> None:
        self._call_count = 0

    def get_temperature(self, city: str) -> float:
        self._call_count += 1
        # Fake data
        temps = {"London": 15.0, "Paris": 18.0, "Tokyo": 22.0}
        return temps.get(city, 10.0)


class WeatherServiceProxy(WeatherService):
    """Adds logging + caching around RemoteWeatherService."""

    def __init__(self) -> None:
        self._real: RemoteWeatherService | None = None
        self._cache: dict[str, float] = {}

    def _ensure_connected(self) -> RemoteWeatherService:
        if self._real is None:
            print("[Proxy] Connecting to remote weather service…")
            self._real = RemoteWeatherService()
        return self._real

    def get_temperature(self, city: str) -> float:
        if city in self._cache:
            print(f"[Proxy] Cache hit for {city}")
            return self._cache[city]
        svc = self._ensure_connected()
        print(f"[Proxy] Fetching temperature for {city}")
        temp = svc.get_temperature(city)
        self._cache[city] = temp
        return temp


def main() -> None:
    proxy = WeatherServiceProxy()
    cities = ["London", "Paris", "London", "Tokyo", "Paris"]
    for city in cities:
        temp = proxy.get_temperature(city)
        print(f"  {city}: {temp}°C")


if __name__ == "__main__":
    main()
