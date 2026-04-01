"""
Context Manager Idiom — Python's RAII equivalent.

Covers:
* Class-based context managers (__enter__ / __exit__)
* @contextmanager generator form
* contextlib.suppress and contextlib.closing
"""
from __future__ import annotations

import contextlib
import io
import time
from contextlib import contextmanager
from typing import Generator


# ---------------------------------------------------------------------------
# 1. Class-based: FileManager
# ---------------------------------------------------------------------------
class FileManager:
    """Context manager that opens a file and guarantees it is closed.

    Args:
        path: File path to open.
        mode: Open mode (default ``'r'``).

    Example::

        with FileManager("data.txt") as f:
            content = f.read()
    """

    def __init__(self, path: str, mode: str = "r") -> None:
        self.path = path
        self.mode = mode
        self._file: io.TextIOWrapper | None = None

    def __enter__(self) -> io.TextIOWrapper:
        self._file = open(self.path, self.mode)
        return self._file

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> bool:
        if self._file:
            self._file.close()
        return False  # do not suppress exceptions


# ---------------------------------------------------------------------------
# 2. Class-based: DatabaseConnection
# ---------------------------------------------------------------------------
class DatabaseConnection:
    """Simulated DB connection that commits on success, rolls back on error.

    Args:
        dsn: Connection string.
    """

    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self.connected = False
        self.committed = False
        self.rolled_back = False
        self._queries: list[str] = []

    def connect(self) -> None:
        self.connected = True

    def execute(self, query: str) -> None:
        self._queries.append(query)

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True

    def close(self) -> None:
        self.connected = False

    def __enter__(self) -> DatabaseConnection:
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> bool:
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        self.close()
        return False


# ---------------------------------------------------------------------------
# 3. Class-based: Timer
# ---------------------------------------------------------------------------
class Timer:
    """Measures wall-clock time of a code block.

    Example::

        with Timer() as t:
            do_work()
        print(f"Elapsed: {t.elapsed:.3f}s")
    """

    def __init__(self) -> None:
        self.elapsed: float = 0.0
        self._start: float = 0.0

    def __enter__(self) -> Timer:
        self._start = time.perf_counter()
        return self

    def __exit__(self, *_: object) -> bool:
        self.elapsed = time.perf_counter() - self._start
        return False


# ---------------------------------------------------------------------------
# 4. @contextmanager form
# ---------------------------------------------------------------------------
@contextmanager
def managed_connection(dsn: str) -> Generator[DatabaseConnection, None, None]:
    """Generator-based context manager for a database connection.

    Yields a ``DatabaseConnection`` and ensures cleanup on exit.
    """
    conn = DatabaseConnection(dsn)
    conn.connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@contextmanager
def temporary_attribute(obj: object, attr: str, value: object) -> Generator[None, None, None]:
    """Temporarily set an attribute on an object, restoring it on exit."""
    original = getattr(obj, attr, None)
    setattr(obj, attr, value)
    try:
        yield
    finally:
        setattr(obj, attr, original)


# ---------------------------------------------------------------------------
# 5. contextlib.suppress and contextlib.closing examples
# ---------------------------------------------------------------------------
def demo_suppress() -> None:
    """contextlib.suppress silences specified exception types."""
    with contextlib.suppress(FileNotFoundError):
        open("/nonexistent/path.txt")  # noqa: WPS515 — intentional
    print("suppress: FileNotFoundError silently ignored")


class FakeLegacyResource:
    """Simulates a resource with a close() method but no context-manager support."""

    def __init__(self) -> None:
        self.open = True

    def read(self) -> str:
        return "data"

    def close(self) -> None:
        self.open = False


def demo_closing() -> None:
    """contextlib.closing wraps any object with .close() as a context manager."""
    resource = FakeLegacyResource()
    with contextlib.closing(resource) as r:
        data = r.read()
    assert not resource.open
    print(f"closing: resource closed automatically, data={data!r}")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Timer
    with Timer() as t:
        _ = sum(range(1_000_000))
    print(f"Timer: {t.elapsed:.4f}s")

    # DatabaseConnection (success)
    db = DatabaseConnection("sqlite:///demo.db")
    with db:
        db.execute("INSERT INTO t VALUES (1)")
    print(f"Committed={db.committed}, closed={not db.connected}")

    # DatabaseConnection (failure → rollback)
    db2 = DatabaseConnection("sqlite:///demo.db")
    try:
        with db2:
            db2.execute("INSERT INTO t VALUES (2)")
            raise ValueError("Oops!")
    except ValueError:
        pass
    print(f"RolledBack={db2.rolled_back}")

    # @contextmanager form
    with managed_connection("postgres://localhost/mydb") as conn:
        conn.execute("SELECT 1")
    print(f"managed_connection committed: {conn.committed}")

    demo_suppress()
    demo_closing()
