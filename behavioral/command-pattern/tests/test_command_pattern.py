"""Tests for the Command Pattern implementation."""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from command_pattern import (
    Command,
    CommandHistory,
    DeleteCommand,
    InsertCommand,
    ReplaceCommand,
    TextEditor,
)


# ---------------------------------------------------------------------------
# TextEditor receiver tests
# ---------------------------------------------------------------------------

class TestTextEditor:
    def test_insert(self) -> None:
        ed = TextEditor("Hello World")
        ed.insert(5, ",")
        assert ed.text == "Hello, World"

    def test_delete(self) -> None:
        ed = TextEditor("Hello World")
        deleted = ed.delete(5, 6)
        assert deleted == " World"
        assert ed.text == "Hello"

    def test_replace(self) -> None:
        ed = TextEditor("Hello World")
        old = ed.replace(6, 5, "Python")
        assert old == "World"
        assert ed.text == "Hello Python"


# ---------------------------------------------------------------------------
# InsertCommand round-trip
# ---------------------------------------------------------------------------

class TestInsertCommand:
    def test_execute_inserts_text(self) -> None:
        ed = TextEditor("Hello")
        cmd = InsertCommand(ed, 5, " World")
        cmd.execute()
        assert ed.text == "Hello World"

    def test_undo_removes_inserted_text(self) -> None:
        ed = TextEditor("Hello")
        cmd = InsertCommand(ed, 5, " World")
        cmd.execute()
        cmd.undo()
        assert ed.text == "Hello"

    def test_interface_contract(self) -> None:
        assert isinstance(InsertCommand(TextEditor(), 0, "x"), Command)


# ---------------------------------------------------------------------------
# DeleteCommand round-trip
# ---------------------------------------------------------------------------

class TestDeleteCommand:
    def test_execute_deletes_text(self) -> None:
        ed = TextEditor("Hello World")
        cmd = DeleteCommand(ed, 5, 6)
        cmd.execute()
        assert ed.text == "Hello"

    def test_undo_restores_deleted_text(self) -> None:
        ed = TextEditor("Hello World")
        cmd = DeleteCommand(ed, 5, 6)
        cmd.execute()
        cmd.undo()
        assert ed.text == "Hello World"


# ---------------------------------------------------------------------------
# ReplaceCommand round-trip
# ---------------------------------------------------------------------------

class TestReplaceCommand:
    def test_execute_replaces_text(self) -> None:
        ed = TextEditor("Hello World")
        cmd = ReplaceCommand(ed, 6, 5, "Python")
        cmd.execute()
        assert ed.text == "Hello Python"

    def test_undo_restores_original(self) -> None:
        ed = TextEditor("Hello World")
        cmd = ReplaceCommand(ed, 6, 5, "Python")
        cmd.execute()
        cmd.undo()
        assert ed.text == "Hello World"


# ---------------------------------------------------------------------------
# CommandHistory (Invoker)
# ---------------------------------------------------------------------------

class TestCommandHistory:
    def test_history_length_increases_on_execute(self) -> None:
        ed = TextEditor("abc")
        hist = CommandHistory()
        hist.execute(InsertCommand(ed, 3, "d"))
        hist.execute(InsertCommand(ed, 4, "e"))
        assert hist.history_length == 2

    def test_undo_decreases_history_length(self) -> None:
        ed = TextEditor("abc")
        hist = CommandHistory()
        hist.execute(InsertCommand(ed, 3, "d"))
        hist.undo()
        assert hist.history_length == 0

    def test_undo_returns_false_when_empty(self) -> None:
        hist = CommandHistory()
        assert hist.undo() is False

    def test_multi_undo_sequence(self) -> None:
        initial = "Hello"
        ed = TextEditor(initial)
        hist = CommandHistory()
        hist.execute(InsertCommand(ed, 5, " World"))
        hist.execute(ReplaceCommand(ed, 6, 5, "Python"))
        hist.execute(DeleteCommand(ed, 0, 6))
        # undo all three
        while hist.undo():
            pass
        assert ed.text == initial

    def test_abc_not_instantiable(self) -> None:
        with pytest.raises(TypeError):
            Command()  # type: ignore[abstract]
