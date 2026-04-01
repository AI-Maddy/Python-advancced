"""
Day 10 — Type Hints: Annotated, TypeGuard, and Advanced Typing
================================================================

Topics:
  - Optional[T] vs T | None (Python 3.10+)
  - Union[A, B] vs A | B
  - Literal["a", "b"], Final, ClassVar
  - Annotated[T, metadata] for rich annotations
  - TypeGuard[T] for type narrowing
  - TypeAlias (PEP 613)
  - typing.cast
  - mypy and pyright quick overview
"""
from __future__ import annotations

from typing import (
    Annotated, ClassVar, Final, Literal, Optional,
    TypeAlias, TypeGuard, Union, cast, get_type_hints,
)


# ---------------------------------------------------------------------------
# 1. Optional and Union
# ---------------------------------------------------------------------------

def find_user(user_id: int) -> dict[str, str] | None:  # Python 3.10+ syntax
    """Return user dict or None. Equivalent to Optional[dict[str, str]]."""
    if user_id == 1:
        return {"name": "Alice", "email": "alice@example.com"}
    return None


# Old style (still valid):
def find_user_old(user_id: int) -> Optional[dict[str, str]]:
    return find_user(user_id)


# Union types
def stringify(value: int | float | str) -> str:
    return str(value)


# ---------------------------------------------------------------------------
# 2. Literal — Exact value constraints
# ---------------------------------------------------------------------------

def set_log_level(level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]) -> None:
    print(f"Log level set to: {level}")


def http_method(method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"]) -> str:
    return f"HTTP {method}"


# ---------------------------------------------------------------------------
# 3. Final — Constants that cannot be reassigned
# ---------------------------------------------------------------------------

MAX_CONNECTIONS: Final[int] = 100
APP_NAME: Final[str] = "MyApp"

class Config:
    # ClassVar[T] — class-level annotation, not an instance field
    _instance_count: ClassVar[int] = 0
    # Final inside class — not reassignable after init
    VERSION: Final[str] = "1.0.0"

    def __init__(self, host: str) -> None:
        self.host = host
        Config._instance_count += 1


# ---------------------------------------------------------------------------
# 4. TypeAlias — Readable type aliases
# ---------------------------------------------------------------------------

# Old style:
Matrix = list[list[float]]

# New style (PEP 613, Python 3.10+):
JsonDict: TypeAlias = dict[str, object]
Callback: TypeAlias = "Callable[[str], None]"  # forward reference ok
Vector: TypeAlias = tuple[float, float, float]


# ---------------------------------------------------------------------------
# 5. Annotated[T, metadata] — Rich annotations
# ---------------------------------------------------------------------------
# Annotated lets you attach metadata to a type.
# The type checker uses the first argument (T); the rest is metadata.
# Libraries like Pydantic, FastAPI use the metadata for validation.

PositiveInt = Annotated[int, "must be > 0"]
Email = Annotated[str, "valid email address"]
Probability = Annotated[float, "between 0.0 and 1.0"]

def create_user(
    name: Annotated[str, "non-empty"],
    age: Annotated[int, "18-120"],
    email: Email,
) -> dict[str, object]:
    """Create user with annotated parameter metadata."""
    # Runtime: annotations are just hints; no automatic validation
    return {"name": name, "age": age, "email": email}


# ---------------------------------------------------------------------------
# 6. TypeGuard — Type Narrowing Functions
# ---------------------------------------------------------------------------
# TypeGuard[T] tells the type checker: if this function returns True,
# the argument can be treated as type T in the if branch.
# C++ equivalent: concept checks or if constexpr with type traits.

def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    """Return True iff val is a list where every element is a str."""
    return all(isinstance(x, str) for x in val)


def is_positive_int(val: object) -> TypeGuard[int]:
    """Return True iff val is a positive integer (not bool)."""
    return isinstance(val, int) and not isinstance(val, bool) and val > 0


def process_items(items: list[object]) -> None:
    if is_string_list(items):
        # mypy knows: items is list[str] here
        for s in items:
            print(s.upper())  # safe — s is str


# ---------------------------------------------------------------------------
# 7. typing.cast — Tell the type checker to trust you
# ---------------------------------------------------------------------------
# cast does nothing at runtime; it's a hint to the type checker.

def get_config_value(key: str) -> object:
    """Returns a value from config, type unknown."""
    store: dict[str, object] = {"port": 8080, "host": "localhost"}
    return store.get(key)


def demo_cast() -> None:
    raw = get_config_value("port")
    port = cast(int, raw)   # tell mypy: trust me, this is int
    print(port + 1)         # mypy allows this; runtime: just returns raw unchanged


if __name__ == "__main__":
    print("=== Optional ===")
    user = find_user(1)
    if user is not None:
        print(user["name"])
    print(find_user(99))

    print("\n=== Literal ===")
    set_log_level("INFO")
    print(http_method("GET"))

    print("\n=== TypeAlias ===")
    m: Matrix = [[1.0, 2.0], [3.0, 4.0]]
    print(m)

    print("\n=== Annotated ===")
    hints = get_type_hints(create_user, include_extras=True)
    print(hints)
    user2 = create_user("Alice", 30, "alice@example.com")
    print(user2)

    print("\n=== TypeGuard ===")
    process_items(["hello", "world"])
    print(is_positive_int(5))
    print(is_positive_int(-1))
    print(is_positive_int(True))  # False

    print("\n=== cast ===")
    demo_cast()
