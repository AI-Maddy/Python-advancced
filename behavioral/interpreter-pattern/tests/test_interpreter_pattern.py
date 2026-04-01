"""Tests for the Interpreter Pattern implementation."""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from interpreter_pattern import (
    AddExpression,
    Context,
    DivideExpression,
    Expression,
    ExpressionParser,
    MultiplyExpression,
    NumberExpression,
    SubtractExpression,
    VariableExpression,
)


# ---------------------------------------------------------------------------
# Terminal expressions
# ---------------------------------------------------------------------------

class TestNumberExpression:
    def test_integer(self) -> None:
        assert NumberExpression(42).interpret({}) == 42

    def test_float(self) -> None:
        assert NumberExpression(3.14).interpret({}) == pytest.approx(3.14)

    def test_zero(self) -> None:
        assert NumberExpression(0).interpret({}) == 0


class TestVariableExpression:
    def test_resolved_from_context(self) -> None:
        assert VariableExpression("x").interpret({"x": 10}) == 10

    def test_raises_for_undefined(self) -> None:
        with pytest.raises(KeyError):
            VariableExpression("z").interpret({})


# ---------------------------------------------------------------------------
# Composite expressions
# ---------------------------------------------------------------------------

class TestAddExpression:
    def test_add_two_numbers(self) -> None:
        expr = AddExpression(NumberExpression(3), NumberExpression(4))
        assert expr.interpret({}) == 7

    def test_add_with_variable(self) -> None:
        expr = AddExpression(VariableExpression("x"), NumberExpression(1))
        assert expr.interpret({"x": 9}) == 10


class TestSubtractExpression:
    def test_subtract(self) -> None:
        expr = SubtractExpression(NumberExpression(10), NumberExpression(3))
        assert expr.interpret({}) == 7

    def test_negative_result(self) -> None:
        expr = SubtractExpression(NumberExpression(3), NumberExpression(10))
        assert expr.interpret({}) == -7


class TestMultiplyExpression:
    def test_multiply(self) -> None:
        expr = MultiplyExpression(NumberExpression(6), NumberExpression(7))
        assert expr.interpret({}) == 42


class TestDivideExpression:
    def test_divide(self) -> None:
        expr = DivideExpression(NumberExpression(10), NumberExpression(4))
        assert expr.interpret({}) == pytest.approx(2.5)

    def test_divide_by_zero(self) -> None:
        with pytest.raises(ZeroDivisionError):
            DivideExpression(NumberExpression(1), NumberExpression(0)).interpret({})


# ---------------------------------------------------------------------------
# Nested / composite trees
# ---------------------------------------------------------------------------

class TestNestedExpressions:
    def test_operator_precedence_via_manual_tree(self) -> None:
        # (3 + 4) * 2 = 14
        expr = MultiplyExpression(
            AddExpression(NumberExpression(3), NumberExpression(4)),
            NumberExpression(2),
        )
        assert expr.interpret({}) == 14

    def test_variable_in_tree(self) -> None:
        ctx: Context = {"a": 5, "b": 3}
        expr = AddExpression(VariableExpression("a"), VariableExpression("b"))
        assert expr.interpret(ctx) == 8


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

class TestExpressionParser:
    def test_simple_addition(self) -> None:
        assert ExpressionParser("1 + 2").parse().interpret({}) == 3

    def test_precedence_mul_before_add(self) -> None:
        assert ExpressionParser("3 + 4 * 2").parse().interpret({}) == 11

    def test_grouping_overrides_precedence(self) -> None:
        assert ExpressionParser("(3 + 4) * 2").parse().interpret({}) == 14

    def test_variable_resolution(self) -> None:
        result = ExpressionParser("x + 1").parse().interpret({"x": 9})
        assert result == 10

    def test_float_literal(self) -> None:
        result = ExpressionParser("1.5 + 0.5").parse().interpret({})
        assert result == pytest.approx(2.0)


# ---------------------------------------------------------------------------
# ABC
# ---------------------------------------------------------------------------

def test_abc_not_instantiable() -> None:
    with pytest.raises(TypeError):
        Expression()  # type: ignore[abstract]
