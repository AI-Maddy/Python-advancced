"""
Example 1 — Log handler factory.

Different environments (console, file, remote) produce different log
handlers through the same factory-method interface.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from io import StringIO


class LogHandler(ABC):
    """Product interface."""

    @abstractmethod
    def emit(self, message: str) -> None: ...

    @abstractmethod
    def name(self) -> str: ...


class ConsoleHandler(LogHandler):
    def emit(self, message: str) -> None:
        print(f"[CONSOLE] {message}")

    def name(self) -> str:
        return "ConsoleHandler"


class FileHandler(LogHandler):
    def __init__(self) -> None:
        self._buffer = StringIO()

    def emit(self, message: str) -> None:
        self._buffer.write(f"[FILE] {message}\n")

    def name(self) -> str:
        return "FileHandler"

    def contents(self) -> str:
        return self._buffer.getvalue()


class RemoteHandler(LogHandler):
    def __init__(self) -> None:
        self._sent: list[str] = []

    def emit(self, message: str) -> None:
        self._sent.append(message)

    def name(self) -> str:
        return "RemoteHandler"


class LogHandlerFactory(ABC):
    @abstractmethod
    def factory_method(self) -> LogHandler: ...

    def log(self, message: str) -> None:
        handler = self.factory_method()
        handler.emit(message)


class ConsoleLogFactory(LogHandlerFactory):
    def factory_method(self) -> LogHandler:
        return ConsoleHandler()


class FileLogFactory(LogHandlerFactory):
    def factory_method(self) -> LogHandler:
        return FileHandler()


class RemoteLogFactory(LogHandlerFactory):
    def factory_method(self) -> LogHandler:
        return RemoteHandler()


def main() -> None:
    for factory_cls in (ConsoleLogFactory, FileLogFactory, RemoteLogFactory):
        factory = factory_cls()
        handler = factory.factory_method()
        print(f"Created handler: {handler.name()}")
        handler.emit("Application started")


if __name__ == "__main__":
    main()
