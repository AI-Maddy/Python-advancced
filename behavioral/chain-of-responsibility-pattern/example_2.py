"""Chain of Responsibility — Example 2: Log Level Filtering.

A logging pipeline where each handler only outputs messages at or above its
configured level: DEBUG → INFO → WARNING → ERROR.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum


class LogLevel(IntEnum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40


@dataclass
class LogRecord:
    level: LogLevel
    message: str


class LogHandler(ABC):
    def __init__(self, min_level: LogLevel) -> None:
        self.min_level = min_level
        self._next: LogHandler | None = None

    def set_next(self, handler: LogHandler) -> LogHandler:
        self._next = handler
        return handler

    @abstractmethod
    def emit(self, record: LogRecord) -> None:
        """Write the record (already level-checked)."""

    def handle(self, record: LogRecord) -> None:
        if record.level >= self.min_level:
            self.emit(record)
        if self._next:
            self._next.handle(record)


class ConsoleHandler(LogHandler):
    """Prints DEBUG and above to stdout."""
    def emit(self, record: LogRecord) -> None:
        print(f"  [CONSOLE:{record.level.name}] {record.message}")


class FileHandler(LogHandler):
    """Simulates writing WARNING and above to a file."""
    def __init__(self) -> None:
        super().__init__(LogLevel.WARNING)
        self._lines: list[str] = []

    def emit(self, record: LogRecord) -> None:
        line = f"[FILE:{record.level.name}] {record.message}"
        self._lines.append(line)
        print(f"  {line}")

    @property
    def lines(self) -> list[str]:
        return list(self._lines)


class AlertHandler(LogHandler):
    """Sends an alert for ERROR messages."""
    def __init__(self) -> None:
        super().__init__(LogLevel.ERROR)
        self.alerts: list[str] = []

    def emit(self, record: LogRecord) -> None:
        msg = f"ALERT: {record.message}"
        self.alerts.append(msg)
        print(f"  [ALERT] {msg}")


def main() -> None:
    console = ConsoleHandler(LogLevel.DEBUG)
    file_h = FileHandler()
    alert = AlertHandler()
    console.set_next(file_h).set_next(alert)

    records = [
        LogRecord(LogLevel.DEBUG, "Entering function foo()"),
        LogRecord(LogLevel.INFO, "User logged in"),
        LogRecord(LogLevel.WARNING, "Disk space below 20%"),
        LogRecord(LogLevel.ERROR, "Database connection lost"),
    ]

    for rec in records:
        print(f"\n>> Dispatching {rec.level.name}: {rec.message}")
        console.handle(rec)

    print(f"\nFile log entries: {len(file_h.lines)}")
    print(f"Alerts triggered: {len(alert.alerts)}")


if __name__ == "__main__":
    main()
