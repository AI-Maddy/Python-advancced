"""
Day 05 — Context Managers and RAII
=====================================

Topics:
  - Python's RAII equivalent: with statement
  - __enter__ / __exit__ protocol
  - contextlib.contextmanager decorator form
  - contextlib.suppress, contextlib.nullcontext, contextlib.ExitStack
  - Exception handling in __exit__ (returning True suppresses)
  - Nested with and with A() as a, B() as b: syntax
  - Real examples: file I/O, database transaction, timer, lock
"""
from __future__ import annotations

import contextlib
import time
import threading
from contextlib import contextmanager, suppress, nullcontext, ExitStack
from typing import Generator


# ---------------------------------------------------------------------------
# 1. Why Context Managers?
# ---------------------------------------------------------------------------
# C++ RAII: destructor releases the resource when the object goes out of scope.
#
# Python doesn't have deterministic destructors (GC is non-deterministic),
# so it provides the 'with' statement as the RAII equivalent.
#
#   C++ RAII:                      Python context manager:
#   {                              with resource_manager() as r:
#     ScopedResource r{...};           use(r)
#     use(r);                      # __exit__ called here — always
#   }  // ~ScopedResource() here
#
# The 'with' guarantee: __exit__ is ALWAYS called, even if an exception occurs.


# ---------------------------------------------------------------------------
# 2. Class-based Context Manager: __enter__ / __exit__
# ---------------------------------------------------------------------------

