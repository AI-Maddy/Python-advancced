"""
Example 2 — collections.abc custom Mapping.
"""
from __future__ import annotations

from collections.abc import Iterator, Mapping


class CaseInsensitiveDict(Mapping):
    """A mapping that stores keys in lower-case for case-insensitive lookup."""

    def __init__(self, data: dict | None = None) -> None:
        self._store: dict[str, object] = {}
        if data:
            for k, v in data.items():
                self[k] = v  # type: ignore[index]

    def __setitem__(self, key: str, value: object) -> None:
        self._store[key.lower()] = value

    def __getitem__(self, key: str) -> object:
        return self._store[key.lower()]

    def __iter__(self) -> Iterator:
        return iter(self._store)

    def __len__(self) -> int:
        return len(self._store)

    def __contains__(self, key: object) -> bool:
        if isinstance(key, str):
            return key.lower() in self._store
        return False


def main() -> None:
    d: Mapping = CaseInsensitiveDict({"Content-Type": "application/json", "Accept": "*/*"})

    print(f"isinstance Mapping: {isinstance(d, Mapping)}")

    print(d["content-type"])   # works
    print(d["CONTENT-TYPE"])   # works
    print(d["accept"])         # works

    print(f"'accept' in d: {'accept' in d}")
    print(f"'ACCEPT' in d: {'ACCEPT' in d}")

    # Mapping ABC provides keys(), values(), items(), get(), __eq__ etc. for free
    for k, v in d.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
