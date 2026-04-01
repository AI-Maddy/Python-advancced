"""Memento Pattern — Example 1: Text Editor Undo.

A richer text editor tracks cursor position and content; each keystroke
can be undone independently.
"""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dataclasses import dataclass
from memento_pattern import Caretaker, Originator


@dataclass
class EditorState:
    """Snapshot of the editor's content and cursor."""
    content: str
    cursor: int


def main() -> None:
    editor = Originator(EditorState("", 0))
    care = Caretaker(editor)

    def type_text(text: str) -> None:
        s = editor.state
        new_content = s.content[: s.cursor] + text + s.content[s.cursor :]
        editor.state = EditorState(new_content, s.cursor + len(text))

    def show() -> None:
        s = editor.state
        print(f"  Content: '{s.content}' | Cursor: {s.cursor}")

    # User types a document
    care.save(); type_text("Hello"); show()
    care.save(); type_text(", "); show()
    care.save(); type_text("World"); show()
    care.save(); type_text("!"); show()

    print("\n--- Undo steps ---")
    while care.undo():
        show()


if __name__ == "__main__":
    main()
