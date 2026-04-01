"""Tests for the State Pattern implementation."""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from state_pattern import (
    GreenState,
    RedState,
    State,
    TrafficLight,
    YellowState,
)


class TestTrafficLightTransitions:
    def test_initial_state_is_red(self) -> None:
        light = TrafficLight()
        assert isinstance(light.state, RedState)

    def test_red_transitions_to_green(self) -> None:
        light = TrafficLight()
        light.request()
        assert isinstance(light.state, GreenState)

    def test_green_transitions_to_yellow(self) -> None:
        light = TrafficLight()
        light.request()  # red → green
        light.request()  # green → yellow
        assert isinstance(light.state, YellowState)

    def test_yellow_transitions_to_red(self) -> None:
        light = TrafficLight()
        light.request()  # red → green
        light.request()  # green → yellow
        light.request()  # yellow → red
        assert isinstance(light.state, RedState)

    def test_full_cycle(self) -> None:
        light = TrafficLight()
        states: list[type[State]] = []
        for _ in range(6):
            light.request()
            states.append(type(light.state))
        expected = [GreenState, YellowState, RedState, GreenState, YellowState, RedState]
        assert states == expected

    def test_context_delegates_to_state(self) -> None:
        """Verify that calling request() actually changes state (delegation works)."""
        light = TrafficLight()
        initial = type(light.state)
        light.request()
        assert type(light.state) != initial

    def test_set_state_directly(self) -> None:
        light = TrafficLight()
        light.set_state(YellowState())
        assert isinstance(light.state, YellowState)

    def test_state_abc_not_instantiable(self) -> None:
        with pytest.raises(TypeError):
            State()  # type: ignore[abstract]
