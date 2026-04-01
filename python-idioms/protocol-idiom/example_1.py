"""
Example 1 — Protocol-based plug-in system.

Any class with a process(data) → str method works as a processor.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class DataProcessor(Protocol):
    def process(self, data: str) -> str: ...
    def name(self) -> str: ...


class UpperCaseProcessor:
    def process(self, data: str) -> str:
        return data.upper()

    def name(self) -> str:
        return "UpperCase"


class ReverseProcessor:
    def process(self, data: str) -> str:
        return data[::-1]

    def name(self) -> str:
        return "Reverse"


class Pipeline:
    def __init__(self, processors: list[DataProcessor]) -> None:
        self._processors = processors

    def run(self, data: str) -> str:
        for p in self._processors:
            data = p.process(data)
        return data


def main() -> None:
    processors: list[DataProcessor] = [UpperCaseProcessor(), ReverseProcessor()]

    for p in processors:
        print(f"{p.name()}: isinstance check = {isinstance(p, DataProcessor)}")

    pipeline = Pipeline(processors)
    result = pipeline.run("hello world")
    print(f"Pipeline result: {result!r}")


if __name__ == "__main__":
    main()
