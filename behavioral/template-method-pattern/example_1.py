"""Template Method Pattern — Example 1: Report Generation.

Different report formats (text, HTML, Markdown) share the same pipeline:
collect_data → format_header → format_body → format_footer → output.
"""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ReportData:
    title: str
    rows: list[dict[str, str]]


class ReportGenerator(ABC):
    """Abstract report generator — template method is ``generate()``."""

    def generate(self, data: ReportData) -> str:
        """Template method: header + body + footer."""
        parts = [
            self.format_header(data.title),
            self.format_body(data.rows),
            self.format_footer(),
        ]
        return "\n".join(parts)

    @abstractmethod
    def format_header(self, title: str) -> str: ...
    @abstractmethod
    def format_body(self, rows: list[dict[str, str]]) -> str: ...
    @abstractmethod
    def format_footer(self) -> str: ...


class TextReportGenerator(ReportGenerator):
    def format_header(self, title: str) -> str:
        return f"{'='*40}\n{title.upper()}\n{'='*40}"

    def format_body(self, rows: list[dict[str, str]]) -> str:
        lines = []
        for row in rows:
            lines.append("  " + " | ".join(f"{k}: {v}" for k, v in row.items()))
        return "\n".join(lines)

    def format_footer(self) -> str:
        return "--- End of Report ---"


class HTMLReportGenerator(ReportGenerator):
    def format_header(self, title: str) -> str:
        return f"<html><body><h1>{title}</h1>"

    def format_body(self, rows: list[dict[str, str]]) -> str:
        cells = "".join(
            "<tr>" + "".join(f"<td>{v}</td>" for v in row.values()) + "</tr>"
            for row in rows
        )
        return f"<table>{cells}</table>"

    def format_footer(self) -> str:
        return "</body></html>"


class MarkdownReportGenerator(ReportGenerator):
    def format_header(self, title: str) -> str:
        return f"# {title}"

    def format_body(self, rows: list[dict[str, str]]) -> str:
        if not rows:
            return ""
        headers = list(rows[0].keys())
        header_row = "| " + " | ".join(headers) + " |"
        separator = "| " + " | ".join("---" for _ in headers) + " |"
        data_rows = [
            "| " + " | ".join(row.get(h, "") for h in headers) + " |"
            for row in rows
        ]
        return "\n".join([header_row, separator] + data_rows)

    def format_footer(self) -> str:
        return "\n*Generated report*"


def main() -> None:
    data = ReportData(
        title="Q1 Sales Report",
        rows=[
            {"product": "Widget A", "units": "120", "revenue": "$1200"},
            {"product": "Widget B", "units": "80", "revenue": "$960"},
        ],
    )

    for gen in (TextReportGenerator(), HTMLReportGenerator(), MarkdownReportGenerator()):
        print(f"\n=== {type(gen).__name__} ===")
        print(gen.generate(data))


if __name__ == "__main__":
    main()
