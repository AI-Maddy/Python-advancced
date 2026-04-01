"""Chain of Responsibility — Example 1: HTTP Middleware Chain.

Simulates a web framework's middleware pipeline:
  AuthMiddleware → RateLimiterMiddleware → LoggingMiddleware → Handler
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class HttpRequest:
    method: str
    path: str
    headers: dict[str, str] = field(default_factory=dict)
    user: str | None = None


@dataclass
class HttpResponse:
    status: int
    body: str


class Middleware(ABC):
    def __init__(self) -> None:
        self._next: Middleware | None = None

    def set_next(self, mw: Middleware) -> Middleware:
        self._next = mw
        return mw

    @abstractmethod
    def handle(self, request: HttpRequest) -> HttpResponse: ...

    def _forward(self, request: HttpRequest) -> HttpResponse:
        if self._next:
            return self._next.handle(request)
        return HttpResponse(404, "Not Found")


class AuthMiddleware(Middleware):
    """Rejects requests without a valid Authorization header."""
    VALID_TOKENS: frozenset[str] = frozenset({"token-abc", "token-xyz"})

    def handle(self, request: HttpRequest) -> HttpResponse:
        token = request.headers.get("Authorization")
        if token not in self.VALID_TOKENS:
            print(f"  [Auth] DENIED {request.path}")
            return HttpResponse(401, "Unauthorized")
        request.user = token
        print(f"  [Auth] Passed for token {token[:9]}...")
        return self._forward(request)


class RateLimiterMiddleware(Middleware):
    """Limits each user to max_requests calls."""

    def __init__(self, max_requests: int = 3) -> None:
        super().__init__()
        self._counts: dict[str, int] = {}
        self._max = max_requests

    def handle(self, request: HttpRequest) -> HttpResponse:
        user = request.user or "anonymous"
        self._counts[user] = self._counts.get(user, 0) + 1
        if self._counts[user] > self._max:
            print(f"  [RateLimit] THROTTLED {user} ({self._counts[user]} reqs)")
            return HttpResponse(429, "Too Many Requests")
        print(f"  [RateLimit] OK ({self._counts[user]}/{self._max})")
        return self._forward(request)


class LoggingMiddleware(Middleware):
    """Logs the request and passes it on."""
    def handle(self, request: HttpRequest) -> HttpResponse:
        print(f"  [Log] {request.method} {request.path}")
        response = self._forward(request)
        print(f"  [Log] Response: {response.status}")
        return response


class AppHandler(Middleware):
    """Final handler — returns a 200 OK."""
    def handle(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse(200, f"OK: {request.path}")


def main() -> None:
    auth = AuthMiddleware()
    rate = RateLimiterMiddleware(max_requests=2)
    log = LoggingMiddleware()
    app = AppHandler()
    auth.set_next(rate).set_next(log).set_next(app)

    good_headers = {"Authorization": "token-abc"}

    for i in range(4):
        print(f"\n-- Request {i+1} --")
        resp = auth.handle(HttpRequest("GET", "/api/data", good_headers))
        print(f"   Final: {resp.status} {resp.body}")

    print("\n-- Unauthenticated --")
    resp = auth.handle(HttpRequest("GET", "/secret", {}))
    print(f"   Final: {resp.status} {resp.body}")


if __name__ == "__main__":
    main()
