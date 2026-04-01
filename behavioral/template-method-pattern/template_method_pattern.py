"""Template Method Pattern — defines the skeleton of an algorithm, deferring steps to subclasses.

The Template Method pattern defines the program skeleton of an algorithm in
an operation, deferring some steps to subclasses.  Subclasses can redefine
certain steps without changing the algorithm's structure.

Python-specific notes:
- The template method is a concrete method on the ABC; it calls ``@abstractmethod``
  hooks that subclasses must implement.
- Optional hooks can be concrete methods that do nothing by default.
- ``@final`` (Python 3.8+) can mark the template method to prevent overriding,
  but is often omitted for simplicity.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


# ---------------------------------------------------------------------------
# Abstract base with template method
# ---------------------------------------------------------------------------

class DataProcessor(ABC):
    """Abstract data processor that defines the ``process()`` template method.

    The algorithm is: ``read()`` → ``transform()`` → ``write()``.
    Subclasses implement each step; ``process()`` orchestrates the sequence.
    """

    def process(self) -> None:
        """Template method — execute the full data processing pipeline.

        The order is always: read → transform → write.
        Hooks (``before_process`` / ``after_process``) are optional.
        """
        self.before_process()
        data = self.read()
        transformed = self.transform(data)
        self.write(transformed)
        self.after_process()

    @abstractmethod
    def read(self) -> Any:
        """Read raw data from the source.

        Returns:
            Raw data in an implementation-specific form.
        """

    @abstractmethod
    def transform(self, data: Any) -> Any:
        """Transform the raw *data*.

        Args:
            data: Raw data returned by ``read()``.

        Returns:
            Transformed data ready for writing.
        """

    @abstractmethod
    def write(self, data: Any) -> None:
        """Write the transformed *data* to the destination.

        Args:
            data: Transformed data from ``transform()``.
        """

    # Optional hooks — no-ops by default
    def before_process(self) -> None:
        """Hook called before the pipeline starts (override if needed)."""

    def after_process(self) -> None:
        """Hook called after the pipeline completes (override if needed)."""


# ---------------------------------------------------------------------------
# Concrete implementations
# ---------------------------------------------------------------------------

class CSVProcessor(DataProcessor):
    """Processes CSV-like data: reads rows, uppercases all values, writes result.

    Attributes:
        source_data: List of CSV row strings (input).
        result:      List of processed rows (output).
    """

    def __init__(self, source_data: list[str]) -> None:
        self.source_data = source_data
        self.result: list[str] = []

    def read(self) -> list[list[str]]:
        """Parse CSV rows into lists of field values."""
        print("  [CSV] Reading CSV data...")
        return [row.split(",") for row in self.source_data]

    def transform(self, data: list[list[str]]) -> list[list[str]]:
        """Strip whitespace and uppercase every field."""
        print("  [CSV] Transforming (strip + uppercase)...")
        return [[field.strip().upper() for field in row] for row in data]

    def write(self, data: list[list[str]]) -> None:
        """Join fields back into CSV strings."""
        print("  [CSV] Writing output...")
        self.result = [",".join(row) for row in data]
        for row in self.result:
            print(f"    {row}")

    def before_process(self) -> None:
        print("  [CSV] Opening file handle")

    def after_process(self) -> None:
        print("  [CSV] Closing file handle")


class JSONProcessor(DataProcessor):
    """Processes JSON-like data: reads dicts, filters keys, writes summary.

    Attributes:
        records: List of dict records (input).
        result:  Filtered records (output).
    """

    def __init__(self, records: list[dict[str, Any]], keep_keys: list[str]) -> None:
        self.records = records
        self.keep_keys = keep_keys
        self.result: list[dict[str, Any]] = []

    def read(self) -> list[dict[str, Any]]:
        print("  [JSON] Reading records...")
        return list(self.records)

    def transform(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        print("  [JSON] Projecting keys:", self.keep_keys)
        return [{k: rec[k] for k in self.keep_keys if k in rec} for rec in data]

    def write(self, data: list[dict[str, Any]]) -> None:
        print("  [JSON] Writing output...")
        self.result = data
        for rec in self.result:
            print(f"    {rec}")


class XMLProcessor(DataProcessor):
    """Processes a list of tag→value pairs into a minimal XML string.

    Attributes:
        elements: List of ``(tag, value)`` tuples.
        output:   Generated XML string.
    """

    def __init__(self, elements: list[tuple[str, str]]) -> None:
        self.elements = elements
        self.output: str = ""

    def read(self) -> list[tuple[str, str]]:
        print("  [XML] Parsing elements...")
        return list(self.elements)

    def transform(self, data: list[tuple[str, str]]) -> list[str]:
        print("  [XML] Generating XML tags...")
        return [f"  <{tag}>{value}</{tag}>" for tag, value in data]

    def write(self, data: list[str]) -> None:
        print("  [XML] Serialising output...")
        self.output = "<root>\n" + "\n".join(data) + "\n</root>"
        print(self.output)


# ---------------------------------------------------------------------------
# Client demonstration
# ---------------------------------------------------------------------------

def main() -> None:
    print("=== CSV Processor ===")
    csv = CSVProcessor(["name, age, city", "alice, 30, new york", "bob, 25, berlin"])
    csv.process()

    print("\n=== JSON Processor ===")
    records = [
        {"id": 1, "name": "Alice", "email": "a@example.com", "password": "secret"},
        {"id": 2, "name": "Bob", "email": "b@example.com", "password": "hunter2"},
    ]
    json_proc = JSONProcessor(records, keep_keys=["id", "name", "email"])
    json_proc.process()

    print("\n=== XML Processor ===")
    xml_proc = XMLProcessor([("title", "Observer Pattern"), ("author", "GoF"), ("year", "1994")])
    xml_proc.process()


if __name__ == "__main__":
    main()
