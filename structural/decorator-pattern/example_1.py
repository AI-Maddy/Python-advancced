"""
Example 1 — Text formatter decorators.

UpperCase, Trim, and Wrap decorators are stacked to transform text.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class TextProcessor(ABC):
    @abstractmethod
    def process(self, text: str) -> str: ...


class PlainText(TextProcessor):
    def process(self, text: str) -> str:
        return text


class TextDecorator(TextProcessor, ABC):
    def __init__(self, wrapped: TextProcessor) -> None:
        self._wrapped = wrapped


class UpperCaseDecorator(TextDecorator):
    def process(self, text: str) -> str:
        return self._wrapped.process(text).upper()


class TrimDecorator(TextDecorator):
    def process(self, text: str) -> str:
        return self._wrapped.process(text).strip()


class WrapDecorator(TextDecorator):
    def __init__(self, wrapped: TextProcessor, prefix: str, suffix: str) -> None:
        super().__init__(wrapped)
        self._prefix = prefix
        self._suffix = suffix

    def process(self, text: str) -> str:
        return self._prefix + self._wrapped.process(text) + self._suffix


def main() -> None:
    raw_text = "  hello world  "

    plain = PlainText()
    print(repr(plain.process(raw_text)))

    trimmed = TrimDecorator(PlainText())
    print(repr(trimmed.process(raw_text)))

    upper_trimmed = UpperCaseDecorator(TrimDecorator(PlainText()))
    print(repr(upper_trimmed.process(raw_text)))

    wrapped = WrapDecorator(UpperCaseDecorator(TrimDecorator(PlainText())), "[", "]")
    print(repr(wrapped.process(raw_text)))


if __name__ == "__main__":
    main()