class Timer:
    """Measures elapsed time. Class-based context manager.

    Usage:
        with Timer("my operation") as t:
            do_work()
        # elapsed is printed on exit
    """

    def __init__(self, label: str = "operation") -> None:
        self.label = label
        self.elapsed: float = 0.0
        self._start: float = 0.0

    def __enter__(self) -> "Timer":
        """Called at the 'with' statement. Returns the context value."""
        self._start = time.perf_counter()
        return self   # available as 'as t' in 'with Timer() as t:'

    def __exit__(
        self,
        exc_type: type | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> bool | None:
        """Called when the 'with' block exits.

        Args:
            exc_type, exc_val, exc_tb: exception info (all None if no exception)

        Returns:
            True to suppress the exception, False/None to propagate it.
        """
        self.elapsed = time.perf_counter() - self._start
        print(f"[Timer] {self.label}: {self.elapsed * 1000:.2f} ms")
        # Returning None (falsy) = propagate any exception
        return None


class DatabaseTransaction:
    """Simulated database transaction context manager."""

    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self._committed = False
        self._rolled_back = False

    def __enter__(self) -> "DatabaseTransaction":
        print(f"[DB] BEGIN TRANSACTION on {self.db_name}")
        return self

    def __exit__(
        self,
        exc_type: type | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> bool | None:
        if exc_type is None:
            # No exception: commit
            print(f"[DB] COMMIT on {self.db_name}")
            self._committed = True
        else:
            # Exception: rollback
            print(f"[DB] ROLLBACK on {self.db_name} due to {exc_type.__name__}")
            self._rolled_back = True
        # Return None: propagate the exception (don't suppress it)
        return None

    def execute(self, sql: str) -> None:
        print(f"[DB] execute: {sql}")


# ---------------------------------------------------------------------------
# 3. @contextmanager — Generator-based Context Managers
# ---------------------------------------------------------------------------
# The simpler way to write context managers.
# Code before 'yield' = __enter__
# The yield value = the 'as' variable
# Code after 'yield' = __exit__

@contextmanager
def managed_file(path: str, mode: str = "r") -> Generator[object, None, None]:
    """File context manager using @contextmanager."""
    print(f"[File] Opening {path}")
    f = None
    try:
        f = open(path, mode)
        yield f               # caller uses the file here
    finally:
        if f is not None:
            f.close()
            print(f"[File] Closed {path}")


@contextmanager
def timer_cm(label: str = "operation") -> Generator[dict[str, float], None, None]:
    """Timer as a generator-based context manager."""
    result: dict[str, float] = {}
    start = time.perf_counter()
    try:
        yield result          # caller can set result["custom"] inside the block
    finally:
        result["elapsed"] = time.perf_counter() - start
        print(f"[Timer] {label}: {result['elapsed'] * 1000:.2f} ms")


@contextmanager
def suppress_and_log(*exceptions: type[BaseException]) -> Generator[None, None, None]:
    """Suppress specific exceptions and log them."""
    try:
        yield
    except exceptions as e:
        print(f"[Suppressed] {type(e).__name__}: {e}")


# ---------------------------------------------------------------------------
# 4. Exception Handling in __exit__
# ---------------------------------------------------------------------------

class SuppressSpecific:
    """Context manager that suppresses specific exception types.

    This shows the 'return True' suppression mechanism.
    """

    def __init__(self, *exc_types: type[BaseException]) -> None:
        self.exc_types = exc_types
        self.suppressed: BaseException | None = None

    def __enter__(self) -> "SuppressSpecific":
        return self

    def __exit__(
        self,
        exc_type: type | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> bool:
        if exc_type is not None and issubclass(exc_type, self.exc_types):
            self.suppressed = exc_val
            return True    # suppress the exception — don't propagate
        return False       # propagate the exception


# ---------------------------------------------------------------------------
# 5. Nested Context Managers
# ---------------------------------------------------------------------------

def demo_nested() -> None:
    """Show nested and multi-context syntax."""

    # Old style: nested with blocks
    # with A() as a:
    #     with B() as b:
    #         use(a, b)

    # Modern style: multiple contexts on one line (Python 2.7+)
    # with A() as a, B() as b:
    #     use(a, b)

    # ExitStack: dynamic number of context managers
    with ExitStack() as stack:
        timers = [stack.enter_context(Timer(f"task{i}")) for i in range(3)]
        for i, t in enumerate(timers):
            time.sleep(0.001 * i)
    # All timers' __exit__ called in reverse order


# ---------------------------------------------------------------------------
# 6. contextlib Utilities
# ---------------------------------------------------------------------------

def demo_contextlib() -> None:
    """Show contextlib.suppress and contextlib.nullcontext."""

    # suppress: ignore specific exceptions
    with suppress(FileNotFoundError):
        open("/nonexistent/path/to/file.txt")   # silently ignored
    print("After suppress — no exception propagated")

    # nullcontext: no-op context manager (useful in conditional code)
    debug = True
    lock: threading.Lock | None = threading.Lock() if debug else None

    with (lock if lock else nullcontext()):
        print("Inside conditional lock")

    # suppress as a function — clean exception ignoring
    with suppress(ValueError, TypeError):
        int("not a number")  # ignored


# ---------------------------------------------------------------------------
# 7. Real-world: Lock Context Manager
# ---------------------------------------------------------------------------

class LockedCounter:
    """Thread-safe counter using Lock as context manager."""

    def __init__(self) -> None:
        self._count = 0
        self._lock = threading.Lock()

    def increment(self) -> None:
        with self._lock:     # acquires on enter, releases on exit
            self._count += 1

    @property
    def count(self) -> int:
        with self._lock:
            return self._count


if __name__ == "__main__":
    print("=== Class-based Timer ===")
    with Timer("sort 10000 items") as t:
        data = sorted(range(10000, 0, -1))
    print(f"elapsed captured: {t.elapsed:.6f}s")

    print("\n=== Database Transaction — success ===")
    with DatabaseTransaction("users_db") as tx:
        tx.execute("INSERT INTO users VALUES (1, 'Alice')")

    print("\n=== Database Transaction — rollback ===")
    try:
        with DatabaseTransaction("users_db") as tx:
            tx.execute("INSERT INTO users VALUES (2, 'Bob')")
            raise RuntimeError("Simulated error")
    except RuntimeError:
        pass

    print("\n=== Generator Context Manager ===")
    with timer_cm("test") as result:
        time.sleep(0.01)
    print(f"result dict: {result}")

    print("\n=== Suppress Specific ===")
    with SuppressSpecific(ValueError, ZeroDivisionError) as ctx:
        int("not a number")
    print(f"suppressed: {ctx.suppressed}")

    print("\n=== contextlib utilities ===")
    demo_contextlib()

    print("\n=== LockedCounter ===")
    counter = LockedCounter()
    threads = [threading.Thread(target=counter.increment) for _ in range(100)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    print(f"count = {counter.count}")   # should be 100
