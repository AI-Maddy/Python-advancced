"""Interpreter Pattern — defines a grammar and an interpreter for that grammar.

The Interpreter pattern defines a representation for a language's grammar
along with an interpreter that uses that representation to interpret sentences
in the language.

Python-specific notes:
- ABC + @abstractmethod enforces the ``interpret(context)`` contract.
- ``Context`` is a simple dict that maps variable names to values, allowing
  variable expressions without a separate symbol-table class.
- Composite expressions recursively call ``interpret`` on their children.
- Python's operator overloading (``__add__``, ``__mul__``) could be used but
  is avoided here to keep the pattern explicit.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


# ---------------------------------------------------------------------------
# Context type
# ---------------------------------------------------------------------------

Context = dict[str, Any]


# ---------------------------------------------------------------------------
# Abstract expression
# ---------------------------------------------------------------------------

class Expression(ABC):
    """Abstract expression in the arithmetic language grammar."""

    @abstractmethod
    def interpret(self, context: Context) -> int | float:
        """Evaluate this expression using *context*.

        Args:
            context: A mapping of variable names to their current values.

        Returns:
            The numeric result of evaluating this expression.
        """


# ---------------------------------------------------------------------------
# Terminal expressions
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class NumberExpression(Expression):
    """A literal numeric terminal.

    Attributes:
        value: The numeric value of this terminal.
    """
    value: int | float

    def interpret(self, context: Context) -> int | float:
        return self.value


@dataclass(frozen=True)
class VariableExpression(Expression):
    """A variable reference resolved from the context.

    Attributes:
        name: The variable name to look up in the context.
    """
    name: str

    def interpret(self, context: Context) -> int | float:
        if self.name not in context:
            raise KeyError(f"Undefined variable: {self.name!r}")
        return context[self.name]


# ---------------------------------------------------------------------------
# Non-terminal (composite) expressions
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AddExpression(Expression):
    """Non-terminal that represents the addition of two sub-expressions."""
    left: Expression
    right: Expression

    def interpret(self, context: Context) -> int | float:
        return self.left.interpret(context) + self.right.interpret(context)


@dataclass(frozen=True)
class SubtractExpression(Expression):
    """Non-terminal that represents the subtraction of two sub-expressions."""
    left: Expression
    right: Expression

    def interpret(self, context: Context) -> int | float:
        return self.left.interpret(context) - self.right.interpret(context)


@dataclass(frozen=True)
class MultiplyExpression(Expression):
    """Non-terminal that represents the multiplication of two sub-expressions."""
    left: Expression
    right: Expression

    def interpret(self, context: Context) -> int | float:
        return self.left.interpret(context) * self.right.interpret(context)


@dataclass(frozen=True)
class DivideExpression(Expression):
    """Non-terminal that represents the division of two sub-expressions."""
    left: Expression
    right: Expression

    def interpret(self, context: Context) -> float:
        divisor = self.right.interpret(context)
        if divisor == 0:
            raise ZeroDivisionError("Division by zero in expression")
        return self.left.interpret(context) / divisor


# ---------------------------------------------------------------------------
# Simple expression parser (token-based recursive descent)
# ---------------------------------------------------------------------------

class ExpressionParser:
    """Parses a simple arithmetic string into an ``Expression`` tree.

    Supported grammar::

        expr   := term (('+' | '-') term)*
        term   := factor (('*' | '/') factor)*
        factor := NUMBER | IDENT | '(' expr ')'
    """

    def __init__(self, text: str) -> None:
        self._tokens = self._tokenise(text)
        self._pos = 0

    @staticmethod
    def _tokenise(text: str) -> list[str]:
        import re
        return re.findall(r"\d+\.?\d*|[+\-*/()]|\w+", text)

    def parse(self) -> Expression:
        """Parse and return the root ``Expression``."""
        expr = self._parse_expr()
        if self._pos != len(self._tokens):
            raise SyntaxError(f"Unexpected token: {self._tokens[self._pos]!r}")
        return expr

    def _peek(self) -> str | None:
        return self._tokens[self._pos] if self._pos < len(self._tokens) else None

    def _consume(self) -> str:
        token = self._tokens[self._pos]
        self._pos += 1
        return token

    def _parse_expr(self) -> Expression:
        left = self._parse_term()
        while self._peek() in ("+", "-"):
            op = self._consume()
            right = self._parse_term()
            left = AddExpression(left, right) if op == "+" else SubtractExpression(left, right)
        return left

    def _parse_term(self) -> Expression:
        left = self._parse_factor()
        while self._peek() in ("*", "/"):
            op = self._consume()
            right = self._parse_factor()
            left = MultiplyExpression(left, right) if op == "*" else DivideExpression(left, right)
        return left

    def _parse_factor(self) -> Expression:
        token = self._peek()
        if token is None:
            raise SyntaxError("Unexpected end of expression")
        if token == "(":
            self._consume()
            expr = self._parse_expr()
            if self._consume() != ")":
                raise SyntaxError("Expected ')'")
            return expr
        self._consume()
        try:
            return NumberExpression(float(token) if "." in token else int(token))
        except ValueError:
            return VariableExpression(token)


# ---------------------------------------------------------------------------
# Client demonstration
# ---------------------------------------------------------------------------

def main() -> None:
    """Build and evaluate several arithmetic expression trees."""
    ctx: Context = {"x": 5, "y": 3}

    # Manual construction: (x + 2) * (y - 1)
    expr = MultiplyExpression(
        AddExpression(VariableExpression("x"), NumberExpression(2)),
        SubtractExpression(VariableExpression("y"), NumberExpression(1)),
    )
    result = expr.interpret(ctx)
    print(f"(x+2)*(y-1) = {result}")  # (5+2)*(3-1) = 14

    # Parser: 3 + 4 * 2
    tree = ExpressionParser("3 + 4 * 2").parse()
    print(f"3 + 4 * 2 = {tree.interpret({})}")  # 11

    # Parser: (3 + 4) * 2
    tree2 = ExpressionParser("(3 + 4) * 2").parse()
    print(f"(3 + 4) * 2 = {tree2.interpret({})}")  # 14

    # Parser with variable
    tree3 = ExpressionParser("x * y + 1").parse()
    print(f"x * y + 1 = {tree3.interpret(ctx)}")  # 16


if __name__ == "__main__":
    main()
