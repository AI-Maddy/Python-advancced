"""
Example 1 — Document template cloning.

A base document template is cloned and customised for each recipient
without touching the original template.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Self


@dataclass
class DocumentTemplate:
    """Prototype document with nested sections."""
    title: str
    sections: list[str] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)

    def clone(self) -> Self:
        return copy.deepcopy(self)

    def personalise(self, recipient: str) -> None:
        self.title = self.title.replace("{{name}}", recipient)
        self.sections = [s.replace("{{name}}", recipient) for s in self.sections]
        self.metadata["recipient"] = recipient


def main() -> None:
    template = DocumentTemplate(
        title="Dear {{name}}, Welcome!",
        sections=[
            "Hello {{name}}, thank you for joining us.",
            "Your account has been created.",
        ],
        metadata={"template_version": "1.0"},
    )

    for name in ("Alice", "Bob", "Carol"):
        doc = template.clone()
        doc.personalise(name)
        print(f"--- Document for {name} ---")
        print(f"Title: {doc.title}")
        for s in doc.sections:
            print(f"  {s}")

    # Original still has placeholders
    print(f"\nOriginal title still has placeholder: {template.title}")
    assert "{{name}}" in template.title


if __name__ == "__main__":
    main()
