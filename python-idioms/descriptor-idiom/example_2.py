"""
Example 2 — CachedProperty for expensive computed attributes.
"""
from __future__ import annotations

import math
import time

from descriptor import CachedProperty


class HeavyMathObject:
    def __init__(self, n: int) -> None:
        self.n = n
        self._prime_count_calls = 0

    def _count_primes(self) -> int:
        self._prime_count_calls += 1
        # Sieve of Eratosthenes (deliberately not super fast to show caching effect)
        sieve = bytearray([1]) * (self.n + 1)
        sieve[0] = sieve[1] = 0
        for i in range(2, int(self.n ** 0.5) + 1):
            if sieve[i]:
                sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
        return sum(sieve)

    prime_count = CachedProperty(_count_primes)  # type: ignore[arg-type]

    def _calc_factorial_sum(self) -> int:
        return sum(math.factorial(i) for i in range(min(self.n, 15)))

    factorial_sum = CachedProperty(_calc_factorial_sum)  # type: ignore[arg-type]


def main() -> None:
    obj = HeavyMathObject(100_000)

    t0 = time.perf_counter()
    count = obj.prime_count
    t1 = time.perf_counter()
    print(f"Primes up to 100,000: {count} (computed in {t1 - t0:.4f}s)")

    t2 = time.perf_counter()
    count2 = obj.prime_count  # cached
    t3 = time.perf_counter()
    print(f"Cached access: {count2} (in {t3 - t2:.6f}s)")
    print(f"_count_primes called {obj._prime_count_calls} time(s)")  # 1

    print(f"Factorial sum: {obj.factorial_sum}")


if __name__ == "__main__":
    main()
