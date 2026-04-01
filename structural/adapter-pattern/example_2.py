"""
Example 2 — Third-party JSON-to-dict adapter.

A third-party library returns its own DataRecord objects.  The adapter
converts them to plain Python dicts that the rest of the app uses.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class DataRecord:
    """Pretend third-party data type."""

    def __init__(self, fields: list[tuple[str, object]]) -> None:
        self._fields = fields

    def get_field_names(self) -> list[str]:
        return [name for name, _ in self._fields]

    def get_value(self, field_name: str) -> object:
        for name, value in self._fields:
            if name == field_name:
                return value
        raise KeyError(field_name)


class DataSource(ABC):
    """Modern target: all operations return plain dicts."""

    @abstractmethod
    def fetch_all(self) -> list[dict]: ...


class ThirdPartyDataClient:
    """Cannot be modified."""

    def query_all(self) -> list[DataRecord]:
        return [
            DataRecord([("id", 1), ("name", "Alice"), ("age", 30)]),
            DataRecord([("id", 2), ("name", "Bob"), ("age", 25)]),
        ]


class ThirdPartyDataAdapter(DataSource):
    """Adapts ThirdPartyDataClient to DataSource."""

    def __init__(self, client: ThirdPartyDataClient) -> None:
        self._client = client

    def fetch_all(self) -> list[dict]:
        records = self._client.query_all()
        return [
            {name: record.get_value(name) for name in record.get_field_names()}
            for record in records
        ]


def process(source: DataSource) -> None:
    for row in source.fetch_all():
        print(row)


def main() -> None:
    client = ThirdPartyDataClient()
    adapter = ThirdPartyDataAdapter(client)
    process(adapter)


if __name__ == "__main__":
    main()
