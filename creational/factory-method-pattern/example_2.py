"""
Example 2 — Serializer factory.

Produces JSON, XML or CSV serializers through the factory-method interface.
"""
from __future__ import annotations

import csv
import io
import json
from abc import ABC, abstractmethod


class Serializer(ABC):
    """Product interface."""

    @abstractmethod
    def serialize(self, data: dict) -> str: ...

    @abstractmethod
    def content_type(self) -> str: ...


class JsonSerializer(Serializer):
    def serialize(self, data: dict) -> str:
        return json.dumps(data, indent=2)

    def content_type(self) -> str:
        return "application/json"


class XmlSerializer(Serializer):
    def serialize(self, data: dict) -> str:
        parts = ["<record>"]
        for k, v in data.items():
            parts.append(f"  <{k}>{v}</{k}>")
        parts.append("</record>")
        return "\n".join(parts)

    def content_type(self) -> str:
        return "application/xml"


class CsvSerializer(Serializer):
    def serialize(self, data: dict) -> str:
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=list(data.keys()))
        writer.writeheader()
        writer.writerow(data)
        return buf.getvalue()

    def content_type(self) -> str:
        return "text/csv"


class SerializerFactory(ABC):
    @abstractmethod
    def factory_method(self) -> Serializer: ...

    def export(self, data: dict) -> str:
        s = self.factory_method()
        print(f"Content-Type: {s.content_type()}")
        return s.serialize(data)


class JsonFactory(SerializerFactory):
    def factory_method(self) -> Serializer:
        return JsonSerializer()


class XmlFactory(SerializerFactory):
    def factory_method(self) -> Serializer:
        return XmlSerializer()


class CsvFactory(SerializerFactory):
    def factory_method(self) -> Serializer:
        return CsvSerializer()


def main() -> None:
    record = {"id": 1, "name": "Alice", "score": 99}
    for factory_cls in (JsonFactory, XmlFactory, CsvFactory):
        factory = factory_cls()
        output = factory.export(record)
        print(output)
        print()


if __name__ == "__main__":
    main()
