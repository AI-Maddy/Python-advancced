# :material-tag-multiple: Day 10 — Type Hints Advanced

!!! abstract "Day at a Glance"
    **Goal:** Go beyond basic annotations — master `Optional`, `Union`, `Literal`, `Final`, `ClassVar`, `Annotated`, `TypeGuard`, `TypeAlias`, `cast`, and `TYPE_CHECKING`.
    **C++ Equivalent:** Day 10 of Learn-Modern-CPP-OOP-30-Days (`const`, `constexpr`, `std::variant`, `std::optional`)
    **Estimated Time:** 60–90 minutes

<div class="grid cards" markdown>
- :material-lightbulb-on: **Core Concept** — advanced type hints let you encode invariants that survive refactoring and catch bugs before tests run
- :material-snake: **Python Way** — use `T | None` (Python 3.10+) instead of `Optional[T]`; use `Annotated` to attach validators
- :material-alert: **Watch Out** — `cast()` is a lie to the type-checker; it does nothing at runtime and can hide real bugs
- :material-check-circle: **By End of Day** — write production-quality annotated APIs with type narrowing, validated fields, and compile-time constants
</div>

## :material-lightbulb-on: Intuition

!!! info "Core Idea"
    Python's type system is *gradual* — you opt in incrementally.
    Advanced hints move the error surface from runtime to the analysis phase.
    `TypeGuard` teaches the checker how your custom `isinstance`-like predicates narrow types.
    `Annotated` threads arbitrary metadata through the type system so validators, serialisers, and ORMs can read it.

!!! success "Python vs C++"
    | Python | C++ |
    |--------|-----|
    | `Optional[T]` / `T \| None` | `std::optional<T>` |
    | `Union[A, B]` / `A \| B` | `std::variant<A, B>` |
    | `Literal["GET", "POST"]` | `enum class Method { GET, POST }` |
    | `Final[int]` | `const int` |
    | `ClassVar[int]` | `static int` member |
    | `Annotated[int, Gt(0)]` | Contracts / attributes (C++23) |
    | `TypeGuard[T]` | `if constexpr` / `std::holds_alternative` |
    | `cast(T, x)` | `static_cast<T>(x)` — but no runtime conversion! |

## :material-chart-flow: Type Narrowing Logic

```mermaid
flowchart TD
    A([Value of type X | Y]) --> B{isinstance check\nor TypeGuard?}
    B -- "isinstance(v, X)" --> C([Narrowed to X])
    B -- "isinstance(v, Y)" --> D([Narrowed to Y])
    B -- custom TypeGuard --> E([Narrowed to guarded type])
    C --> F{Exhausted all branches?}
    D --> F
    E --> F
    F -- Yes --> G([assert_never — dead code detected])
    F -- No --> H([Remaining union type])
    H --> I{None check?}
    I -- "if v is None" --> J([Narrowed to None])
    I -- "if v is not None" --> K([Narrowed: None removed])
```

## :material-book-open-variant: Lesson

### `Optional[T]` vs `T | None`

Both express "this value might be absent". Prefer the modern `|` syntax (Python 3.10+).

```python
from typing import Optional

# Old style (still valid)
def greet(name: Optional[str] = None) -> str:
    if name is None:
        return "Hello, stranger!"
    return f"Hello, {name}!"

# Modern style (Python 3.10+)
def greet_modern(name: str | None = None) -> str:
    return f"Hello, {name or 'stranger'}!"
```

### `Union[A, B]` vs `A | B`

```python
from typing import Union

# Old
def parse(value: Union[int, str, float]) -> str:
    return str(value)

# Modern (3.10+)
def parse_modern(value: int | str | float) -> str:
    return str(value)
```

### `Literal` — Exact Value Types

```python
from typing import Literal

HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
StatusCode = Literal[200, 201, 204, 400, 401, 403, 404, 500]


def make_request(url: str, method: HttpMethod = "GET") -> None:
    ...

make_request("/api/users", "GET")    # OK
# make_request("/api", "TRACE")      # mypy error: "TRACE" not in Literal
```

### `Final` — Compile-time Constants

```python
from typing import Final

MAX_RETRIES: Final = 3
BASE_URL: Final[str] = "https://api.example.com"

# MAX_RETRIES = 5   # mypy error: Cannot assign to final name "MAX_RETRIES"

# In a class:
class Config:
    DEBUG: Final = False
    VERSION: Final[str] = "1.0.0"
```

