"""
Example 1 — Nested context managers for temporary file operations.
"""
from __future__ import annotations

import contextlib
import os
import tempfile

from context_manager import FileManager, Timer


def main() -> None:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
        tmp.write("Hello from context manager!\n")
        tmp_path = tmp.name

    try:
        with Timer() as t:
            with FileManager(tmp_path) as f:
                content = f.read()
        print(f"Read {len(content)} chars in {t.elapsed:.6f}s")
        print(f"Content: {content.strip()!r}")

        # Suppress on missing file
        with contextlib.suppress(FileNotFoundError):
            with FileManager("/no/such/file.txt") as f:
                f.read()
        print("No exception from missing file (suppressed)")

    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    main()
