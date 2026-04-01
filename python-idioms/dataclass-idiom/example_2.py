"""
Example 2 — dataclasses.asdict / replace for configuration snapshots.
"""
from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field


@dataclass
class ServerConfig:
    host: str = "localhost"
    port: int = 8080
    workers: int = 4
    debug: bool = False
    allowed_origins: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not 1 <= self.port <= 65535:
            raise ValueError(f"Invalid port: {self.port}")


def main() -> None:
    dev = ServerConfig(debug=True, allowed_origins=["http://localhost:3000"])
    print("Dev config:", dev)

    # asdict — deep converts to plain dict
    d = dataclasses.asdict(dev)
    print("As dict:", d)

    # replace — create variant without mutating original
    prod = dataclasses.replace(
        dev, host="0.0.0.0", port=443, workers=16, debug=False,
        allowed_origins=["https://example.com"]
    )
    print("Prod config:", prod)
    print("Dev unchanged:", dev.debug)   # True

    # Validation
    try:
        ServerConfig(port=99999)
    except ValueError as e:
        print(f"Validation: {e}")

    # NamedTuple comparison
    from dataclass_idiom import Coordinate
    london = Coordinate(51.5074, -0.1278)
    paris = Coordinate(48.8566, 2.3522)
    print(f"\nLondon: {london.label()}")
    print(f"Paris:  {paris.label()}")
    # NamedTuple supports indexing
    print(f"London lat (index): {london[0]}")


if __name__ == "__main__":
    main()
