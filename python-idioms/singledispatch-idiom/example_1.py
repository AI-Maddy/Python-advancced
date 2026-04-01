"""
Example 1 — AST node visitor via singledispatch.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import singledispatch


@dataclass
class NumberNode:
    value: float


@dataclass
class AddNode:
    left: object
    right: object


@dataclass
class MulNode:
    left: object
    right: object


@dataclass
class NegateNode:
    operand: object


@singledispatch
def evaluate(node: object) -> float:
    raise TypeError(f"Cannot evaluate node: {type(node)}")


@evaluate.register(NumberNode)
def _eval_number(node: NumberNode) -> float:
    return node.value


@evaluate.register(AddNode)
def _eval_add(node: AddNode) -> float:
    return evaluate(node.left) + evaluate(node.right)


@evaluate.register(MulNode)
def _eval_mul(node: MulNode) -> float:
    return evaluate(node.left) * evaluate(node.right)


@evaluate.register(NegateNode)
def _eval_negate(node: NegateNode) -> float:
    return -evaluate(node.operand)


def main() -> None:
    # (2 + 3) * -4 = -20
    expr = MulNode(
        left=AddNode(NumberNode(2), NumberNode(3)),
        right=NegateNode(NumberNode(4))
    )
    result = evaluate(expr)
    print(f"(2 + 3) * -4 = {result}")
    assert result == -20.0


if __name__ == "__main__":
    main()
