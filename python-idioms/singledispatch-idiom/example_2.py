"""
Example 2 — singledispatch for JSON-like serialisation with custom types.
"""
from __future__ import annotations

import datetime
import uuid
from dataclasses import dataclass
from functools import singledispatch


@singledispatch
def to_json_value(obj: object) -> object:
    """Fallback: raise for non-serializable types."""
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serialisable")


@to_json_value.register(str)
@to_json_value.register(int)
@to_json_value.register(float)
@to_json_value.register(bool)
@to_json_value.register(type(None))
def _json_primitive(obj: object) -> object:
    return obj


@to_json_value.register(list)
def _json_list(obj: list) -> list:
    return [to_json_value(item) for item in obj]


@to_json_value.register(dict)
def _json_dict(obj: dict) -> dict:
    return {str(k): to_json_value(v) for k, v in obj.items()}


@to_json_value.register(datetime.datetime)
def _json_datetime(obj: datetime.datetime) -> str:
    return obj.isoformat()


@to_json_value.register(uuid.UUID)
def _json_uuid(obj: uuid.UUID) -> str:
    return str(obj)


def main() -> None:
    import json

    payload = {
        "id": uuid.UUID("12345678-1234-5678-1234-567812345678"),
        "name": "Alice",
        "score": 99.5,
        "active": True,
        "created_at": datetime.datetime(2024, 1, 15, 12, 0, 0),
        "tags": ["python", "advanced"],
    }

    serialised = to_json_value(payload)
    print(json.dumps(serialised, indent=2))


if __name__ == "__main__":
    main()
