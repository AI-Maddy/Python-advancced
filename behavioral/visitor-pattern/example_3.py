"""Visitor Pattern — Example 3: Document Exporter.

A document tree (Heading, Paragraph, Image) can be exported to multiple
formats (plain text, Markdown, HTML) via separate visitor classes.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class ExportVisitor(ABC):
    @abstractmethod
    def visit_heading(self, node: Heading) -> str: ...
    @abstractmethod
    def visit_paragraph(self, node: Paragraph) -> str: ...
    @abstractmethod
    def visit_image(self, node: Image) -> str: ...


class DocNode(ABC):
    @abstractmethod
    def accept(self, visitor: ExportVisitor) -> str: ...


@dataclass
class Heading(DocNode):
    text: str
    level: int = 1

    def accept(self, visitor: ExportVisitor) -> str:
        return visitor.visit_heading(self)


@dataclass
class Paragraph(DocNode):
    text: str

    def accept(self, visitor: ExportVisitor) -> str:
        return visitor.visit_paragraph(self)


@dataclass
class Image(DocNode):
    src: str
    alt: str = ""

    def accept(self, visitor: ExportVisitor) -> str:
        return visitor.visit_image(self)


class PlainTextExporter(ExportVisitor):
    def visit_heading(self, node: Heading) -> str:
        return f"{'#' * node.level} {node.text}\n"

    def visit_paragraph(self, node: Paragraph) -> str:
        return f"{node.text}\n"

    def visit_image(self, node: Image) -> str:
        return f"[Image: {node.alt} ({node.src})]\n"


class MarkdownExporter(ExportVisitor):
    def visit_heading(self, node: Heading) -> str:
        return f"{'#' * node.level} {node.text}\n"

    def visit_paragraph(self, node: Paragraph) -> str:
        return f"{node.text}\n"

    def visit_image(self, node: Image) -> str:
        return f"![{node.alt}]({node.src})\n"


class HTMLExporter(ExportVisitor):
    def visit_heading(self, node: Heading) -> str:
        return f"<h{node.level}>{node.text}</h{node.level}>"

    def visit_paragraph(self, node: Paragraph) -> str:
        return f"<p>{node.text}</p>"

    def visit_image(self, node: Image) -> str:
        return f'<img src="{node.src}" alt="{node.alt}" />'


def main() -> None:
    document: list[DocNode] = [
        Heading("Design Patterns", level=1),
        Paragraph("Design patterns are reusable solutions to common problems."),
        Heading("Observer Pattern", level=2),
        Paragraph("Defines a one-to-many dependency between objects."),
        Image("observer.png", alt="Observer UML diagram"),
    ]

    for ExporterClass in (PlainTextExporter, MarkdownExporter, HTMLExporter):
        exporter = ExporterClass()
        print(f"\n=== {type(exporter).__name__} ===")
        for node in document:
            print(node.accept(exporter))


if __name__ == "__main__":
    main()
