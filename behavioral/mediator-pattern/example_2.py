"""Mediator Pattern — Example 2: Air Traffic Control.

An ATC tower mediates communication between aircraft.  Aircraft never talk
directly to each other — all coordination goes through the tower.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


class ATCMediator(ABC):
    @abstractmethod
    def notify(self, sender: object, event: str, data: Any = None) -> None: ...


@dataclass
class Aircraft:
    callsign: str
    mediator: ATCMediator
    messages: list[str] = field(default_factory=list)

    def request_landing(self) -> None:
        print(f"  [{self.callsign}] Requesting landing clearance")
        self.mediator.notify(self, "landing_request", self.callsign)

    def request_takeoff(self) -> None:
        print(f"  [{self.callsign}] Requesting takeoff clearance")
        self.mediator.notify(self, "takeoff_request", self.callsign)

    def receive(self, message: str) -> None:
        self.messages.append(message)
        print(f"  [{self.callsign}] ATC: {message}")


class ATCTower(ATCMediator):
    """Air traffic control tower — the concrete mediator."""

    def __init__(self) -> None:
        self._aircraft: dict[str, Aircraft] = {}
        self._runway_free: bool = True

    def register(self, aircraft: Aircraft) -> None:
        self._aircraft[aircraft.callsign] = aircraft

    def notify(self, sender: object, event: str, data: Any = None) -> None:
        if not isinstance(sender, Aircraft):
            return
        callsign = str(data)

        if event == "landing_request":
            if self._runway_free:
                self._runway_free = False
                sender.receive(f"Cleared to land, runway is yours.")
                # Notify others of traffic
                for cs, ac in self._aircraft.items():
                    if cs != callsign:
                        ac.receive(f"Hold position — {callsign} landing.")
            else:
                sender.receive("Runway busy. Hold and await further instructions.")

        elif event == "takeoff_request":
            if self._runway_free:
                self._runway_free = False
                sender.receive("Cleared for takeoff.")
            else:
                sender.receive("Runway busy. Hold short.")

        elif event == "vacated":
            self._runway_free = True
            print(f"  [ATC] Runway now free after {callsign}")


def main() -> None:
    tower = ATCTower()
    ua500 = Aircraft("UA500", tower)
    ba202 = Aircraft("BA202", tower)
    lh300 = Aircraft("LH300", tower)
    for ac in (ua500, ba202, lh300):
        tower.register(ac)

    print("=== Landing requests ===")
    ua500.request_landing()
    ba202.request_landing()   # runway busy

    print("\n=== UA500 vacates runway ===")
    tower.notify(ua500, "vacated", "UA500")
    ba202.request_landing()   # should be cleared now


if __name__ == "__main__":
    main()
