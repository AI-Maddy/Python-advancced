"""
Classmethod Factory Idiom — named constructors.

Equivalent to C++ named constructor idiom.

Demonstrates:
* @classmethod as alternative constructors (from_string, from_timestamp, today)
* __init_subclass__ for subclass configuration
* __class_getitem__ for generic syntax
"""
from __future__ import annotations

import datetime
import time
from typing import Any, ClassVar


# ---------------------------------------------------------------------------
# 1. Named constructors with @classmethod
# ---------------------------------------------------------------------------
class Date:
    """Immutable date value object with multiple construction paths.

    Prefer named constructors over raw ``Date(year, month, day)`` where
    the source of the data makes the intent clearer.
    """

    def __init__(self, year: int, month: int, day: int) -> None:
        if not 1 <= month <= 12:
            raise ValueError(f"month must be 1–12, got {month}")
        if not 1 <= day <= 31:
            raise ValueError(f"day must be 1–31, got {day}")
        self.year = year
        self.month = month
        self.day = day

    # --- Named constructors ---

    @classmethod
    def from_string(cls, s: str) -> Date:
        """Parse ``'YYYY-MM-DD'`` format.

        Args:
            s: Date string in ISO format.

        Returns:
            A new Date instance.
        """
        year, month, day = (int(part) for part in s.split("-"))
        return cls(year, month, day)

    @classmethod
    def from_timestamp(cls, ts: float) -> Date:
        """Construct from a UNIX timestamp.

        Args:
            ts: Seconds since the epoch.
        """
        dt = datetime.datetime.fromtimestamp(ts)
        return cls(dt.year, dt.month, dt.day)

    @classmethod
    def today(cls) -> Date:
        """Return today's date."""
        dt = datetime.date.today()
        return cls(dt.year, dt.month, dt.day)

    def to_string(self) -> str:
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Date):
            return NotImplemented
        return self.year == other.year and self.month == other.month and self.day == other.day

    def __repr__(self) -> str:
        return f"Date({self.year}, {self.month}, {self.day})"


# ---------------------------------------------------------------------------
# 2. More named constructors — Connection
# ---------------------------------------------------------------------------
class Connection:
    """Database connection with several construction flavours."""

    def __init__(self, host: str, port: int, database: str, *, ssl: bool = False) -> None:
        self.host = host
        self.port = port
        self.database = database
        self.ssl = ssl

    @classmethod
    def from_dsn(cls, dsn: str) -> Connection:
        """Parse a DSN like ``'postgresql://host:5432/mydb'``.

        Args:
            dsn: Data source name string.
        """
        # postgresql://host:port/database
        without_scheme = dsn.split("://", 1)[1]
        host_port, database = without_scheme.rsplit("/", 1)
        if ":" in host_port:
            host, port_str = host_port.rsplit(":", 1)
            port = int(port_str)
        else:
            host = host_port
            port = 5432
        return cls(host, port, database)

    @classmethod
    def local(cls, database: str) -> Connection:
        """Create a local loopback connection."""
        return cls("127.0.0.1", 5432, database)

    @classmethod
    def readonly(cls, host: str, database: str) -> Connection:
        """Create a read-only replica connection (port 5433)."""
        return cls(host, 5433, database)

    def __repr__(self) -> str:
        return f"Connection({self.host}:{self.port}/{self.database}, ssl={self.ssl})"


# ---------------------------------------------------------------------------
# 3. __init_subclass__ for subclass configuration
# ---------------------------------------------------------------------------
class Registry:
    """Base class; each subclass registers itself with a ``key``."""

    _registry: ClassVar[dict[str, type[Registry]]] = {}

    def __init_subclass__(cls, key: str = "", **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if key:
            Registry._registry[key] = cls

    @classmethod
    def get(cls, key: str) -> type[Registry]:
        return cls._registry[key]


class HandlerA(Registry, key="handler_a"):
    pass


class HandlerB(Registry, key="handler_b"):
    pass


# ---------------------------------------------------------------------------
# 4. __class_getitem__ for generic-like syntax
# ---------------------------------------------------------------------------
class TypedList:
    """A list that carries its element type via subscript syntax.

    Example::

        MyList = TypedList[int]
        instance = MyList([1, 2, 3])
    """

    _element_type: type = object

    def __init__(self, items: list) -> None:
        for item in items:
            if not isinstance(item, self._element_type):
                raise TypeError(
                    f"Expected {self._element_type.__name__}, got {type(item).__name__}"
                )
        self._items = list(items)

    def __class_getitem__(cls, item: type) -> type:
        """Return a subclass specialised for element type ``item``."""
        return type(
            f"TypedList[{item.__name__}]",
            (cls,),
            {"_element_type": item},
        )

    def __repr__(self) -> str:
        return f"TypedList[{self._element_type.__name__}]{self._items}"


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    d1 = Date.from_string("2024-03-15")
    d2 = Date.from_timestamp(time.time())
    d3 = Date.today()
    print(f"from_string : {d1}")
    print(f"from_timestamp: {d2}")
    print(f"today        : {d3}")

    conn1 = Connection.from_dsn("postgresql://db.example.com:5432/myapp")
    conn2 = Connection.local("testdb")
    conn3 = Connection.readonly("replica.example.com", "analytics")
    print(f"\n{conn1}")
    print(f"{conn2}")
    print(f"{conn3}")

    print(f"\nRegistry: {list(Registry._registry.keys())}")
    ha = Registry.get("handler_a")()
    print(f"handler_a: {ha}")

    IntList = TypedList[int]
    il = IntList([1, 2, 3])
    print(f"\n{il}")
    try:
        IntList([1, "oops"])
    except TypeError as e:
        print(f"TypedList error: {e}")