### `ClassVar` — Class-level vs Instance-level

```python
from typing import ClassVar


class Counter:
    _count: ClassVar[int] = 0   # belongs to the class

    def __init__(self, name: str) -> None:
        self.name = name        # belongs to each instance
        Counter._count += 1

    @classmethod
    def total(cls) -> int:
        return cls._count


a = Counter("a")
b = Counter("b")
print(Counter.total())   # 2
```

### `Annotated[T, metadata]` — Typed Validators

```python
from typing import Annotated, get_type_hints, get_args, get_origin
import dataclasses


class Gt:
    """Metadata: value must be greater than `value`."""
    def __init__(self, value): self.value = value

class MaxLen:
    """Metadata: string length must not exceed `n`."""
    def __init__(self, n): self.n = n


def validate(cls, instance) -> None:
    """Simple validator that reads Annotated metadata."""
    hints = get_type_hints(cls, include_extras=True)
    for field, hint in hints.items():
        if get_origin(hint) is Annotated:
            base, *meta = get_args(hint)
            value = getattr(instance, field)
            for m in meta:
                if isinstance(m, Gt) and not (value > m.value):
                    raise ValueError(f"{field} must be > {m.value}, got {value}")
                if isinstance(m, MaxLen) and len(value) > m.n:
                    raise ValueError(f"{field} length must be <= {m.n}")


@dataclasses.dataclass
class Product:
    name: Annotated[str, MaxLen(50)]
    price: Annotated[float, Gt(0)]
    stock: Annotated[int, Gt(-1)]


p = Product("Widget", 9.99, 100)
validate(Product, p)   # OK

try:
    bad = Product("Item", -1.0, 5)
    validate(Product, bad)
except ValueError as e:
    print(e)   # price must be > 0, got -1.0
```

### `TypeGuard[T]` — Type Narrowing

```python
from typing import TypeGuard


def is_list_of_str(val: list) -> TypeGuard[list[str]]:
    """Returns True only if every element is a str."""
    return all(isinstance(x, str) for x in val)


def process(items: list[int | str]) -> None:
    # Without TypeGuard the checker doesn't know the type inside the branch
    if is_list_of_str(items):
        # Here mypy/pyright knows: items is list[str]
        print(", ".join(items))
    else:
        print(sum(x for x in items if isinstance(x, int)))


process(["a", "b", "c"])   # a, b, c
process([1, 2, 3])          # 6
```

### `TypeAlias` — Named Aliases

```python
from typing import TypeAlias

# Python 3.10+: use TypeAlias for explicit aliases
Vector: TypeAlias = list[float]
Matrix: TypeAlias = list[Vector]
JsonValue: TypeAlias = str | int | float | bool | None | dict | list

def dot(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b))

# Python 3.12+ can also use: type Vector = list[float]
```

### `typing.cast` — Escape Hatch

```python
from typing import cast

data: dict = {"name": "Alice", "age": 30}

# We know this is str — tell the checker, but NO runtime conversion
name = cast(str, data["name"])
print(name.upper())   # ALICE

# cast does NOTHING at runtime:
x = cast(int, "hello")   # no error at runtime — but TypeErrors follow!
```

### `TYPE_CHECKING` — Break Import Cycles

```python
from __future__ import annotations   # makes all hints strings (lazy)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from heavy_module import HeavyClass   # only imported during type analysis

class MyService:
    def process(self, obj: "HeavyClass") -> None:   # string annotation if needed
        ...
```

### Exhaustiveness with `assert_never`

```python
from typing import Literal, NoReturn, assert_never

Status = Literal["ok", "error", "pending"]


def handle(s: Status) -> str:
    if s == "ok":
        return "All good"
    elif s == "error":
        return "Something went wrong"
    elif s == "pending":
        return "Waiting..."
    else:
        assert_never(s)   # mypy error if a new Literal value is not handled
```

## :material-alert: Common Pitfalls

!!! warning "`Optional[T]` does NOT mean 'optional parameter'"
    `Optional[str]` means `str | None`.
    It says nothing about whether the parameter has a default value.
    An `Optional[str]` parameter with no default is *required* and can accept `None`.

    ```python
    def f(x: Optional[str]) -> None: ...   # x is required, but may be None
    def g(x: str = "") -> None: ...         # x is optional (has default)
    def h(x: Optional[str] = None) -> None: ...  # both: optional AND nullable
    ```

