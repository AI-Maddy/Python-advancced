"""
Abstract Factory Pattern.

Provides an interface for creating families of related UI widgets.
WindowsFactory, MacOSFactory, and LinuxFactory each produce consistent
sets of Button, Checkbox, and Dialog widgets.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Abstract products
# ---------------------------------------------------------------------------
class Button(ABC):
    """Abstract button widget."""

    @abstractmethod
    def render(self) -> str: ...

    @abstractmethod
    def on_click(self) -> str: ...


class Checkbox(ABC):
    """Abstract checkbox widget."""

    @abstractmethod
    def render(self) -> str: ...

    @abstractmethod
    def toggle(self) -> str: ...


class Dialog(ABC):
    """Abstract dialog widget."""

    @abstractmethod
    def render(self) -> str: ...

    @abstractmethod
    def close(self) -> str: ...


# ---------------------------------------------------------------------------
# Windows products
# ---------------------------------------------------------------------------
class WindowsButton(Button):
    def render(self) -> str:
        return "<WinButton style='flat'/>"

    def on_click(self) -> str:
        return "Windows button clicked (ripple effect)"


class WindowsCheckbox(Checkbox):
    def render(self) -> str:
        return "<WinCheckbox checked='false'/>"

    def toggle(self) -> str:
        return "Windows checkbox toggled"


class WindowsDialog(Dialog):
    def render(self) -> str:
        return "<WinDialog title='Dialog'/>"

    def close(self) -> str:
        return "Windows dialog closed"


# ---------------------------------------------------------------------------
# macOS products
# ---------------------------------------------------------------------------
class MacOSButton(Button):
    def render(self) -> str:
        return "<MacButton rounded='true'/>"

    def on_click(self) -> str:
        return "macOS button clicked (haptic)"


class MacOSCheckbox(Checkbox):
    def render(self) -> str:
        return "<MacCheckbox style='toggle'/>"

    def toggle(self) -> str:
        return "macOS checkbox toggled"


class MacOSDialog(Dialog):
    def render(self) -> str:
        return "<MacSheet modal='true'/>"

    def close(self) -> str:
        return "macOS sheet dismissed"


# ---------------------------------------------------------------------------
# Linux products
# ---------------------------------------------------------------------------
class LinuxButton(Button):
    def render(self) -> str:
        return "<GtkButton relief='normal'/>"

    def on_click(self) -> str:
        return "GTK button activated"


class LinuxCheckbox(Checkbox):
    def render(self) -> str:
        return "<GtkCheckButton active='false'/>"

    def toggle(self) -> str:
        return "GTK checkbox toggled"


class LinuxDialog(Dialog):
    def render(self) -> str:
        return "<GtkDialog/>"

    def close(self) -> str:
        return "GTK dialog destroyed"


# ---------------------------------------------------------------------------
# Abstract factory
# ---------------------------------------------------------------------------
class UIFactory(ABC):
    """Abstract factory — creates a family of related UI widgets."""

    @abstractmethod
    def create_button(self) -> Button: ...

    @abstractmethod
    def create_checkbox(self) -> Checkbox: ...

    @abstractmethod
    def create_dialog(self) -> Dialog: ...


class WindowsFactory(UIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()

    def create_dialog(self) -> Dialog:
        return WindowsDialog()


class MacOSFactory(UIFactory):
    def create_button(self) -> Button:
        return MacOSButton()

    def create_checkbox(self) -> Checkbox:
        return MacOSCheckbox()

    def create_dialog(self) -> Dialog:
        return MacOSDialog()


class LinuxFactory(UIFactory):
    def create_button(self) -> Button:
        return LinuxButton()

    def create_checkbox(self) -> Checkbox:
        return LinuxCheckbox()

    def create_dialog(self) -> Dialog:
        return LinuxDialog()


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------
class Application:
    """Client that uses a UIFactory without knowing concrete types."""

    def __init__(self, factory: UIFactory) -> None:
        self._button = factory.create_button()
        self._checkbox = factory.create_checkbox()
        self._dialog = factory.create_dialog()

    def render_ui(self) -> list[str]:
        """Render all widgets and return their HTML-like representations."""
        return [
            self._button.render(),
            self._checkbox.render(),
            self._dialog.render(),
        ]

    def interact(self) -> list[str]:
        """Simulate user interactions."""
        return [
            self._button.on_click(),
            self._checkbox.toggle(),
            self._dialog.close(),
        ]


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    for platform, factory_cls in [
        ("Windows", WindowsFactory),
        ("macOS", MacOSFactory),
        ("Linux", LinuxFactory),
    ]:
        print(f"\n--- {platform} ---")
        app = Application(factory_cls())
        for widget in app.render_ui():
            print(" ", widget)
        for action in app.interact():
            print(" ", action)
