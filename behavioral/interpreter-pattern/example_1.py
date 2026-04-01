"""Interpreter Pattern — Example 1: Math Expression Parser.

Demonstrates the full expression parser on a variety of arithmetic
expressions, including variable substitution and operator precedence.
"""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interpreter_pattern import Context, ExpressionParser


def evaluate(expr_str: str, context: Context | None = None) -> object:
    ctx = context or {}
    tree = ExpressionParser(expr_str).parse()
    result = tree.interpret(ctx)
    print(f"  {expr_str!r:30s} = {result}")
    return result


def main() -> None:
    print("=== Pure numeric expressions ===")
    assert evaluate("1 + 2") == 3
    assert evaluate("10 - 3") == 7
    assert evaluate("4 * 5") == 20
    assert evaluate("10 / 4") == 2.5
    assert evaluate("3 + 4 * 2") == 11        # precedence
    assert evaluate("(3 + 4) * 2") == 14      # grouping
    assert evaluate("2 * 3 + 4 * 5") == 26

    print("\n=== Variable expressions ===")
    ctx: Context = {"a": 10, "b": 4}
    assert evaluate("a + b", ctx) == 14
    assert evaluate("a * b - 2", ctx) == 38
    assert evaluate("(a + b) / 2", ctx) == 7.0

    print("\nAll assertions passed.")


if __name__ == "__main__":
    main()
