"""Tests for the Chain of Responsibility Pattern implementation."""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from chain_of_responsibility_pattern import (
    Handler,
    HighPriorityHandler,
    LowPriorityHandler,
    MediumPriorityHandler,
    Request,
)


def build_chain() -> LowPriorityHandler:
    low = LowPriorityHandler()
    medium = MediumPriorityHandler()
    high = HighPriorityHandler()
    low.set_next(medium).set_next(high)
    return low


class TestChainRouting:
    def test_low_priority_handled_by_low(self) -> None:
        chain = build_chain()
        result = chain.handle(Request(1, "low task"))
        assert result is not None
        assert "Low" in result

    def test_medium_priority_handled_by_medium(self) -> None:
        chain = build_chain()
        result = chain.handle(Request(2, "medium task"))
        assert result is not None
        assert "Medium" in result

    def test_high_priority_handled_by_high(self) -> None:
        chain = build_chain()
        result = chain.handle(Request(3, "high task"))
        assert result is not None
        assert "High" in result

    def test_unhandled_returns_none(self) -> None:
        chain = build_chain()
        result = chain.handle(Request(99, "unknown priority"))
        assert result is None

    def test_fluent_chaining(self) -> None:
        low = LowPriorityHandler()
        medium = MediumPriorityHandler()
        high = HighPriorityHandler()
        returned = low.set_next(medium)
        assert returned is medium
        returned2 = medium.set_next(high)
        assert returned2 is high

    def test_single_handler_handles_its_level(self) -> None:
        handler = HighPriorityHandler()
        result = handler.handle(Request(3, "only high"))
        assert result is not None

    def test_single_handler_returns_none_for_out_of_range(self) -> None:
        handler = LowPriorityHandler()
        result = handler.handle(Request(2, "too high for low"))
        assert result is None

    def test_abc_not_instantiable(self) -> None:
        with pytest.raises(TypeError):
            Handler()  # type: ignore[abstract]

    def test_interface_contract(self) -> None:
        for HandlerClass in (LowPriorityHandler, MediumPriorityHandler, HighPriorityHandler):
            h = HandlerClass()
            assert isinstance(h, Handler)
