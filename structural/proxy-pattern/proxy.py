"""
Proxy Pattern — three variants.

1. VirtualProxy   — defers creation of the real subject until needed.
2. ProtectionProxy — checks permissions before delegating.
3. CachingProxy   — memoises results of expensive operations.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Subject interface
# ---------------------------------------------------------------------------
class Service(ABC):
    """Common interface for both real subject and proxies."""

    @abstractmethod
    def request(self, query: str) -> str:
        """Execute a (possibly expensive) request."""


# ---------------------------------------------------------------------------
# Real subject
# ---------------------------------------------------------------------------
class RealService(Service):
    """The actual (heavyweight) service that does real work.

    In a real system this might open a network connection or load a file.
    """

    def __init__(self) -> None:
        # Simulate expensive initialisation
        self._initialized = True

    def request(self, query: str) -> str:
        return f"RealService result for '{query}'"


# ---------------------------------------------------------------------------
# 1. Virtual Proxy (lazy initialisation)
# ---------------------------------------------------------------------------
class VirtualProxy(Service):
    """Creates the RealService only when first accessed.

    Args:
        (none) — RealService is constructed lazily.
    """

    def __init__(self) -> None:
        self._real: RealService | None = None
        self._load_count = 0

    def request(self, query: str) -> str:
        if self._real is None:
            self._real = RealService()
            self._load_count += 1
        return self._real.request(query)

    @property
    def loaded(self) -> bool:
        """True if the real service has been instantiated."""
        return self._real is not None

    @property
    def load_count(self) -> int:
        return self._load_count


# ---------------------------------------------------------------------------
# 2. Protection Proxy (access control)
# ---------------------------------------------------------------------------
class ProtectionProxy(Service):
    """Only allows requests from permitted users.

    Args:
        real_service: The service to protect.
        allowed_users: Set of user names that may access the service.
    """

    def __init__(self, real_service: Service, allowed_users: set[str]) -> None:
        self._real = real_service
        self._allowed = allowed_users
        self._current_user: str = ""

    def set_user(self, user: str) -> None:
        """Set the active user for subsequent requests."""
        self._current_user = user

    def request(self, query: str) -> str:
        if self._current_user not in self._allowed:
            raise PermissionError(
                f"User '{self._current_user}' is not allowed to access this service."
            )
        return self._real.request(query)


# ---------------------------------------------------------------------------
# 3. Caching Proxy (memoisation)
# ---------------------------------------------------------------------------
class CachingProxy(Service):
    """Memoises results of the real service to avoid redundant calls.

    Args:
        real_service: The service whose results are cached.
    """

    def __init__(self, real_service: Service) -> None:
        self._real = real_service
        self._cache: dict[str, str] = {}
        self._hit_count = 0
        self._miss_count = 0

    def request(self, query: str) -> str:
        if query in self._cache:
            self._hit_count += 1
            return self._cache[query]
        result = self._real.request(query)
        self._cache[query] = result
        self._miss_count += 1
        return result

    def invalidate(self, query: str) -> None:
        """Remove a cached result."""
        self._cache.pop(query, None)

    @property
    def hit_count(self) -> int:
        return self._hit_count

    @property
    def miss_count(self) -> int:
        return self._miss_count


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== VirtualProxy ===")
    vp = VirtualProxy()
    print(f"Loaded before first call: {vp.loaded}")
    print(vp.request("hello"))
    print(f"Loaded after first call: {vp.loaded}")
    print(f"Load count: {vp.load_count}")
    print(vp.request("world"))
    print(f"Load count (still 1): {vp.load_count}")

    print("\n=== ProtectionProxy ===")
    real = RealService()
    pp = ProtectionProxy(real, allowed_users={"alice", "bob"})
    pp.set_user("alice")
    print(pp.request("secret data"))
    pp.set_user("eve")
    try:
        pp.request("secret data")
    except PermissionError as exc:
        print(f"Blocked: {exc}")

    print("\n=== CachingProxy ===")
    cp = CachingProxy(RealService())
    print(cp.request("query-A"))
    print(cp.request("query-A"))   # cache hit
    print(cp.request("query-B"))
    print(f"Hits: {cp.hit_count}, Misses: {cp.miss_count}")
