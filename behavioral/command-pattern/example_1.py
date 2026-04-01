"""Command Pattern — Example 1: Text Editor with Full Undo/Redo.

Shows a text editor session with multiple edits followed by undo operations,
demonstrating the full round-trip for all three command types.
"""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from command_pattern import (
    CommandHistory,
    DeleteCommand,
    InsertCommand,
    ReplaceCommand,
    TextEditor,
)


def main() -> None:
    editor = TextEditor()
    history = CommandHistory()

    def show(label: str) -> None:
        print(f"  [{label}] '{editor.text}'")

    # Build up a document step by step
    history.execute(InsertCommand(editor, 0, "The quick brown fox"))
    show("after insert 1")

    history.execute(InsertCommand(editor, 19, " jumps over the lazy dog"))
    show("after insert 2")

    history.execute(ReplaceCommand(editor, 4, 5, "slow"))
    show("after replace 'quick'→'slow'")

    history.execute(DeleteCommand(editor, 0, 4))
    show("after delete 'The '")

    print(f"\n  History depth: {history.history_length}")

    print("\n--- Undo steps ---")
    while history.undo():
        show("undo")


if __name__ == "__main__":
    main()
