"""Interpreter Pattern — Example 2: Boolean Query Language.

A tiny boolean expression language:
  AND(expr, expr), OR(expr, expr), NOT(expr), TRUE/FALSE, variable names.
Useful for feature flags or search filters.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


BoolContext = dict[str, bool]


class BoolExpr(ABC):
    @abstractmethod
    def interpret(self, ctx: BoolContext) -> bool: ...

    def __repr__(self) -> str:
        return type(self).__name__


@dataclass(frozen=True)
class Literal(BoolExpr):
    value: bool
    def interpret(self, ctx: BoolContext) -> bool:
        return self.value


@dataclass(frozen=True)
class Variable(BoolExpr):
    name: str
    def interpret(self, ctx: BoolContext) -> bool:
        return ctx.get(self.name, False)


@dataclass(frozen=True)
class AndExpr(BoolExpr):
    left: BoolExpr
    right: BoolExpr
    def interpret(self, ctx: BoolContext) -> bool:
        return self.left.interpret(ctx) and self.right.interpret(ctx)


@dataclass(frozen=True)
class OrExpr(BoolExpr):
    left: BoolExpr
    right: BoolExpr
    def interpret(self, ctx: BoolContext) -> bool:
        return self.left.interpret(ctx) or self.right.interpret(ctx)


@dataclass(frozen=True)
class NotExpr(BoolExpr):
    operand: BoolExpr
    def interpret(self, ctx: BoolContext) -> bool:
        return not self.operand.interpret(ctx)


def main() -> None:
    # Feature flags: show_banner AND (is_premium OR is_beta)
    query = AndExpr(
        Variable("show_banner"),
        OrExpr(Variable("is_premium"), Variable("is_beta")),
    )

    test_cases: list[tuple[BoolContext, bool]] = [
        ({"show_banner": True, "is_premium": True, "is_beta": False}, True),
        ({"show_banner": True, "is_premium": False, "is_beta": True}, True),
        ({"show_banner": False, "is_premium": True, "is_beta": True}, False),
        ({"show_banner": True, "is_premium": False, "is_beta": False}, False),
    ]

    print("Query: show_banner AND (is_premium OR is_beta)")
    for ctx, expected in test_cases:
        result = query.interpret(ctx)
        status = "OK" if result == expected else "FAIL"
        print(f"  {ctx} → {result} [{status}]")
        assert result == expected

    # NOT example
    not_expr = NotExpr(Variable("maintenance_mode"))
    print("\n  maintenance_mode=True → NOT →", not_expr.interpret({"maintenance_mode": True}))
    print("  maintenance_mode=False → NOT →", not_expr.interpret({"maintenance_mode": False}))


if __name__ == "__main__":
    main()
