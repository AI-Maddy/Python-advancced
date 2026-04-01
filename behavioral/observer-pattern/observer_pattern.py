"""Observer Pattern — broadcasts state changes to subscribers.

The Observer pattern defines a one-to-many dependency between objects so that
when one object changes state, all its dependents are notified and updated
automatically.

Python-specific notes:
- Use ABC + @abstractmethod for the Observer interface.
- Subject holds a list of weak-references or direct references to observers.
- Python's built-in event libraries (e.g. blinker) offer similar functionality,
  but implementing from scratch keeps the pattern explicit and testable.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Abstract base
# ---------------------------------------------------------------------------

class Observer(ABC):
    """Abstract observer that receives event notifications."""

    @abstractmethod
    def update(self, event: str, data: Any = None) -> None:
        """React to a notification from the subject.

        Args:
            event: Name of the event that occurred.
            data:  Optional payload attached to the event.
        """


class Subject:
    """Observable subject that manages a list of observers and notifies them.

    Attributes:
        _observers: Mapping of event names to registered observers.
            An empty string key ``""`` represents a wildcard (all events).
    """

    def __init__(self) -> None:
        self._observers: dict[str, list[Observer]] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def attach(self, observer: Observer, event: str = "") -> None:
        """Register *observer* to receive notifications for *event*.

        Args:
            observer: The observer to register.
            event:    Event name to listen to; ``""`` means all events.
        """
        self._observers.setdefault(event, [])
        if observer not in self._observers[event]:
            self._observers[event].append(observer)

    def detach(self, observer: Observer, event: str = "") -> None:
        """Unregister *observer* from *event*.

        Args:
            observer: The observer to remove.
            event:    Event name; ``""`` means all events.
        """
        bucket = self._observers.get(event, [])
        if observer in bucket:
            bucket.remove(observer)

    # ------------------------------------------------------------------
    # Notification
    # ------------------------------------------------------------------

    def notify(self, event: str, data: Any = None) -> None:
        """Notify all observers registered for *event* or wildcard.

        Args:
            event: Name of the event that occurred.
            data:  Optional payload to forward to observers.
        """
        seen: set[int] = set()
        for bucket_key in (event, ""):
            for obs in list(self._observers.get(bucket_key, [])):
                if id(obs) not in seen:
                    obs.update(event, data)
                    seen.add(id(obs))


# ---------------------------------------------------------------------------
# Concrete observers
# ---------------------------------------------------------------------------

@dataclass
class EventLogger(Observer):
    """Logs every event to an in-memory list.

    Attributes:
        log: Chronologically ordered list of ``(event, data)`` tuples.
    """
    log: list[tuple[str, Any]] = field(default_factory=list)

    def update(self, event: str, data: Any = None) -> None:
        """Append *(event, data)* to the log."""
        self.log.append((event, data))
        print(f"[EventLogger] {event}: {data}")


@dataclass
class MetricsCollector(Observer):
    """Counts how many times each event fires.

    Attributes:
        counts: Mapping from event name to occurrence count.
    """
    counts: dict[str, int] = field(default_factory=dict)

    def update(self, event: str, data: Any = None) -> None:
        """Increment the counter for *event*."""
        self.counts[event] = self.counts.get(event, 0) + 1
        print(f"[MetricsCollector] {event} count={self.counts[event]}")


@dataclass
class AlertSystem(Observer):
    """Raises an alert when a monitored threshold event occurs.

    Attributes:
        alerts:          List of alert messages triggered so far.
        watched_events:  Set of event names that should trigger alerts.
    """
    alerts: list[str] = field(default_factory=list)
    watched_events: set[str] = field(default_factory=set)

    def update(self, event: str, data: Any = None) -> None:
        """Trigger an alert if *event* is in *watched_events*."""
        if not self.watched_events or event in self.watched_events:
            msg = f"ALERT: {event} — {data}"
            self.alerts.append(msg)
            print(f"[AlertSystem] {msg}")


# ---------------------------------------------------------------------------
# Client demonstration
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the Observer pattern with a simple temperature sensor."""
    sensor = Subject()

    logger = EventLogger()
    metrics = MetricsCollector()
    alerts = AlertSystem(watched_events={"overheating"})

    sensor.attach(logger)          # wildcard: receives all events
    sensor.attach(metrics)         # wildcard
    sensor.attach(alerts)          # wildcard (but internally filters)

    sensor.notify("temperature_change", 45)
    sensor.notify("overheating", 95)
    sensor.notify("temperature_change", 38)

    # Detach the logger and fire another event
    sensor.detach(logger)
    sensor.notify("temperature_change", 30)

    print("\n--- Summary ---")
    print("Logger entries:", logger.log)
    print("Metrics:", metrics.counts)
    print("Alerts:", alerts.alerts)


if __name__ == "__main__":
    main()
