Day 15 — Error Handling and Custom Exceptions
===============================================

Python Exception Hierarchy
----------------------------
::

    BaseException
      SystemExit, KeyboardInterrupt, GeneratorExit
      Exception
        ArithmeticError: ZeroDivisionError, OverflowError
        LookupError: IndexError, KeyError
        TypeError, ValueError, AttributeError, OSError, ...

Custom Exceptions
------------------
.. code-block:: python

    class AppError(Exception):
        def __init__(self, message: str, code: int = 0) -> None:
            super().__init__(message)
            self.code = code

    class ValidationError(AppError):
        def __init__(self, field: str, message: str) -> None:
            super().__init__(f"{field}: {message}", code=1001)
            self.field = field

Exception Chaining
-------------------
.. code-block:: python

    # Explicit chaining — __cause__ set
    raise AppError("high level") from original_exception

    # Suppress chaining context
    raise AppError("clean") from None

ExceptionGroup (Python 3.11+)
--------------------------------
.. code-block:: python

    raise ExceptionGroup("validation", [e1, e2, e3])

    # Catch with except*:
    try:
        ...
    except* ValueError as eg:
        for e in eg.exceptions: ...
    except* TypeError as eg:
        ...

C++ std::expected vs Python exceptions
-----------------------------------------
Python traditionally uses exceptions for errors; ``Result[T, E]`` (Day 11)
provides a ``std::expected``-like alternative.  Use exceptions for truly
exceptional conditions; use Result types when failure is an expected outcome.
