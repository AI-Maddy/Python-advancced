"""
Day 15 — Error Handling and Custom Exceptions
===============================================

Topics:
  - Exception hierarchy in Python
  - try/except/else/finally
  - Custom exception classes with extra context
  - Exception chaining: raise NewError() from original
  - contextlib.suppress
  - ExceptionGroup (Python 3.11, except*)
  - logging module integration
  - Result types as alternative to exceptions
  - C++ comparison: std::expected vs Python exceptions
"""
from __future__ import annotations

import contextlib
import logging
from typing import Any

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# 1. Python Exception Hierarchy
# ---------------------------------------------------------------------------
# BaseException
#   SystemExit, KeyboardInterrupt, GeneratorExit
#   Exception
#     ArithmeticError: ZeroDivisionError, OverflowError
#     LookupError: IndexError, KeyError
#     TypeError, ValueError, AttributeError, NameError
#     OSError: FileNotFoundError, PermissionError, ...
#     RuntimeError, NotImplementedError, StopIteration

# RULE: Always catch specific exceptions, never bare 'except:'
# BAD:  except:              # catches EVERYTHING including SystemExit!
# BAD:  except Exception:    # too broad for most uses
# GOOD: except ValueError:   # specific

# ---------------------------------------------------------------------------
# 2. try / except / else / finally
# ---------------------------------------------------------------------------

def read_integer(s: str) -> int | None:
    """Demonstrate try/except/else/finally."""
    try:
        result = int(s)
    except ValueError:
        logger.warning("Cannot parse %r as integer", s)
        return None
    except TypeError:
        logger.error("Expected string, got %s", type(s).__name__)
        return None
    else:
        # Runs ONLY if no exception was raised in try
        logger.info("Parsed successfully: %d", result)
        return result
    finally:
        # ALWAYS runs — even if we return in try or except
        logger.debug("read_integer('%s') done", s)


# ---------------------------------------------------------------------------
# 3. Custom Exception Classes
# ---------------------------------------------------------------------------

from solutions import (
    AppError, ValidationError, NotFoundError,
    DatabaseError, ConnectionError, validate_form, safe_divide,
)


def demo_custom_exceptions() -> None:
    # Custom exceptions with extra attributes
    try:
        raise ValidationError("email", "must contain @", value="bad-email")
    except ValidationError as e:
        print(f"Code: {e.code}, Field: {e.field}, Value: {e.value!r}")
        print(f"Message: {e}")

    # Hierarchy: catch DatabaseError to catch ConnectionError too
    try:
        raise ConnectionError("db.example.com", 5432)
    except DatabaseError as e:
        print(f"Any DB error: {e}")


# ---------------------------------------------------------------------------
# 4. Exception Chaining
# ---------------------------------------------------------------------------

def demo_chaining() -> None:
    """raise X from Y sets __cause__; raise X inside except sets __context__."""

    # Implicit chaining (raise inside except — __context__ is set)
    try:
        try:
            int("bad")
        except ValueError:
            raise RuntimeError("conversion failed")
    except RuntimeError as e:
        print(f"RuntimeError.__context__: {e.__context__}")

    # Explicit chaining (raise X from Y — __cause__ is set)
    def process(data: str) -> int:
        try:
            return int(data)
        except ValueError as e:
            raise ValidationError("data", "must be integer") from e

    try:
        process("not-a-number")
    except ValidationError as e:
        print(f"ValidationError caused by: {e.__cause__!r}")

    # Suppress chaining: raise X from None
    def clean_raise(data: str) -> int:
        try:
            return int(data)
        except ValueError:
            raise ValidationError("data", "bad format") from None

    try:
        clean_raise("bad")
    except ValidationError as e:
        print(f"__cause__ is None: {e.__cause__ is None}")


# ---------------------------------------------------------------------------
# 5. ExceptionGroup (Python 3.11+)
# ---------------------------------------------------------------------------

def demo_exception_group() -> None:
    """Show ExceptionGroup and except*."""
    try:
        validate_form({"name": "", "age": -5, "email": "no-at-sign"})
    except ExceptionGroup as eg:
        print(f"Got {len(eg.exceptions)} validation errors:")
        for e in eg.exceptions:
            if isinstance(e, ValidationError):
                print(f"  field={e.field}: {e}")

    # except* syntax (Python 3.11+) — handle different exception types separately
    try:
        raise ExceptionGroup("mixed", [
            ValueError("bad value"),
            TypeError("bad type"),
        ])
    except* ValueError as eg:
        print(f"ValueError(s): {[str(e) for e in eg.exceptions]}")
    except* TypeError as eg:
        print(f"TypeError(s): {[str(e) for e in eg.exceptions]}")


# ---------------------------------------------------------------------------
# 6. contextlib.suppress
# ---------------------------------------------------------------------------

def demo_suppress() -> None:
    with contextlib.suppress(FileNotFoundError):
        open("/nonexistent/file.txt")
    print("After suppress — continued normally")

    # suppress multiple
    with contextlib.suppress(ValueError, TypeError):
        int("bad")


# ---------------------------------------------------------------------------
# 7. Logging Integration
# ---------------------------------------------------------------------------

def risky_operation(n: int) -> float:
    """Show logging with exception handling."""
    try:
        if n < 0:
            raise ValueError(f"n must be non-negative, got {n}")
        return 1.0 / n
    except ZeroDivisionError:
        logger.error("Division by zero for n=%d", n)
        raise
    except ValueError as e:
        logger.warning("Invalid input: %s", e)
        raise


if __name__ == "__main__":
    print("=== read_integer ===")
    print(read_integer("42"))
    print(read_integer("bad"))

    print("\n=== Custom Exceptions ===")
    demo_custom_exceptions()

    print("\n=== Exception Chaining ===")
    demo_chaining()

    print("\n=== ExceptionGroup ===")
    demo_exception_group()

    print("\n=== contextlib.suppress ===")
    demo_suppress()
