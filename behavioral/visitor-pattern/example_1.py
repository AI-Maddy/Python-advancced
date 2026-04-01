"""Visitor Pattern — Example 1: AST Node Visitor.

A minimal arithmetic AST (Number, BinaryOp) is traversed by:
- EvalVisitor (evaluates to a number)
- PrettyPrintVisitor (converts to string)
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# AST nodes
# ---------------------------------------------------------------------------

class ASTNode(ABC):
    @abstractmethod
    def accept(self, visitor: ASTVisitor) -> object: ...


class ASTVisitor(ABC):
    @abstractmethod
    def visit_number(self, node: NumberNode) -> object: ...
    @abstractmethod
    def visit_binop(self, node: BinOpNode) -> object: ...


@dataclass
class NumberNode(ASTNode):
    value: float

    def accept(self, visitor: ASTVisitor) -> object:
        return visitor.visit_number(self)


@dataclass
class BinOpNode(ASTNode):
    op: str       # '+', '-', '*', '/'
    left: ASTNode
    right: ASTNode

    def accept(self, visitor: ASTVisitor) -> object:
        return visitor.visit_binop(self)


# ---------------------------------------------------------------------------
# Visitors
# ---------------------------------------------------------------------------

class EvalVisitor(ASTVisitor):
    """Evaluates the AST to a numeric result."""

    def visit_number(self, node: NumberNode) -> float:
        return node.value

    def visit_binop(self, node: BinOpNode) -> float:
        left = float(node.left.accept(self))  # type: ignore[arg-type]
        right = float(node.right.accept(self))  # type: ignore[arg-type]
        ops = {"+": left + right, "-": left - right, "*": left * right}
        if node.op == "/":
            return left / right
        return ops[node.op]


class PrettyPrintVisitor(ASTVisitor):
    """Converts the AST to an infix string."""

    def visit_number(self, node: NumberNode) -> str:
        return str(node.value)

    def visit_binop(self, node: BinOpNode) -> str:
        left = node.left.accept(self)
        right = node.right.accept(self)
        return f"({left} {node.op} {right})"


def main() -> None:
    # Build AST for: (3 + 4) * (10 - 2)
    ast = BinOpNode(
        "*",
        BinOpNode("+", NumberNode(3), NumberNode(4)),
        BinOpNode("-", NumberNode(10), NumberNode(2)),
    )

    printer = PrettyPrintVisitor()
    evaluator = EvalVisitor()

    expr_str = ast.accept(printer)
    result = ast.accept(evaluator)
    print(f"Expression: {expr_str}")
    print(f"Result:     {result}")
    assert result == 56.0


if __name__ == "__main__":
    main()
