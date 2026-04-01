"""Memento Pattern — captures and restores object state without violating encapsulation.

The Memento pattern lets you save and restore the previous state of an object
without revealing the details of its implementation.

Python-specific notes:
- A ``Memento`` is a frozen (immutable) snapshot — use ``@dataclass(frozen=True)``
  or a ``NamedTuple``.
- The ``Originator`` creates and consumes mementos; the ``Caretaker`` merely
  stores them.
- ``copy.deepcopy`` is used to ensure snapshots are independent of later
  state changes.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


# ---------------------------------------------------------------------------
# Memento — frozen snapshot
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Memento:
    """Immutable snapshot of an Originator's state.

    Attributes:
        state:     The captured state data.
        timestamp: When the snapshot was taken.
    """
    state: Any
    timestamp: datetime = field(default_factory=datetime.now)

    def __repr__(self) -> str:
        return f"Memento(state={self.state!r}, at={self.timestamp:%H:%M:%S})"


# ---------------------------------------------------------------------------
# Originator
# ---------------------------------------------------------------------------

class Originator:
    """The object whose state can be saved and restored.

    Attributes:
        _state: Current internal state (mutable).
    """

    def __init__(self, initial: Any = None) -> None:
        self._state: Any = initial

    @property
    def state(self) -> Any:
        """Current state (read-only view)."""
        return self._state

    @state.setter
    def state(self, value: Any) -> None:
        """Update the internal state."""
        self._state = value

    def save(self) -> Memento:
        """Capture a deep-copy snapshot of the current state.

        Returns:
            A new ``Memento`` containing the current state.
        """
        return Memento(state=copy.deepcopy(self._state))

    def restore(self, memento: Memento) -> None:
        """Restore state from *memento*.

        Args:
            memento: A previously saved ``Memento``.
        """
        self._state = copy.deepcopy(memento.state)

    def __repr__(self) -> str:
        return f"Originator(state={self._state!r})"


# ---------------------------------------------------------------------------
# Caretaker
# ---------------------------------------------------------------------------

class Caretaker:
    """Manages the undo history of ``Memento`` objects.

    The Caretaker never inspects or modifies the contents of mementos.

    Attributes:
        _originator: The object being managed.
        _history:    Stack of saved mementos (most recent last).
    """

    def __init__(self, originator: Originator) -> None:
        self._originator = originator
        self._history: list[Memento] = []

    def save(self) -> None:
        """Save the originator's current state to the history stack."""
        memo = self._originator.save()
        self._history.append(memo)
        print(f"  [Caretaker] Saved: {memo}")

    def undo(self) -> bool:
        """Restore the originator to its most recently saved state.

        Returns:
            ``True`` if a restore was performed; ``False`` if history is empty.
        """
        if not self._history:
            return False
        memo = self._history.pop()
        self._originator.restore(memo)
        print(f"  [Caretaker] Restored: {memo}")
        return True

    @property
    def history_length(self) -> int:
        """Number of saved snapshots."""
        return len(self._history)


# ---------------------------------------------------------------------------
# Client demonstration
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate save/restore on a simple string state."""
    orig = Originator("Initial state")
    care = Caretaker(orig)

    care.save()
    orig.state = "State after first change"
    care.save()
    orig.state = "State after second change"
    care.save()
    orig.state = "Oops — bad state"

    print(f"\nCurrent: {orig}")
    print(f"History depth: {care.history_length}\n")

    care.undo()
    print(f"After undo 1: {orig.state}")
    care.undo()
    print(f"After undo 2: {orig.state}")
    care.undo()
    print(f"After undo 3: {orig.state}")
    print(f"Further undo: {care.undo()}")


if __name__ == "__main__":
    main()
