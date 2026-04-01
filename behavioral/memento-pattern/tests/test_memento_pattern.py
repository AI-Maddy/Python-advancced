"""Tests for the Memento Pattern implementation."""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from memento_pattern import Caretaker, Memento, Originator


class TestMemento:
    def test_frozen_immutable(self) -> None:
        m = Memento(state="hello")
        with pytest.raises((AttributeError, TypeError)):
            m.state = "changed"  # type: ignore[misc]

    def test_stores_state(self) -> None:
        m = Memento(state=42)
        assert m.state == 42


class TestOriginator:
    def test_save_captures_state(self) -> None:
        orig = Originator("initial")
        memo = orig.save()
        assert memo.state == "initial"

    def test_restore_resets_state(self) -> None:
        orig = Originator("initial")
        memo = orig.save()
        orig.state = "changed"
        orig.restore(memo)
        assert orig.state == "initial"

    def test_save_is_deep_copy(self) -> None:
        data = [1, 2, 3]
        orig = Originator(data)
        memo = orig.save()
        data.append(4)
        orig.state = data
        # Memento should still hold the old state
        assert memo.state == [1, 2, 3]

    def test_restore_does_not_alias_memento(self) -> None:
        orig = Originator([1, 2])
        memo = orig.save()
        orig.restore(memo)
        orig.state.append(99)
        # Memento should be unaffected
        assert memo.state == [1, 2]


class TestCaretaker:
    def test_history_grows_on_save(self) -> None:
        orig = Originator(0)
        care = Caretaker(orig)
        care.save()
        care.save()
        assert care.history_length == 2

    def test_undo_restores_last_save(self) -> None:
        orig = Originator("v1")
        care = Caretaker(orig)
        care.save()
        orig.state = "v2"
        care.save()
        orig.state = "v3"
        care.undo()
        assert orig.state == "v2"

    def test_undo_returns_false_when_empty(self) -> None:
        care = Caretaker(Originator(0))
        assert care.undo() is False

    def test_full_undo_to_original(self) -> None:
        orig = Originator("start")
        care = Caretaker(orig)
        care.save()
        for new_state in ("a", "b", "c"):
            orig.state = new_state
            care.save()
        while care.undo():
            pass
        assert orig.state == "start"

    def test_history_length_decreases_on_undo(self) -> None:
        orig = Originator(0)
        care = Caretaker(orig)
        care.save()
        care.save()
        care.undo()
        assert care.history_length == 1
