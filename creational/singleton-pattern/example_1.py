"""
Example 1 — Database connection pool singleton.

Demonstrates that multiple "creation" calls across threads all receive the
same DatabasePool instance.
"""
from __future__ import annotations

import threading
from singleton import DatabasePool


def worker(results: list[int], idx: int) -> None:
    pool = DatabasePool(max_connections=5)
    results[idx] = id(pool)


def main() -> None:
    results: list[int] = [0] * 10
    threads = [threading.Thread(target=worker, args=(results, i)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(set(results)) == 1, "All threads must get the same instance!"
    print(f"All 10 threads received pool id={results[0]}")
    print("Database connection pool singleton works correctly across threads.")

    pool = DatabasePool()
    h1 = pool.acquire()
    h2 = pool.acquire()
    print(f"Acquired: {h1}, {h2} — active={len(pool._pool)}")
    pool.release(h1)
    print(f"After release — active={len(pool._pool)}")


if __name__ == "__main__":
    main()
