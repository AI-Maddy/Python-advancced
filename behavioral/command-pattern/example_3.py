"""Command Pattern — Example 3: Macro Recording.

A macro recorder captures a sequence of commands so they can be replayed
as a single composite command — classic "record and play" functionality.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...
    @abstractmethod
    def undo(self) -> None: ...


# ---------------------------------------------------------------------------
# Simple light receiver
# ---------------------------------------------------------------------------

@dataclass
class SmartLight:
    """Smart home light that can be turned on/off and dimmed."""
    name: str
    on: bool = False
    brightness: int = 100  # 0–100

    def turn_on(self) -> None:
        self.on = True
        print(f"  {self.name}: ON (brightness {self.brightness}%)")

    def turn_off(self) -> None:
        self.on = False
        print(f"  {self.name}: OFF")

    def dim(self, level: int) -> None:
        self.brightness = max(0, min(100, level))
        print(f"  {self.name}: dimmed to {self.brightness}%")


# ---------------------------------------------------------------------------
# Concrete commands
# ---------------------------------------------------------------------------

@dataclass
class TurnOnCommand(Command):
    light: SmartLight
    _was_on: bool = field(default=False, init=False)
    _prev_brightness: int = field(default=100, init=False)

    def execute(self) -> None:
        self._was_on = self.light.on
        self._prev_brightness = self.light.brightness
        self.light.turn_on()

    def undo(self) -> None:
        if not self._was_on:
            self.light.turn_off()
        self.light.dim(self._prev_brightness)


@dataclass
class TurnOffCommand(Command):
    light: SmartLight
    _was_on: bool = field(default=False, init=False)

    def execute(self) -> None:
        self._was_on = self.light.on
        self.light.turn_off()

    def undo(self) -> None:
        if self._was_on:
            self.light.turn_on()


@dataclass
class DimCommand(Command):
    light: SmartLight
    level: int
    _prev: int = field(default=100, init=False)

    def execute(self) -> None:
        self._prev = self.light.brightness
        self.light.dim(self.level)

    def undo(self) -> None:
        self.light.dim(self._prev)


# ---------------------------------------------------------------------------
# Macro
# ---------------------------------------------------------------------------

class MacroCommand(Command):
    """Composite command — records and replays a sequence."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._commands: list[Command] = []

    def add(self, command: Command) -> None:
        self._commands.append(command)

    def execute(self) -> None:
        print(f">> Executing macro: {self.name}")
        for cmd in self._commands:
            cmd.execute()

    def undo(self) -> None:
        print(f">> Undoing macro: {self.name}")
        for cmd in reversed(self._commands):
            cmd.undo()


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    bedroom = SmartLight("Bedroom")
    living = SmartLight("Living Room")

    # Record a "movie mode" macro
    movie_mode = MacroCommand("Movie Mode")
    movie_mode.add(TurnOffCommand(bedroom))
    movie_mode.add(TurnOnCommand(living))
    movie_mode.add(DimCommand(living, 20))

    print("=== Execute Movie Mode ===")
    movie_mode.execute()

    print("\n=== Undo Movie Mode ===")
    movie_mode.undo()


if __name__ == "__main__":
    main()
