"""Strategy Pattern — Example 2: Compression Strategies.

A file archiver supports different compression algorithms.  Each algorithm
is encapsulated as a strategy so the archiver context never needs to change.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class CompressionStrategy(ABC):
    """Abstract compression strategy."""

    @abstractmethod
    def compress(self, data: bytes) -> bytes:
        """Compress *data* and return compressed bytes."""

    @abstractmethod
    def decompress(self, data: bytes) -> bytes:
        """Decompress *data* and return original bytes."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable algorithm name."""


class NoCompressionStrategy(CompressionStrategy):
    """Pass-through — no compression applied."""

    def compress(self, data: bytes) -> bytes:
        return data

    def decompress(self, data: bytes) -> bytes:
        return data

    @property
    def name(self) -> str:
        return "none"


class RLECompressionStrategy(CompressionStrategy):
    """Simple Run-Length Encoding (demonstration only)."""

    def compress(self, data: bytes) -> bytes:
        if not data:
            return b""
        result = bytearray()
        count = 1
        for i in range(1, len(data)):
            if data[i] == data[i - 1] and count < 255:
                count += 1
            else:
                result += bytes([count, data[i - 1]])
                count = 1
        result += bytes([count, data[-1]])
        return bytes(result)

    def decompress(self, data: bytes) -> bytes:
        result = bytearray()
        for i in range(0, len(data), 2):
            result += bytes([data[i + 1]] * data[i])
        return bytes(result)

    @property
    def name(self) -> str:
        return "RLE"


class ZlibCompressionStrategy(CompressionStrategy):
    """Uses Python's built-in zlib module."""

    def compress(self, data: bytes) -> bytes:
        import zlib
        return zlib.compress(data)

    def decompress(self, data: bytes) -> bytes:
        import zlib
        return zlib.decompress(data)

    @property
    def name(self) -> str:
        return "zlib"


@dataclass
class Archiver:
    """Context that compresses/decompresses using a pluggable strategy."""
    strategy: CompressionStrategy

    def archive(self, data: bytes) -> bytes:
        compressed = self.strategy.compress(data)
        ratio = len(compressed) / max(len(data), 1) * 100
        print(
            f"[{self.strategy.name}] {len(data)} → {len(compressed)} bytes "
            f"({ratio:.1f}%)"
        )
        return compressed

    def extract(self, data: bytes) -> bytes:
        return self.strategy.decompress(data)


def main() -> None:
    sample = b"AAABBBCCCCDDDDDEEEEE" * 10

    for strat in (NoCompressionStrategy(), RLECompressionStrategy(), ZlibCompressionStrategy()):
        arch = Archiver(strategy=strat)
        compressed = arch.archive(sample)
        recovered = arch.extract(compressed)
        assert recovered == sample, f"Round-trip failed for {strat.name}"
    print("All round-trips verified.")


if __name__ == "__main__":
    main()
