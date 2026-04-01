"""pytest tests for singleton pattern implementations."""
from __future__ import annotations

import sys
import threading
from pathlib import Path

import pytest

# Allow imports from parent directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from singleton import AppLogger, ConfigRegistry, DatabasePool, singleton


# ---------------------------------------------------------------------------
# DatabasePool (metaclass singleton)
# ---------------------------------------------------------------------------
class TestDatabasePool:
    def setup_method(self) -> None:
        # Reset singleton between tests via internal dict
        DatabasePool._instances.pop(DatabasePool, None)  # type: ignore[attr-defined]

    def test_same_instance_returned(self) -> None:
        p1 = DatabasePool()
        p2 = DatabasePool()
        assert p1 is p2

    def test_first_args_win(self) -> None:
        p1 = DatabasePool(max_connections=7)
        p2 = DatabasePool(max_connections=99)
        assert p2.max_connections == 7   # second call ignored

    def test_thread_safe_creation(self) -> None:
        instances: list[DatabasePool] = []
        lock = threading.Lock()

        def create() -> None:
            inst = DatabasePool()
            with lock:
                instances.append(inst)

        threads = [threading.Thread(target=create) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(set(id(i) for i in instances)) == 1

    def test_acquire_release(self) -> None:
        pool = DatabasePool()
        h = pool.acquire()
        assert h in pool._pool
        pool.release(h)
        assert h not in pool._pool


# ---------------------------------------------------------------------------
# ConfigRegistry (__new__ singleton)
# ---------------------------------------------------------------------------
class TestConfigRegistry:
    def setup_method(self) -> None:
        ConfigRegistry._instance = None  # type: ignore[attr-defined]

    def test_same_instance_returned(self) -> None:
        r1 = ConfigRegistry()
        r2 = ConfigRegistry()
        assert r1 is r2

    def test_shared_state(self) -> None:
        r1 = ConfigRegistry()
        r1.set("foo", 42)
        r2 = ConfigRegistry()
        assert r2.get("foo") == 42

    def test_default_value(self) -> None:
        cfg = ConfigRegistry()
        assert cfg.get("missing", "default") == "default"


# ---------------------------------------------------------------------------
# AppLogger (@singleton decorator)
# ---------------------------------------------------------------------------
class TestAppLogger:
    def test_same_instance_returned(self) -> None:
        lg1 = AppLogger()
        lg2 = AppLogger()
        assert lg1 is lg2

    def test_shared_log_entries(self) -> None:
        lg1 = AppLogger()
        lg2 = AppLogger()
        before = len(lg1.entries)
        lg1.log("test-message")
        assert len(lg2.entries) == before + 1
        assert lg2.entries[-1] == "test-message"


# ---------------------------------------------------------------------------
# Custom @singleton decorator
# ---------------------------------------------------------------------------
class TestSingletonDecorator:
    def test_decorator_enforces_singleton(self) -> None:
        @singleton
        class Counter:
            def __init__(self) -> None:
                self.value = 0

        c1 = Counter()
        c2 = Counter()
        assert c1 is c2

    def test_thread_safe_via_decorator(self) -> None:
        @singleton
        class Service:
            pass

        results: list[int] = []
        lock = threading.Lock()

        def create() -> None:
            s = Service()
            with lock:
                results.append(id(s))

        threads = [threading.Thread(target=create) for _ in range(15)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(set(results)) == 1
