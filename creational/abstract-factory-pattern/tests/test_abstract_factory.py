"""pytest tests for abstract factory pattern."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from abstract_factory import (
    Application,
    Button,
    Checkbox,
    Dialog,
    LinuxButton,
    LinuxCheckbox,
    LinuxDialog,
    LinuxFactory,
    MacOSButton,
    MacOSCheckbox,
    MacOSDialog,
    MacOSFactory,
    UIFactory,
    WindowsButton,
    WindowsCheckbox,
    WindowsDialog,
    WindowsFactory,
)


class TestWindowsFactory:
    def setup_method(self) -> None:
        self.factory: UIFactory = WindowsFactory()

    def test_creates_windows_button(self) -> None:
        assert isinstance(self.factory.create_button(), WindowsButton)

    def test_creates_windows_checkbox(self) -> None:
        assert isinstance(self.factory.create_checkbox(), WindowsCheckbox)

    def test_creates_windows_dialog(self) -> None:
        assert isinstance(self.factory.create_dialog(), WindowsDialog)

    def test_products_are_buttons(self) -> None:
        assert isinstance(self.factory.create_button(), Button)

    def test_products_are_checkboxes(self) -> None:
        assert isinstance(self.factory.create_checkbox(), Checkbox)

    def test_products_are_dialogs(self) -> None:
        assert isinstance(self.factory.create_dialog(), Dialog)


class TestMacOSFactory:
    def setup_method(self) -> None:
        self.factory: UIFactory = MacOSFactory()

    def test_creates_macos_button(self) -> None:
        assert isinstance(self.factory.create_button(), MacOSButton)

    def test_creates_macos_checkbox(self) -> None:
        assert isinstance(self.factory.create_checkbox(), MacOSCheckbox)

    def test_creates_macos_dialog(self) -> None:
        assert isinstance(self.factory.create_dialog(), MacOSDialog)


class TestLinuxFactory:
    def setup_method(self) -> None:
        self.factory: UIFactory = LinuxFactory()

    def test_creates_linux_button(self) -> None:
        assert isinstance(self.factory.create_button(), LinuxButton)

    def test_creates_linux_checkbox(self) -> None:
        assert isinstance(self.factory.create_checkbox(), LinuxCheckbox)

    def test_creates_linux_dialog(self) -> None:
        assert isinstance(self.factory.create_dialog(), LinuxDialog)


class TestApplication:
    def test_windows_app_renders(self) -> None:
        app = Application(WindowsFactory())
        widgets = app.render_ui()
        assert len(widgets) == 3
        assert all(isinstance(w, str) for w in widgets)

    def test_macos_app_renders(self) -> None:
        app = Application(MacOSFactory())
        widgets = app.render_ui()
        assert len(widgets) == 3

    def test_linux_app_renders(self) -> None:
        app = Application(LinuxFactory())
        widgets = app.render_ui()
        assert len(widgets) == 3

    def test_products_from_same_factory_are_compatible(self) -> None:
        """Products from the same factory must all be from the same family."""
        win_app = Application(WindowsFactory())
        mac_app = Application(MacOSFactory())
        # Render strings differ between platforms
        assert win_app.render_ui() != mac_app.render_ui()

    def test_interact_returns_actions(self) -> None:
        app = Application(LinuxFactory())
        actions = app.interact()
        assert len(actions) == 3
        assert all(isinstance(a, str) for a in actions)
