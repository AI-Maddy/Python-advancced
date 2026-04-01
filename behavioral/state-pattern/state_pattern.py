"""State Pattern — lets an object alter its behaviour when its internal state changes.

The object will appear to change its class.  Instead of sprawling ``if``/``elif``
chains inside a single class, each state is a separate class that handles the
context's behaviour for that state.

Python-specific notes:
- ABC + @abstractmethod enforces the ``handle(context)`` contract.
- The context stores the current state object and delegates behaviour to it.
- States can transition the context by calling ``context.set_state()``.
- ``__repr__`` on each state gives readable debugging output.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Abstract state
# ---------------------------------------------------------------------------

class State(ABC):
    """Abstract base class for traffic-light states."""

    @abstractmethod
    def handle(self, context: TrafficLight) -> None:
        """React to a transition request and update *context* state.

        Args:
            context: The ``TrafficLight`` whose state may be changed.
        """

    @abstractmethod
    def __repr__(self) -> str: ...


# ---------------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------------

class TrafficLight:
    """Context that delegates behaviour to the current ``State``.

    Attributes:
        _state: The current state object.
    """

    def __init__(self) -> None:
        self._state: State = RedState()

    @property
    def state(self) -> State:
        """The current state object."""
        return self._state

    def set_state(self, state: State) -> None:
        """Transition to a new *state*.

        Args:
            state: The new state object.
        """
        print(f"  TrafficLight: {self._state!r} → {state!r}")
        self._state = state

    def request(self) -> None:
        """Ask the current state to handle a cycle tick."""
        self._state.handle(self)


# ---------------------------------------------------------------------------
# Concrete states
# ---------------------------------------------------------------------------

class RedState(State):
    """Red light — stop.  Transitions to GreenState."""

    def handle(self, context: TrafficLight) -> None:
        print("  🔴 RED — Stop")
        context.set_state(GreenState())

    def __repr__(self) -> str:
        return "RedState"


class YellowState(State):
    """Yellow light — prepare to stop.  Transitions to RedState."""

    def handle(self, context: TrafficLight) -> None:
        print("  🟡 YELLOW — Caution")
        context.set_state(RedState())

    def __repr__(self) -> str:
        return "YellowState"


class GreenState(State):
    """Green light — go.  Transitions to YellowState."""

    def handle(self, context: TrafficLight) -> None:
        print("  🟢 GREEN — Go")
        context.set_state(YellowState())

    def __repr__(self) -> str:
        return "GreenState"


# ---------------------------------------------------------------------------
# Client demonstration
# ---------------------------------------------------------------------------

def main() -> None:
    """Cycle through a traffic light sequence."""
    light = TrafficLight()
    print(f"Initial state: {light.state!r}\n")

    for cycle in range(1, 7):
        print(f"Cycle {cycle}:")
        light.request()


if __name__ == "__main__":
    main()
