"""Day 15 — Exercises: Error Handling"""
from __future__ import annotations
from typing import Any

# Ex 1: Custom ValidationError hierarchy
class AppError(Exception):
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
    def __init__(self, field: str, message: str, value: Any = None) -> None:
        super().__init__(f"Validation error on '{field}': {message}", code=1001)
        self.field = field
        self.value = value

class NotFoundError(AppError):
    def __init__(self, resource: str, resource_id: Any) -> None:
        super().__init__(
            f"{resource} with id={resource_id!r} not found",
            code=1002,
            context={"resource": resource, "id": resource_id},
        )
        self.resource = resource
        self.resource_id = resource_id

# Ex 2: safe_divide raising ValidationError for zero
def safe_divide(a: float, b: float) -> float:
    try:
        result = a / b
    except ZeroDivisionError:
        raise ValidationError("b", "cannot be zero", value=b)
    else:
        return result
    finally:
        pass

# Ex 3: validate_form collecting all errors into ExceptionGroup
def validate_form(data: dict[str, Any]) -> None:
    errors: list[Exception] = []

    if not data.get("name"):
        errors.append(ValidationError("name", "required"))
    if not isinstance(data.get("age"), int) or data.get("age", -1) < 0:
        errors.append(ValidationError("age", "must be non-negative integer"))
    if "@" not in str(data.get("email", "")):
        errors.append(ValidationError("email", "must contain @"))

    if errors:
        raise ExceptionGroup("form validation failed", errors)

# Ex 4: Exception chaining — raise AppError from low-level exception
def load_config(path: str) -> dict[str, Any]:
    try:
        with open(path) as f:
            import json
            return json.load(f)
    except FileNotFoundError as e:
        raise NotFoundError("config file", path) from e
    except Exception as e:
        raise AppError(f"Failed to load config: {path}") from e

if __name__ == "__main__":
    try:
        raise ValidationError("email", "bad format", "x")
    except ValidationError as e:
        print(e)
