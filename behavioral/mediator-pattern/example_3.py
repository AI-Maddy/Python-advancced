"""Mediator Pattern — Example 3: UI Component Coordination.

A dialog mediator coordinates a text field, a checkbox, and a submit button.
The submit button is enabled only when the text field is non-empty AND the
checkbox is checked.  Components never directly query each other.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


class UIMediator(ABC):
    @abstractmethod
    def notify(self, sender: object, event: str, data: Any = None) -> None: ...


@dataclass
class TextField:
    name: str
    mediator: UIMediator
    value: str = ""

    def set_text(self, text: str) -> None:
        self.value = text
        print(f"  [TextField:{self.name}] value='{text}'")
        self.mediator.notify(self, "text_changed", text)


@dataclass
class Checkbox:
    name: str
    mediator: UIMediator
    checked: bool = False

    def toggle(self) -> None:
        self.checked = not self.checked
        print(f"  [Checkbox:{self.name}] checked={self.checked}")
        self.mediator.notify(self, "checked_changed", self.checked)


@dataclass
class Button:
    name: str
    mediator: UIMediator
    enabled: bool = False

    def click(self) -> None:
        if self.enabled:
            print(f"  [Button:{self.name}] CLICKED!")
            self.mediator.notify(self, "clicked", None)
        else:
            print(f"  [Button:{self.name}] disabled, cannot click")

    def set_enabled(self, enabled: bool) -> None:
        self.enabled = enabled
        status = "enabled" if enabled else "disabled"
        print(f"  [Button:{self.name}] is now {status}")


class DialogMediator(UIMediator):
    """Mediator that wires TextField + Checkbox → Button enable logic."""

    def __init__(self) -> None:
        self.text_field: TextField | None = None
        self.checkbox: Checkbox | None = None
        self.submit_btn: Button | None = None

    def notify(self, sender: object, event: str, data: Any = None) -> None:
        self._update_submit_state()

    def _update_submit_state(self) -> None:
        if self.submit_btn and self.text_field and self.checkbox:
            should_enable = bool(self.text_field.value) and self.checkbox.checked
            self.submit_btn.set_enabled(should_enable)


def main() -> None:
    mediator = DialogMediator()
    name_field = TextField("name", mediator)
    agree_box = Checkbox("agree", mediator)
    submit = Button("submit", mediator)

    mediator.text_field = name_field
    mediator.checkbox = agree_box
    mediator.submit_btn = submit

    print("=== Initial state ===")
    submit.click()  # disabled

    print("\n=== Type name ===")
    name_field.set_text("Alice")
    submit.click()  # still disabled (checkbox unchecked)

    print("\n=== Check box ===")
    agree_box.toggle()
    submit.click()  # now enabled

    print("\n=== Uncheck box ===")
    agree_box.toggle()
    submit.click()  # disabled again


if __name__ == "__main__":
    main()
