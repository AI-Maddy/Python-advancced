"""Observer Pattern — Example 2: UI Event System.

Simulates a minimal GUI event bus where widgets subscribe to DOM-like events
(click, hover, keypress) and react independently.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from observer_pattern import Observer, Subject


@dataclass
class EventBus(Subject):
    """Central event bus that widgets publish to and subscribe from."""

    def emit(self, event: str, payload: Any = None) -> None:
        """Publish *event* with optional *payload* to all subscribers."""
        self.notify(event, payload)


@dataclass
class ButtonWidget(Observer):
    """Reacts to 'click' events."""
    name: str = "Button"
    click_count: int = 0

    def update(self, event: str, data: Any = None) -> None:
        if event == "click":
            self.click_count += 1
            print(f"[{self.name}] clicked! (total: {self.click_count})")


@dataclass
class TooltipWidget(Observer):
    """Shows a tooltip on 'hover' events."""
    visible: bool = False

    def update(self, event: str, data: Any = None) -> None:
        if event == "hover":
            self.visible = True
            print(f"[Tooltip] shown for element: {data}")
        elif event == "blur":
            self.visible = False
            print("[Tooltip] hidden")


@dataclass
class KeyLogger(Observer):
    """Captures 'keypress' events."""
    keys: list[str] = field(default_factory=list)

    def update(self, event: str, data: Any = None) -> None:
        if event == "keypress" and data:
            self.keys.append(str(data))
            print(f"[KeyLogger] key pressed: {data}")


def main() -> None:
    bus = EventBus()
    btn = ButtonWidget(name="SubmitBtn")
    tip = TooltipWidget()
    klog = KeyLogger()

    bus.attach(btn, "click")
    bus.attach(tip, "hover")
    bus.attach(tip, "blur")
    bus.attach(klog, "keypress")

    bus.emit("hover", "submit-button")
    bus.emit("click")
    bus.emit("keypress", "Enter")
    bus.emit("click")
    bus.emit("blur")
    bus.emit("keypress", "Escape")

    print(f"\nButton clicked {btn.click_count} times")
    print(f"Keys captured: {klog.keys}")


if __name__ == "__main__":
    main()
