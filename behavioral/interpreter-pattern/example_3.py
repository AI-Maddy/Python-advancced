"""Interpreter Pattern — Example 3: Simple Template Engine.

A minimal template engine that resolves ``{{variable}}`` placeholders in
a string using the Interpreter pattern.  Each token in the template is an
expression that either returns its literal text or looks up a variable.
"""
from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass


TemplateContext = dict[str, str]


class TemplateExpr(ABC):
    @abstractmethod
    def interpret(self, ctx: TemplateContext) -> str: ...


@dataclass(frozen=True)
class LiteralText(TemplateExpr):
    text: str
    def interpret(self, ctx: TemplateContext) -> str:
        return self.text


@dataclass(frozen=True)
class VariablePlaceholder(TemplateExpr):
    name: str
    default: str = ""
    def interpret(self, ctx: TemplateContext) -> str:
        return ctx.get(self.name, self.default)


class SequenceExpr(TemplateExpr):
    """Concatenates a list of template expressions."""
    def __init__(self, parts: list[TemplateExpr]) -> None:
        self._parts = parts

    def interpret(self, ctx: TemplateContext) -> str:
        return "".join(part.interpret(ctx) for part in self._parts)


class TemplateParser:
    """Parses a template string into a ``SequenceExpr``."""
    PLACEHOLDER = re.compile(r"\{\{(\w+)\}\}")

    def parse(self, template: str) -> SequenceExpr:
        parts: list[TemplateExpr] = []
        last = 0
        for m in self.PLACEHOLDER.finditer(template):
            if m.start() > last:
                parts.append(LiteralText(template[last : m.start()]))
            parts.append(VariablePlaceholder(m.group(1)))
            last = m.end()
        if last < len(template):
            parts.append(LiteralText(template[last:]))
        return SequenceExpr(parts)


def render(template: str, ctx: TemplateContext) -> str:
    parser = TemplateParser()
    expr = parser.parse(template)
    return expr.interpret(ctx)


def main() -> None:
    templates = [
        ("Hello, {{name}}!", {"name": "Alice"}),
        ("Dear {{title}} {{last_name}},", {"title": "Dr.", "last_name": "Smith"}),
        (
            "Order #{{order_id}} for {{customer}} — Total: ${{total}}",
            {"order_id": "1042", "customer": "Bob", "total": "129.99"},
        ),
        ("Missing {{undefined}} variable", {}),
    ]

    for tmpl, ctx in templates:
        result = render(tmpl, ctx)
        print(f"  Template: {tmpl!r}")
        print(f"  Result:   {result!r}\n")


if __name__ == "__main__":
    main()