!!! danger "`cast()` bypasses all type safety"
    ```python
    # This passes mypy but crashes at runtime:
    x = cast(int, "not_a_number")
    print(x + 1)   # TypeError: can only concatenate str (not "int") to str
    ```
    Use `cast` only when you have *proven* the type is correct and the checker cannot infer it.

!!! warning "Forgetting `from __future__ import annotations`"
    Forward references in annotations require quoting (`"MyClass"`) unless you use `from __future__ import annotations` which lazily evaluates all annotations. Without it, `def f(x: MyClass)` before `MyClass` is defined raises `NameError`.

## :material-help-circle: Flashcards

???+ question "Q1 — What is the difference between `Literal` and `Final`?"
    `Literal["GET", "POST"]` constrains the *set of values* a variable may hold — it's a type.
    `Final` constrains *reassignment* — a `Final` variable may still hold any value of its declared type, but cannot be rebound after initialisation.
    They are orthogonal: `x: Final[Literal["GET"]] = "GET"` is both.

???+ question "Q2 — When should you use `Annotated` instead of a plain type?"
    When you need to attach domain-specific metadata (validators, units, database column info, serialisation rules) *inside* the type hint, so that frameworks can read it with `get_type_hints(include_extras=True)` without requiring a separate attribute or decorator.

???+ question "Q3 — What does `TypeGuard[T]` tell the type-checker?"
    If a function `def is_foo(x: Any) -> TypeGuard[Foo]` returns `True`, the checker narrows the type of `x` to `Foo` inside the `if` branch. It is the typed equivalent of an `isinstance` check for custom predicate functions.

???+ question "Q4 — Why use `TYPE_CHECKING`?"
    To avoid circular imports or expensive imports that are only needed for type annotations.
    Code inside `if TYPE_CHECKING:` runs only when a static type-checker processes the file; at runtime the block is skipped entirely.

## :material-clipboard-check: Self Test

=== "Question 1"
    Write a `safe_divide` function that returns `float | None` and narrows cleanly. Then write a `TypeGuard` predicate `is_positive_int` that checks if a value is an `int` greater than zero.

=== "Answer 1"
    ```python
    from typing import TypeGuard, Any


    def safe_divide(a: float, b: float) -> float | None:
        if b == 0:
            return None
        return a / b


    result = safe_divide(10, 2)
    if result is not None:
        print(f"{result:.1f}")   # 5.0


    def is_positive_int(val: Any) -> TypeGuard[int]:
        return isinstance(val, int) and val > 0


    data: list[int | str] = [1, -2, "hello", 42]
    positives = [x for x in data if is_positive_int(x)]
    print(positives)   # [1, 42]
    ```

=== "Question 2"
    What is the difference between these two? Which is preferred in Python 3.10+?
    ```python
    from typing import Optional, Union
    def f(x: Optional[str]) -> Union[int, str]: ...
    def g(x: str | None) -> int | str: ...
    ```

=== "Answer 2"
    They are **semantically identical** — `Optional[str]` is sugar for `Union[str, None]`, and `str | None` is the 3.10+ shorthand for the same thing.
    In Python 3.10+, the `|` syntax (`g`'s style) is preferred because it is more concise and readable, matches how sets are written, and is valid in `isinstance()` checks at runtime:
    ```python
    isinstance("hi", str | None)   # True (Python 3.10+)
    ```

## :material-check-circle: Summary

!!! success "Key Takeaways"
    - Use `T | None` (3.10+) instead of `Optional[T]` for clarity
    - `Literal` encodes exact values as types — great for string-enum parameters
    - `Final` prevents reassignment — the Python equivalent of `const`
    - `ClassVar` distinguishes class-level from instance-level attributes for the checker
    - `Annotated[T, meta]` attaches domain metadata that frameworks can introspect
    - `TypeGuard[T]` makes custom narrowing predicates type-safe
    - `TypeAlias` (or `type X = ...` in 3.12+) gives meaningful names to complex types
    - `cast()` is a static-analysis-only escape hatch — no runtime conversion happens
    - `TYPE_CHECKING` eliminates import cycles and expensive runtime imports for type-only dependencies
