"""Command Pattern — encapsulates requests as objects to queue, log, and undo.

The Command pattern turns a request into a stand-alone object that contains
all information about the request.  This lets you parameterise methods with
different requests, delay or queue execution, and implement undoable operations.

Python-specific notes:
- ABC + @abstractmethod enforces the ``execute``/``undo`` contract.
- ``CommandHistory`` (the Invoker) maintains a stack of executed commands to
  support multi-level undo.
- ``TextEditor`` (the Receiver) owns the mutable state; commands mutate it.
- ``dataclass`` is convenient for command objects that carry data.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Abstract command
# ---------------------------------------------------------------------------

class Command(ABC):
    """Abstract base for all commands."""

    @abstractmethod
    def execute(self) -> None:
        """Carry out the action."""

    @abstractmethod
    def undo(self) -> None:
        """Reverse the action."""


# ---------------------------------------------------------------------------
# Receiver
# ---------------------------------------------------------------------------

class TextEditor:
    """Simple text buffer that acts as the command receiver.

    Attributes:
        _text: Current content of the editor.
    """

    def __init__(self, initial: str = "") -> None:
        self._text: str = initial

    @property
    def text(self) -> str:
        """Current text in the editor."""
        return self._text

    def insert(self, position: int, content: str) -> None:
        """Insert *content* at *position*."""
        self._text = self._text[:position] + content + self._text[position:]

    def delete(self, position: int, length: int) -> str:
        """Delete *length* characters starting at *position*; return deleted text."""
        deleted = self._text[position : position + length]
        self._text = self._text[:position] + self._text[position + length :]
        return deleted

    def replace(self, position: int, length: int, content: str) -> str:
        """Replace *length* characters at *position* with *content*; return replaced text."""
        old = self._text[position : position + length]
        self._text = self._text[:position] + content + self._text[position + length :]
        return old


# ---------------------------------------------------------------------------
# Concrete commands
# ---------------------------------------------------------------------------

@dataclass
class InsertCommand(Command):
    """Inserts text at a given position."""
    editor: TextEditor
    position: int
    content: str

    def execute(self) -> None:
        """Insert *content* at *position*."""
        self.editor.insert(self.position, self.content)

    def undo(self) -> None:
        """Remove the previously inserted content."""
        self.editor.delete(self.position, len(self.content))


@dataclass
class DeleteCommand(Command):
    """Deletes a span of text."""
    editor: TextEditor
    position: int
    length: int
    _deleted: str = field(default="", init=False, repr=False)

    def execute(self) -> None:
        """Delete *length* characters starting at *position*."""
        self._deleted = self.editor.delete(self.position, self.length)

    def undo(self) -> None:
        """Re-insert the previously deleted text."""
        self.editor.insert(self.position, self._deleted)


@dataclass
class ReplaceCommand(Command):
    """Replaces a span of text with new content."""
    editor: TextEditor
    position: int
    length: int
    new_content: str
    _old_content: str = field(default="", init=False, repr=False)

    def execute(self) -> None:
        """Replace *length* characters at *position* with *new_content*."""
        self._old_content = self.editor.replace(self.position, self.length, self.new_content)

    def undo(self) -> None:
        """Restore the text to what it was before the replacement."""
        self.editor.replace(self.position, len(self.new_content), self._old_content)


# ---------------------------------------------------------------------------
# Invoker
# ---------------------------------------------------------------------------

class CommandHistory:
    """Invoker that executes commands and maintains an undo stack.

    Attributes:
        _history: Stack of executed commands (most recent last).
    """

    def __init__(self) -> None:
        self._history: list[Command] = []

    def execute(self, command: Command) -> None:
        """Execute *command* and push it onto the history stack.

        Args:
            command: The command to execute.
        """
        command.execute()
        self._history.append(command)

    def undo(self) -> bool:
        """Undo the most recent command.

        Returns:
            ``True`` if a command was undone, ``False`` if history is empty.
        """
        if not self._history:
            return False
        self._history.pop().undo()
        return True

    @property
    def history_length(self) -> int:
        """Number of commands in the undo stack."""
        return len(self._history)


# ---------------------------------------------------------------------------
# Client demonstration
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate insert/delete/replace with undo support."""
    editor = TextEditor("Hello World")
    history = CommandHistory()

    print("Initial:", editor.text)

    history.execute(InsertCommand(editor, 5, ","))
    print("After insert ',':", editor.text)

    history.execute(ReplaceCommand(editor, 7, 5, "Python"))
    print("After replace 'World'→'Python':", editor.text)

    history.execute(DeleteCommand(editor, 0, 6))
    print("After delete 'Hello,':", editor.text)

    print("\n--- Undo sequence ---")
    while history.undo():
        print("Undo →", editor.text)

    print("Fully restored:", editor.text)


if __name__ == "__main__":
    main()
