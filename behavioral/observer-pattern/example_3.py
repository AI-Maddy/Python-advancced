"""Observer Pattern — Example 3: Sensor Data Pipeline.

A sensor produces readings.  Multiple downstream consumers (a data recorder,
an anomaly detector, and a display) react to each new reading independently.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from observer_pattern import Observer, Subject


@dataclass
class TemperatureSensor(Subject):
    """Simulates a temperature sensor that emits periodic readings."""
    _current: float = 20.0

    def read(self) -> float:
        """Simulate a new sensor reading and notify observers."""
        delta = random.uniform(-2.0, 3.0)
        self._current = round(self._current + delta, 2)
        self.notify("reading", self._current)
        return self._current


@dataclass
class DataRecorder(Observer):
    """Stores all readings in a time-series list."""
    readings: list[float] = field(default_factory=list)

    def update(self, event: str, data: Any = None) -> None:
        if event == "reading" and data is not None:
            self.readings.append(float(data))


@dataclass
class AnomalyDetector(Observer):
    """Flags readings outside the normal range."""
    low: float = 15.0
    high: float = 30.0
    anomalies: list[float] = field(default_factory=list)

    def update(self, event: str, data: Any = None) -> None:
        if event == "reading" and data is not None:
            val = float(data)
            if val < self.low or val > self.high:
                self.anomalies.append(val)
                print(f"[AnomalyDetector] Out-of-range: {val}°C")


@dataclass
class DisplayPanel(Observer):
    """Prints the latest reading to the console display."""
    last: float | None = None

    def update(self, event: str, data: Any = None) -> None:
        if event == "reading" and data is not None:
            self.last = float(data)
            print(f"[Display] Current temperature: {self.last}°C")


def main() -> None:
    random.seed(42)
    sensor = TemperatureSensor()

    recorder = DataRecorder()
    detector = AnomalyDetector(low=18.0, high=25.0)
    display = DisplayPanel()

    sensor.attach(recorder)
    sensor.attach(detector)
    sensor.attach(display)

    print("=== Sensor readings ===")
    for _ in range(10):
        sensor.read()

    print(f"\nRecorded {len(recorder.readings)} readings")
    print(f"Anomalies detected: {detector.anomalies}")
    avg = sum(recorder.readings) / len(recorder.readings)
    print(f"Average temperature: {avg:.2f}°C")


if __name__ == "__main__":
    main()
