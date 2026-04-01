"""Day 15 — Exercises: Error Handling"""
from __future__ import annotations
from typing import Any

# Ex 1: Custom ValidationError hierarchy
class AppError(Exception):
    def __init__(self, message: str, code: int = 0) -> None: pass  # TODO

class ValidationError(AppError):
    def __init__(self, field: str, message: str, value: Any = None) -> None: pass  # TODO

class NotFoundError(AppError):
    def __init__(self, resource: str, resource_id: Any) -> None: pass  # TODO

# Ex 2: safe_divide raising ValidationError for zero
def safe_divide(a: float, b: float) -> float:
    pass  # TODO

# Ex 3: validate_form collecting all errors into ExceptionGroup
def validate_form(data: dict[str, Any]) -> None:
    pass  # TODO

# Ex 4: Exception chaining — raise AppError from low-level exception
def load_config(path: str) -> dict[str, Any]:
    pass  # TODO

if __name__ == "__main__":
    try:
        raise ValidationError("email", "bad format", "x")
    except ValidationError as e:
        print(e)
