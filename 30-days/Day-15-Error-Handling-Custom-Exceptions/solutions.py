"""Day 15 — Solutions: Error Handling and Custom Exceptions"""
from __future__ import annotations

from typing import Any


# ---------------------------------------------------------------------------
# Custom Exception Hierarchy
# ---------------------------------------------------------------------------

class AppError(Exception):
    """Base application exception."""

    def __init__(self, message: str, code: int = 0, context: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.context = context or {}

    def __str__(self) -> str:
        base = super().__str__()
        if self.code:
            return f"[E{self.code:04d}] {base}"
        return base


class ValidationError(AppError):
    """Raised when input validation fails."""

    def __init__(self, field: str, message: str, value: Any = None) -> None:
        super().__init__(f"Validation error on '{field}': {message}", code=1001)
        self.field = field
        self.value = value


class NotFoundError(AppError):
    """Raised when a resource is not found."""

    def __init__(self, resource: str, resource_id: Any) -> None:
        super().__init__(
            f"{resource} with id={resource_id!r} not found",
            code=1002,
            context={"resource": resource, "id": resource_id},
        )
        self.resource = resource
        self.resource_id = resource_id


class DatabaseError(AppError):
    """Database operation failure."""

    def __init__(self, operation: str, message: str) -> None:
        super().__init__(f"Database error during {operation}: {message}", code=2001)
        self.operation = operation


class ConnectionError(DatabaseError):
    """Cannot connect to database."""

    def __init__(self, host: str, port: int) -> None:
        super().__init__("connect", f"Cannot reach {host}:{port}")
        self.host = host
        self.port = port


# ---------------------------------------------------------------------------
# Exception chaining
# ---------------------------------------------------------------------------

def load_config(path: str) -> dict[str, Any]:
    """Load config — raises AppError chained from FileNotFoundError."""
    try:
        with open(path) as f:
            import json
            return json.load(f)
    except FileNotFoundError as e:
        raise NotFoundError("config file", path) from e
    except Exception as e:
        raise AppError(f"Failed to load config: {path}") from e


# ---------------------------------------------------------------------------
# try/except/else/finally
# ---------------------------------------------------------------------------

def safe_divide(a: float, b: float) -> float:
    """Demonstrates try/except/else/finally."""
    try:
        result = a / b
    except ZeroDivisionError:
        raise ValidationError("b", "cannot be zero", value=b)
    else:
        # Runs only if no exception
        return result
    finally:
        # Always runs — cleanup goes here
        pass


# ---------------------------------------------------------------------------
# ExceptionGroup (Python 3.11+)
# ---------------------------------------------------------------------------

def validate_form(data: dict[str, Any]) -> None:
    """Collect ALL validation errors and raise as ExceptionGroup."""
    errors: list[Exception] = []

    if not data.get("name"):
        errors.append(ValidationError("name", "required"))
    if not isinstance(data.get("age"), int) or data.get("age", -1) < 0:
        errors.append(ValidationError("age", "must be non-negative integer"))
    if "@" not in str(data.get("email", "")):
        errors.append(ValidationError("email", "must contain @"))

    if errors:
        raise ExceptionGroup("form validation failed", errors)


if __name__ == "__main__":
    # Custom exceptions
    try:
        raise ValidationError("email", "invalid format", value="not-an-email")
    except ValidationError as e:
        print(f"Caught: {e}, field={e.field}, value={e.value!r}")

    try:
        raise ConnectionError("localhost", 5432)
    except DatabaseError as e:
        print(f"DB error: {e}")
    except AppError as e:
        print(f"App error: {e}")

    # safe_divide
    print(safe_divide(10.0, 3.0))
    try:
        safe_divide(1.0, 0.0)
    except ValidationError as e:
        print(f"Validation: {e}")

    # ExceptionGroup
    try:
        validate_form({"name": "", "age": -1, "email": "bad"})
    except ExceptionGroup as eg:
        print(f"ExceptionGroup: {eg.message}, {len(eg.exceptions)} errors")
        for exc in eg.exceptions:
            print(f"  - {exc}")
