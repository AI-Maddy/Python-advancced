"""
Example 1 — Lazy file-line pipeline.

Read a large file lazily, filter, transform, and materialise only the needed lines.
"""
from __future__ import annotations

import io
from typing import Generator, Iterator


def read_lines(fileobj: io.TextIOBase) -> Generator[str, None, None]:
    """Yield lines from a file object lazily."""
    for line in fileobj:
        yield line.rstrip("\n")


def filter_nonempty(lines: Iterator[str]) -> Generator[str, None, None]:
    for line in lines:
        if line.strip():
            yield line


def strip_comments(lines: Iterator[str], prefix: str = "#") -> Generator[str, None, None]:
    for line in lines:
        if not line.lstrip().startswith(prefix):
            yield line


def uppercase_lines(lines: Iterator[str]) -> Generator[str, None, None]:
    for line in lines:
        yield line.upper()


def main() -> None:
    # Simulate a file with blank lines, comments, and real content
    fake_file = io.StringIO(
        "# header comment\n"
        "\n"
        "hello world\n"
        "# another comment\n"
        "python generators\n"
        "\n"
        "lazy evaluation\n"
    )

    pipeline = uppercase_lines(
        strip_comments(
            filter_nonempty(
                read_lines(fake_file)
            )
        )
    )

    print("Processed lines:")
    for line in pipeline:
        print(f"  {line!r}")


if __name__ == "__main__":
    main()
